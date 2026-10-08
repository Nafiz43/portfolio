"""Build and search a source-attributed portfolio entity/relationship graph.

Only the explicitly listed public portfolio files are ingested. No filesystem,
shell, or arbitrary URL access is available to the conversational model.
"""
import hashlib
import json
import math
import re
import subprocess
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://nafiz43.github.io/portfolio/"
INPUTS = ["index.html", "data/publications.json", "js/work_experience.js",
          "js/awards.js", "js/activities.js", "js/teaching_experience_mist.js", "js/projects.js"]


class Element:
    def __init__(self, tag="", attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def text(self):
        return " ".join(" ".join(c.text() if isinstance(c, Element) else c
                                 for c in self.children).split())

    def find(self, tag=None, **attrs):
        found = []
        if (tag is None or self.tag == tag) and all(self.attrs.get(k) == v for k, v in attrs.items()):
            found.append(self)
        for c in self.children:
            if isinstance(c, Element):
                found.extend(c.find(tag, **attrs))
        return found


class HTML(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Element()
        self.stack = [self.root]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Element(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in {"img", "br", "hr", "input", "link", "meta", "source", "wbr"}:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, text):
        if self.stack[-1].tag not in {"script", "style"}:
            self.stack[-1].children.append(text)


def plain(value):
    return HTML(str(value)).root.text()


def js_data(filename, variable):
    # Evaluate only the trusted, checked-in data literal, never visitor content.
    script = r"""
const fs = require('fs'), vm = require('vm');
const source = fs.readFileSync(process.argv[1], 'utf8');
const re = new RegExp('const\\s+' + process.argv[2] + '\\s*=\\s*(\\[[\\s\\S]*?\\n\\s*\\]);');
const match = source.match(re);
if (!match) throw new Error('Portfolio data array missing');
process.stdout.write(JSON.stringify(vm.runInNewContext('(' + match[1] + ')', {}, {timeout:1000})));
"""
    return json.loads(subprocess.check_output(
        ["node", "-e", script, str(ROOT / filename), variable], text=True, timeout=5))


TOPICS = {
    "Large language models": r"\bLLMs?\b|language models?|Llama|Mixtral",
    "Retrieval-augmented generation": r"\bRAG\b|retrieval.augmented",
    "AI for health": r"medical|clinical|radiology|mammograph|health|AngioVision",
    "Software engineering": r"software engineering|open.source|\bOSS\b|repositor|RepoWise|OSSPREY",
    "Machine learning": r"machine learning|deep learning|\bML\b|\bLSTM\b|neural",
    "Vision-language models": r"vision.language|\bVLMs?\b|AngioVision|MammoGen",
    "Human-computer interaction": r"usability|user interface|human.computer|\bHCI\b",
}


def build_graph():
    nodes, edges = {}, []

    def add(kind, label, text, source, **extra):
        identifier = kind + ":" + hashlib.sha256((label + source).encode()).hexdigest()[:12]
        nodes[identifier] = dict(id=identifier, type=kind, label=plain(label),
                                 text=plain(text), source=source, **extra)
        return identifier

    def edge(a, relation, b):
        item = dict(source=a, relation=relation, target=b)
        if item not in edges:
            edges.append(item)

    html = HTML((ROOT / "index.html").read_text()).root
    about = html.find("section", id="about")[0]
    bio = " ".join(p.text() for p in about.find("p", **{"class": "lead"}))
    headline = about.find("div", **{"class": "subheading mb-5"})[0].text()
    person = add("person", "Nafiz Imtiaz Khan", headline + ". " + bio, SITE + "#about")
    for name, relation in [("Vladimir Filkov", "advised_by"), ("Roger Eric Goldman", "coadvised_by")]:
        mentor = add("person", name, name + " advises Nafiz Imtiaz Khan.", SITE + "#about")
        edge(person, relation, mentor)
    for item in about.find("div", **{"class": "description"}):
        education = add("education", item.text(), item.text(), SITE + "#about")
        edge(person, "educated_at", education)
    for item in about.find("ul", **{"class": "news-list"})[0].find("li"):
        news = add("news", item.text(), item.text(), SITE + "#about")
        edge(person, "announced", news)
    publications = json.loads((ROOT / "data/publications.json").read_text())
    for p in publications:
        source = p.get("link") or SITE + "#research"
        pub = add("publication", p["title"],
                  " | ".join(str(p.get(k, "")) for k in ["title", "authors", "venue", "year", "award", "description"]),
                  source, year=p.get("year"), selected=p.get("selected", False))
        edge(person, "authored", pub)
        if p.get("venue"):
            venue = add("venue", p["venue"], p["venue"], SITE + "#research")
            edge(pub, "published_in", venue)
    for job in js_data("js/work_experience.js", "experiences"):
        org = add("organization", job["company"], job["company"], job.get("companyLink") or SITE + "#work")
        role = add("role", job["title"] + " at " + job["company"],
                   job["title"] + " at " + job["company"] + "; " + job["date"] + ". " + " ".join(job["tasks"]), SITE + "#work")
        edge(person, "held_role", role)
        edge(role, "at_organization", org)
        for task in job["tasks"]:
            contribution = add("contribution", plain(task)[:120], task, SITE + "#work")
            edge(role, "contributed", contribution)
            edge(person, "contributed", contribution)
    for filename, var, kind, relation, section in [
        ("js/awards.js", "awards", "award", "received", "awards"),
        ("js/activities.js", "roles", "activity", "participated_in", "activities"),
        ("js/teaching_experience_mist.js", "courses", "course", "taught", "teaching"),
        ("js/projects.js", "articles", "project", "built", "work"),
    ]:
        for item in js_data(filename, var):
            label = item.get("title") or item.get("name")
            text = " | ".join(str(v) for k, v in item.items() if k not in {"image", "link", "eventLink", "organizerLink", "venueLink"})
            node = add(kind, label, text, item.get("link") or SITE + "#" + section)
            edge(person, relation, node)
    for section in ["patents", "contact"]:
        for item in html.find("section", id=section):
            node = add(section, section.title(), item.text(), SITE + "#" + section)
            edge(person, "has_" + section, node)
    for label, pattern in TOPICS.items():
        topic = add("topic", label, label, SITE + "#research")
        for node in list(nodes.values()):
            if node["type"] in {"publication", "contribution", "project", "person"} and re.search(pattern, node["text"], re.I):
                edge(node["id"], "about_topic", topic)
    # Explicit named-project mentions connect publications to implementation work.
    for label in ["RepoWise", "OSSPREY", "EvidenceBot", "ReACT-GPT", "PCL-Fetcher", "MammoGen-RAG", "AngioVision", "ReACTive"]:
        mentions = [n for n in nodes.values() if n["type"] in {"publication", "contribution"} and re.search(r"\b" + re.escape(label) + r"\b", n["text"], re.I)]
        if mentions:
            project = add("project", label, " ".join(n["text"] for n in mentions if n["type"] == "contribution"), SITE + "#work")
            edge(person, "built", project)
            for n in mentions:
                edge(n["id"], "describes_project", project)
    graph = dict(person=person, publication_count=len(publications), nodes=list(nodes.values()), edges=edges,
                 source_files=INPUTS, fingerprint=fingerprint())
    (ROOT / "server/knowledge_graph.json").write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n")
    return graph


def fingerprint():
    return hashlib.sha256(b"".join((ROOT / f).read_bytes() for f in INPUTS)).hexdigest()


STOP = set("a an the is are was were do does did to of in on for with and or it his he him her she they their you your me my what which how can could would about tell please nafiz khan imtiaz".split())


def tokens(text):
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 1]


class KnowledgeGraph:
    def __init__(self):
        path = ROOT / "server/knowledge_graph.json"
        self.graph = json.loads(path.read_text()) if path.exists() else build_graph()
        if self.graph.get("fingerprint") != fingerprint():
            self.graph = build_graph()
        self.nodes = {n["id"]: n for n in self.graph["nodes"]}
        self.terms = {key: Counter(tokens(n["label"] + " " + n["label"] + " " + n["text"])) for key, n in self.nodes.items()}
        self.df = Counter(t for words in self.terms.values() for t in words)
        self.adj = defaultdict(list)
        for e in self.graph["edges"]:
            self.adj[e["source"]].append(e["target"])
            self.adj[e["target"]].append(e["source"])

    def search(self, query, limit=8):
        expanded = query
        for pattern, extra in [(r"\b(papers?|publications?|research)\b", "publication"),
                               (r"\b(teach|teaching|courses)\b", "course"),
                               (r"\b(education|degrees?|study|studied)\b", "education"),
                               (r"\b(experience|jobs?|worked|internships?)\b", "role"),
                               (r"\b(awards?|honors?)\b", "award"),
                               (r"\b(advisor|advisors|advises|supervisor)\b", "Filkov Goldman")]:
            if re.search(pattern, query, re.I):
                expanded += " " + extra
        q = set(tokens(expanded))
        scores = {}
        for key, words in self.terms.items():
            node = self.nodes[key]
            score = sum(math.log(1 + len(self.nodes) / (1 + self.df[t])) * words[t] / (words[t] + 0.7 + sum(words.values()) / 160) for t in q if words[t])
            if node["type"] in q:
                score += 3
            if node.get("selected") and "publication" in q:
                score += 3
            if score:
                scores[key] = score
        seeds = sorted(scores, key=scores.get, reverse=True)[:limit]
        # One-hop expansion follows actual relationships, without exploding through
        # the person/topic hubs into every publication.
        for key in seeds[:4]:
            if self.nodes[key]["type"] in {"person", "topic", "venue", "organization"}:
                continue
            for neighbor in self.adj[key]:
                if self.nodes[neighbor]["type"] not in {"person", "topic", "venue"}:
                    scores[neighbor] = scores.get(neighbor, 0) + scores[key] * 0.12
        chosen = sorted(scores, key=scores.get, reverse=True)[:limit]
        if self.graph["person"] not in chosen:
            chosen.insert(0, self.graph["person"])
        result = [self.nodes[key] for key in chosen]
        edges = [e for e in self.graph["edges"] if e["source"] in chosen and e["target"] in chosen]
        return result, edges


if __name__ == "__main__":
    graph = build_graph()
    print(f"Built {len(graph['nodes'])} nodes and {len(graph['edges'])} relationships from {len(INPUTS)} public files.")
