// Research tools shown as cards in the Projects section (after Publications). Newest first.
// The old MIST projects that were here are in git history (before 2026-11-23).
document.addEventListener("DOMContentLoaded", function () {
  const projects = [
    {
      title: "AngioVision",
      image: "img/projects/angiovision.svg",
      venue: "Ongoing research with UC Davis Health",
      description: "A vision-language model that learns to read digital subtraction angiography (DSA) videos from the reports that interventional radiologists already write, with no manual labels. I designed a new contrastive learning algorithm for this task and built AngioBERT, a custom clinical text encoder trained on UC Davis Health radiology reports.",
      links: {} // code and data are private (patient data)
    },
    {
      title: "MedVision",
      image: "img/projects/medvision.jpg",
      venue: "UC Davis Radiology Research Symposium 2026",
      description: "Ask a hospital imaging archive questions in words, with an image, or both. It runs on premises inside the hospital network.",
      links: { Page: "medvision/", Video: "medvision/medvision_demo.mp4" }
    },
    {
      title: "RepoWise",
      image: "img/projects/repowise.jpg",
      venue: "SEET 2026 (Springer CCIS)",
      award: "Best Paper Award",
      description: "A conversational tool that answers questions about an open-source repository's governance, contribution guidelines, commits and issues, with retrieval-augmented generation and cited sources.",
      links: {
        Page: "https://repowise.github.io/RepoWise-website",
        Paper: "https://link.springer.com/chapter/10.1007/978-3-032-39763-8_16",
        Code: "https://github.com/RepoWise",
        Demo: "https://repowise.netlify.app",
        Video: "https://www.youtube.com/watch?v=0xwoYf62TEc"
      }
    },
    {
      title: "OSSPREY",
      image: "img/projects/ossprey.jpg",
      venue: "ASE 2025 Tool Demonstrations",
      description: "Forecasts the sustainability of an open-source project from its social and technical networks, and recommends research-backed actions to keep it on track.",
      links: {
        Page: "https://oss-prey.github.io/OSSPREY-Website/",
        Paper: "https://ieeexplore.ieee.org/abstract/document/11334666",
        Code: "https://github.com/OSS-PREY",
        Video: "https://www.youtube.com/watch?v=N7a0v4hPylU"
      }
    },
    {
      title: "EvidenceBot",
      image: "img/projects/evidencebot.jpg",
      venue: "FSE 2025 Tool Demonstrations",
      description: "A privacy-preserving, local RAG tool for large document sets, with tunable settings and a module that evaluates LLM answers against ground truth.",
      links: {
        Page: "https://nafiz43.github.io/EvidenceBot",
        Paper: "https://dl.acm.org/doi/10.1145/3696630.3728607",
        Code: "https://github.com/Nafiz43/EvidenceBot",
        Video: "https://www.youtube.com/watch?v=oZZRDebxTBg"
      }
    },
    // Cards with more: true fold under the "More projects" button.
    {
      more: true,
      title: "AIGovernanceBench",
      image: "img/projects/aigovernancebench.jpg",
      venue: "Ongoing research",
      description: "A searchable directory of real Agent Skills and AI governance files. It recommends skills for a given role and task, and finds overlaps and conflicts between agent instructions.",
      links: {
        Page: "https://nafiz43.github.io/AIGovernanceBench/",
        Code: "https://github.com/Nafiz43/AIGovernanceBench"
      }
    },
    {
      more: true,
      title: "PCL-Fetcher",
      image: "img/projects/pcl-fetcher.jpg",
      venue: "JAMIA Open 2026",
      description: "Uses LLMs to read interventional radiology procedure reports and fill in the trainee's procedural case log, so residents spend less time on manual logging.",
      links: {
        Page: "https://nafiz43.github.io/PCL-Fetcher/",
        Paper: "https://doi.org/10.1093/jamiaopen/ooag067",
        Code: "https://github.com/Nafiz43/PCL-Fetcher"
      }
    },
    {
      more: true,
      title: "ReACT-GPT",
      image: "img/projects/react-gpt.jpg",
      venue: "arXiv preprint 2026",
      description: "Uses several LLMs to extract evidence-based actions for OSS sustainability from research papers, checks each one against its source, and sorts them by practice. Available as a Python package.",
      links: {
        Page: "https://nafiz43.github.io/ReACT-GPT",
        Paper: "https://arxiv.org/abs/2602.11746",
        Code: "https://github.com/Nafiz43/react-gpt-package"
      }
    },
    {
      more: true,
      title: "MammoWise",
      image: "img/projects/mammowise.jpg",
      venue: "arXiv preprint 2026",
      description: "A local, multi-model RAG pipeline that writes mammography reports from images, and compares vision-language models across zero-shot, few-shot, chain-of-thought, RAG and fine-tuning.",
      links: {
        Paper: "https://arxiv.org/abs/2602.22462",
        Code: "https://github.com/Nafiz43/MammoGen-RAG"
      }
    },
    {
      more: true,
      title: "ReACTive",
      image: "img/projects/reactive.jpg",
      venue: "FSE 2024",
      description: "An interactive tool that links 105 Researched Actionables (ReACTs), taken from 186 articles, to the OSS sustainability features they affect and to the people responsible for them.",
      links: {
        Page: "https://nafiz43.github.io/ReACTive/",
        Paper: "https://dl.acm.org/doi/abs/10.1145/3663529.3663777",
        Code: "https://github.com/Nafiz43/ReACTive"
      }
    }
  ];

  const container = document.getElementById("project-container");
  if (!container) return;
  const card = p => `
    <div class="project-card">
      ${(u => u ? `<a href="${u}" target="_blank" rel="noopener">` : "")(p.links.Page || Object.values(p.links)[0])}<img src="${p.image}" alt="${p.title} screenshot" loading="lazy" decoding="async">${Object.keys(p.links).length ? "</a>" : ""}
      <div class="project-body">
        <h3>${p.title}</h3>
        <div class="project-venue">${p.venue}${p.award ? ` <span class="pub-award">🏆 ${p.award}</span>` : ""}</div>
        <p>${p.description}</p>
        <div class="project-links">${Object.entries(p.links).map(([k, u]) => `<a href="${u}" target="_blank" rel="noopener">${k}</a>`).join(" · ")}</div>
      </div>
    </div>`;
  const more = projects.filter(p => p.more);
  container.innerHTML = projects.filter(p => !p.more).map(card).join("");
  if (more.length) container.insertAdjacentHTML("afterend",
    `<details class="pub-all"><summary>More projects</summary><div class="project-grid mt-3">${more.map(card).join("")}</div></details>`);
});
