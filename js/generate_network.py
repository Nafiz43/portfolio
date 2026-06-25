#!/usr/bin/env python3
"""
generate_mh_network.py
─────────────────────────────────────────────────────────────────────────────
Reads mental_health_benchmarks.csv (or any path passed as argv[1]) and writes
an interactive D3.js network graph to mental_health_network.html (or argv[2]).

Edges are built from three relationship types:
  category   – same base category (solid line)
  source     – shared Reddit / social-media source (dashed line)
  dependency – known dataset-to-dataset dependency (dotted line)

All columns detected in the CSV are shown in the click-to-open sidebar.
Hovering a node shows its name.

Usage:
    python generate_mh_network.py [input.csv] [output.html]
"""

import csv, json, re, sys, math
from pathlib import Path

# ── defaults ─────────────────────────────────────────────────────────────────
DEFAULT_IN  = "mental_health_benchmarks.csv"
DEFAULT_OUT = "mental_health_network.html"

# ── category → colour ─────────────────────────────────────────────────────────
CAT_COLORS = {
    "clinical_psychiatric_reasoning":    "#4472C4",
    "text_detection_suicide_depression": "#E74C3C",
    "text_detection_depression":         "#E91E8C",
    "text_detection_stress":             "#FF9F43",
    "counseling_dialogue":               "#2ECC71",
    "safety_crisis":                     "#9B59B6",
}
DEFAULT_CLR = "#7F8C8D"

# ── friendly column labels ────────────────────────────────────────────────────
COL_LABELS = {
    "name":"Dataset Name","acronym":"Acronym","year":"Year",
    "task_type":"Task Type","dataset_size":"Dataset Size","size_unit":"Size Unit",
    "source":"Source","modality":"Modality",
    "sample_questions_or_labels":"Sample Questions / Labels",
    "creators_institution":"Creators / Institution",
    "paper_title":"Paper Title","paper_authors":"Authors","venue":"Venue",
    "dataset_link":"Dataset Link","access_conditions":"Access Conditions",
    "associated_article_link":"Associated Article Link",
    "category":"Category","limitations":"Limitations",
    "LLM as Judge":"LLM as Judge","llm_as_judge":"LLM as Judge",
}

LINK_COLS = {
    "dataset_link","associated_article_link",
    "Dataset Link","Associated Article Link",
}

# ── helpers ───────────────────────────────────────────────────────────────────
def base_cat(c):  return re.sub(r'\s*\[standard\]', '', c).strip()
def is_std(c):    return '[standard]' in str(c)
def node_clr(c):  return CAT_COLORS.get(base_cat(c), DEFAULT_CLR)

def build_edges(nodes):
    edges, seen = [], set()
    def add(a, b, t):
        k = tuple(sorted([a, b]))
        if k not in seen:
            seen.add(k)
            edges.append({"source": a, "target": b, "type": t})

    # 1. category edges
    by_cat = {}
    for n in nodes:
        by_cat.setdefault(base_cat(n["category"]), []).append(n["name"])
    for names in by_cat.values():
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                add(names[i], names[j], "category")

    # 2. shared Reddit / social-media source edges (cross-category)
    reddit = [n["name"] for n in nodes
              if "reddit" in n.get("source", "").lower()
              or "social" in n.get("source", "").lower()]
    for i in range(len(reddit)):
        for j in range(i + 1, len(reddit)):
            add(reddit[i], reddit[j], "source")

    # 3. explicit dependency edges
    deps = [
        ("CounselBench", "Counsel Chat"),
        ("CLPsych Shared Task Series (2015–2024)",
         "UMD Reddit Suicidality Dataset"),
        ("Mental Health Crisis Response Evaluation Dataset",
         "Reddit SuicideWatch and Mental Health Collection"),
        ("Mental Health Crisis Response Evaluation Dataset",
         "Emotional Support Conversation"),
    ]
    names_set = {n["name"] for n in nodes}
    for s, t in deps:
        if s in names_set and t in names_set:
            add(s, t, "dependency")

    return edges

def make_html(nodes, edges, columns):
    for n in nodes:
        n["_color"]   = node_clr(n.get("category", ""))
        n["_std"]     = is_std(n.get("category", ""))
        n["_basecat"] = base_cat(n.get("category", ""))

    cat_color_map = {n["_basecat"]: n["_color"] for n in nodes}
    col_labels    = {c: COL_LABELS.get(c, c.replace("_", " ").title()) for c in columns}
    link_cols     = [c for c in columns if c in LINK_COLS]

    data_js = (
        f"const NODES     = {json.dumps(nodes,         ensure_ascii=False)};\n"
        f"const EDGES     = {json.dumps(edges,         ensure_ascii=False)};\n"
        f"const COLUMNS   = {json.dumps(columns,       ensure_ascii=False)};\n"
        f"const CAT_COLORS= {json.dumps(cat_color_map, ensure_ascii=False)};\n"
        f"const COL_LABELS= {json.dumps(col_labels,    ensure_ascii=False)};\n"
        f"const LINK_COLS = new Set({json.dumps(link_cols, ensure_ascii=False)});\n"
    )
    return HTML_TEMPLATE.replace("/* __DATA__ */", data_js)

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    inp  = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_IN
    outp = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT

    with open(inp, encoding="utf-8") as f:
        all_rows = list(csv.DictReader(f))

    nodes   = [r for r in all_rows
               if r.get("name", "").strip() and r.get("name") != "SCOPE NOTE"]
    columns = list(all_rows[0].keys()) if all_rows else []
    edges   = build_edges(nodes)
    html    = make_html(nodes, edges, columns)

    Path(outp).write_text(html, encoding="utf-8")
    print(f"✓  {len(nodes)} nodes  |  {len(edges)} edges  →  {outp}")

# ── HTML template ─────────────────────────────────────────────────────────────
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mental Health Benchmarks · Network Graph</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,Arial,sans-serif;background:#0d1117;color:#c9d1d9;
     display:flex;height:100vh;overflow:hidden}

/* ── graph area ── */
#graph-wrap{flex:1;position:relative;overflow:hidden}
svg{width:100%;height:100%;cursor:grab}
svg:active{cursor:grabbing}

/* ── nodes ── */
.node circle{stroke-width:2;cursor:pointer;transition:filter .15s}
.node circle:hover{filter:brightness(1.35) drop-shadow(0 0 6px rgba(255,255,255,.4))}
.node text{font-size:10px;fill:#c9d1d9;pointer-events:none;user-select:none}

/* ── links ── */
.link{stroke-opacity:.55;pointer-events:none}

/* ── tooltip ── */
#tip{position:absolute;background:rgba(13,17,23,.92);border:1px solid #30363d;
     border-radius:6px;padding:6px 12px;font-size:12.5px;font-weight:600;color:#e6edf3;
     pointer-events:none;display:none;white-space:nowrap;box-shadow:0 4px 14px rgba(0,0,0,.5)}

/* ── sidebar ── */
#sidebar{width:400px;min-width:320px;background:#161b22;border-left:1px solid #30363d;
         overflow-y:auto;transform:translateX(100%);transition:transform .28s ease;
         position:relative;flex-shrink:0}
#sidebar.open{transform:translateX(0)}
#sb-close{position:sticky;top:0;z-index:10;background:#161b22;border-bottom:1px solid #30363d;
           padding:10px 16px;display:flex;justify-content:space-between;align-items:center}
#sb-close-btn{background:none;border:none;color:#8b949e;font-size:18px;cursor:pointer;line-height:1}
#sb-close-btn:hover{color:#e6edf3}
#sb-title{font-size:14px;font-weight:700;color:#e6edf3;flex:1;margin-right:8px;line-height:1.3}
#sb-body{padding:16px}

.meta-field{margin-bottom:13px}
.meta-label{font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;
            color:#8b949e;margin-bottom:3px}
.meta-value{font-size:12px;color:#c9d1d9;line-height:1.55;word-break:break-word}
.meta-value a{color:#58a6ff;text-decoration:none}
.meta-value a:hover{text-decoration:underline}
.meta-sep{border:none;border-top:1px solid #21262d;margin:14px 0}
.meta-badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;
            font-weight:600;color:#fff;margin-bottom:10px}
.std-badge{display:inline-block;background:#b8860b;color:#fff;font-size:10px;
           padding:1px 7px;border-radius:8px;margin-left:6px;vertical-align:middle}
.nf{color:#6e7681;font-style:italic}

/* ── controls panel ── */
#controls{position:absolute;top:14px;right:14px;display:flex;gap:6px;flex-direction:column;
           align-items:flex-end}
.ctrl-btn{background:rgba(22,27,34,.88);border:1px solid #30363d;color:#8b949e;
          border-radius:6px;padding:5px 11px;font-size:11.5px;cursor:pointer;
          transition:background .15s,color .15s;white-space:nowrap}
.ctrl-btn:hover{background:#21262d;color:#e6edf3}
.ctrl-btn.active{border-color:#58a6ff;color:#58a6ff}

/* ── category legend ── */
#cat-legend{position:absolute;top:14px;left:14px;background:rgba(22,27,34,.92);
            border:1px solid #30363d;border-radius:8px;padding:12px 14px;font-size:11.5px}
#cat-legend h4{color:#8b949e;margin-bottom:8px;font-size:10.5px;text-transform:uppercase;
               letter-spacing:.6px}
.cl-item{display:flex;align-items:center;gap:7px;margin-bottom:5px;cursor:pointer;
          border-radius:4px;padding:2px 4px;transition:background .12s}
.cl-item:hover{background:#21262d}
.cl-dot{width:11px;height:11px;border-radius:50%;flex-shrink:0}
.cl-label{color:#c9d1d9}

/* ── edge legend ── */
#edge-legend{position:absolute;bottom:14px;left:14px;background:rgba(22,27,34,.92);
             border:1px solid #30363d;border-radius:8px;padding:12px 14px;font-size:11.5px}
#edge-legend h4{color:#8b949e;margin-bottom:8px;font-size:10.5px;text-transform:uppercase;
                letter-spacing:.6px}
.el-item{display:flex;align-items:center;gap:8px;margin-bottom:5px;cursor:pointer;
          border-radius:4px;padding:2px 4px;transition:background .12s}
.el-item:hover{background:#21262d}
.el-line{width:26px;height:2px;flex-shrink:0}
.el-label{color:#c9d1d9}

/* ── stats bar ── */
#stats{position:absolute;bottom:14px;right:14px;background:rgba(22,27,34,.88);
       border:1px solid #30363d;border-radius:6px;padding:5px 12px;font-size:11px;
       color:#8b949e}
</style>
</head>
<body>

<div id="graph-wrap">
  <svg id="network"></svg>
  <div id="tip"></div>

  <!-- Category legend -->
  <div id="cat-legend">
    <h4>Category</h4>
    <div id="cat-items"></div>
  </div>

  <!-- Edge legend -->
  <div id="edge-legend">
    <h4>Edge Types</h4>
    <div class="el-item" data-etype="category">
      <div class="el-line" style="background:#5b9bd5"></div>
      <span class="el-label">Same Category</span>
    </div>
    <div class="el-item" data-etype="source">
      <svg width="26" height="6" style="flex-shrink:0">
        <line x1="0" y1="3" x2="26" y2="3" stroke="#e67e22" stroke-width="2"
              stroke-dasharray="5,3"/>
      </svg>
      <span class="el-label">Shared Source</span>
    </div>
    <div class="el-item" data-etype="dependency">
      <svg width="26" height="6" style="flex-shrink:0">
        <line x1="0" y1="3" x2="26" y2="3" stroke="#9b59b6" stroke-width="2"
              stroke-dasharray="2,4"/>
      </svg>
      <span class="el-label">Dependency</span>
    </div>
  </div>

  <!-- Controls -->
  <div id="controls">
    <button class="ctrl-btn" id="btn-reset">⟳ Reset View</button>
    <button class="ctrl-btn active" id="btn-labels">Labels On</button>
    <button class="ctrl-btn active" id="btn-cat-edges"  data-etype="category">Category Edges</button>
    <button class="ctrl-btn active" id="btn-src-edges"  data-etype="source">Source Edges</button>
    <button class="ctrl-btn active" id="btn-dep-edges"  data-etype="dependency">Dep. Edges</button>
  </div>

  <!-- Stats -->
  <div id="stats" id="stats"></div>
</div>

<!-- Sidebar -->
<div id="sidebar">
  <div id="sb-close">
    <div id="sb-title"></div>
    <button id="sb-close-btn" title="Close">✕</button>
  </div>
  <div id="sb-body"></div>
</div>

<script>
/* __DATA__ */

// ── layout constants ──────────────────────────────────────────────────────────
const W = () => document.getElementById('graph-wrap').clientWidth;
const H = () => document.getElementById('graph-wrap').clientHeight;

const EDGE_STYLES = {
  category:   { stroke:'#5b9bd5', width:1.6, dash:null },
  source:     { stroke:'#e67e22', width:1.2, dash:'6,3' },
  dependency: { stroke:'#9b59b6', width:1.2, dash:'2,5' },
};

// cluster center offsets (fraction of canvas)
const CLUSTER_POS = {
  'clinical_psychiatric_reasoning':    { fx:.30, fy:.28 },
  'text_detection_suicide_depression': { fx:.65, fy:.22 },
  'text_detection_depression':         { fx:.80, fy:.50 },
  'text_detection_stress':             { fx:.75, fy:.75 },
  'counseling_dialogue':               { fx:.45, fy:.75 },
  'safety_crisis':                     { fx:.18, fy:.65 },
};

// ── state ─────────────────────────────────────────────────────────────────────
let showLabels    = true;
let hiddenEtypes  = new Set();
let selectedNode  = null;

// ── build node / link arrays (D3 mutable copies) ─────────────────────────────
const nodeMap  = new Map(NODES.map(n => [n.name, {...n}]));
const simNodes = [...nodeMap.values()];
const simEdges = EDGES.map(e => ({
  source: nodeMap.get(e.source),
  target: nodeMap.get(e.target),
  type:   e.type,
})).filter(e => e.source && e.target);

// ── SVG setup ─────────────────────────────────────────────────────────────────
const svg  = d3.select('#network');
const root = svg.append('g').attr('class','root');
const zoom = d3.zoom().scaleExtent([.15, 4]).on('zoom', e => root.attr('transform', e.transform));
svg.call(zoom);

// arrow markers (for dependency edges)
svg.append('defs').selectAll('marker')
  .data(['dep'])
  .join('marker')
    .attr('id', 'arr-dep')
    .attr('viewBox','0 -4 8 8')
    .attr('refX', 20).attr('refY', 0)
    .attr('markerWidth', 5).attr('markerHeight', 5)
    .attr('orient','auto')
  .append('path')
    .attr('d','M0,-4L8,0L0,4')
    .attr('fill','#9b59b6');

const linkGroup = root.append('g').attr('class','links');
const nodeGroup = root.append('g').attr('class','nodes');

// ── links ─────────────────────────────────────────────────────────────────────
const linkSel = linkGroup.selectAll('line')
  .data(simEdges)
  .join('line')
  .attr('class','link')
  .each(function(d){
    const s = EDGE_STYLES[d.type] || EDGE_STYLES.category;
    d3.select(this)
      .attr('stroke', s.stroke)
      .attr('stroke-width', s.width)
      .attr('stroke-dasharray', s.dash || null)
      .attr('marker-end', d.type==='dependency' ? 'url(#arr-dep)' : null);
  });

// ── nodes ─────────────────────────────────────────────────────────────────────
const R      = 14;   // base radius
const R_STD  = 18;   // standard benchmark radius

const nodeSel = nodeGroup.selectAll('g.node')
  .data(simNodes, d => d.name)
  .join('g')
  .attr('class','node')
  .call(d3.drag()
    .on('start', (e,d) => { if(!e.active) sim.alphaTarget(.3).restart(); d.fx=d.x; d.fy=d.y; })
    .on('drag',  (e,d) => { d.fx=e.x; d.fy=e.y; })
    .on('end',   (e,d) => { if(!e.active) sim.alphaTarget(0); d.fx=null; d.fy=null; })
  );

// gold halo for [standard] nodes
nodeSel.filter(d => d._std)
  .append('circle')
  .attr('r', d => R_STD + 4)
  .attr('fill','none')
  .attr('stroke','#FFD700')
  .attr('stroke-width', 2.5)
  .attr('stroke-dasharray','4,2')
  .attr('opacity',.75);

nodeSel.append('circle')
  .attr('r', d => d._std ? R_STD : R)
  .attr('fill', d => d._color)
  .attr('stroke','#0d1117')
  .attr('stroke-width', 2);

// label
const labelSel = nodeSel.append('text')
  .attr('dy', d => (d._std ? R_STD : R) + 12)
  .attr('text-anchor','middle')
  .text(d => d.acronym && d.acronym !== 'not found' ? d.acronym : d.name.slice(0,14));

// ── tooltip ───────────────────────────────────────────────────────────────────
const tip = document.getElementById('tip');
nodeSel
  .on('mouseover', (e, d) => {
    tip.textContent = d.name;
    tip.style.display = 'block';
  })
  .on('mousemove', e => {
    tip.style.left = (e.offsetX + 14) + 'px';
    tip.style.top  = (e.offsetY - 28) + 'px';
  })
  .on('mouseout', () => { tip.style.display = 'none'; });

// ── sidebar ───────────────────────────────────────────────────────────────────
const sidebar  = document.getElementById('sidebar');
const sbTitle  = document.getElementById('sb-title');
const sbBody   = document.getElementById('sb-body');

function openSidebar(d) {
  selectedNode = d.name;
  sbTitle.innerHTML =
    `${d.name}` +
    (d._std ? `<span class="std-badge">★ standard</span>` : '');

  const rows = COLUMNS.filter(c => c !== 'name').map(col => {
    const raw  = d[col] || '';
    const val  = raw.trim();
    if (!val || val === 'not found') return '';
    const lbl  = COL_LABELS[col] || col.replace(/_/g,' ');
    const isLk = LINK_COLS.has(col);

    let display;
    if (isLk) {
      display = `<a href="${val}" target="_blank" rel="noopener">${val}</a>`;
    } else if (col === 'category') {
      const bc = d._basecat;
      const clr = CAT_COLORS[bc] || '#7f8c8d';
      display = `<span class="meta-badge" style="background:${clr}">${val}</span>`;
    } else {
      display = escHtml(val);
    }
    return `<div class="meta-field">
      <div class="meta-label">${escHtml(lbl)}</div>
      <div class="meta-value">${display}</div>
    </div>`;
  }).filter(Boolean);

  sbBody.innerHTML = rows.join('<hr class="meta-sep">');
  sidebar.classList.add('open');

  // dim all nodes, highlight selected
  nodeSel.select('circle').attr('opacity', n => n.name === d.name ? 1 : .35);
  linkSel.attr('stroke-opacity', l =>
    (l.source.name === d.name || l.target.name === d.name) ? .9 : .1);
}

function closeSidebar() {
  sidebar.classList.remove('open');
  selectedNode = null;
  nodeSel.select('circle').attr('opacity', 1);
  linkSel.attr('stroke-opacity', .55);
}

nodeSel.on('click', (e, d) => { e.stopPropagation(); openSidebar(d); });
svg.on('click', closeSidebar);
document.getElementById('sb-close-btn').addEventListener('click', closeSidebar);

// ── force simulation ──────────────────────────────────────────────────────────
const sim = d3.forceSimulation(simNodes)
  .force('link',    d3.forceLink(simEdges).id(d => d.name)
                       .distance(d => d.type === 'category' ? 90 : 160)
                       .strength(d => d.type === 'category' ? .4 : .15))
  .force('charge',  d3.forceManyBody().strength(-420))
  .force('collide', d3.forceCollide(R_STD + 8))
  .force('center',  d3.forceCenter(W() / 2, H() / 2))
  .force('cluster', clusterForce(.18))
  .on('tick', ticked);

function clusterForce(strength) {
  return (alpha) => {
    const w = W(), h = H();
    simNodes.forEach(n => {
      const pos = CLUSTER_POS[n._basecat];
      if (pos) {
        n.vx += (pos.fx * w - n.x) * alpha * strength;
        n.vy += (pos.fy * h - n.y) * alpha * strength;
      }
    });
  };
}

function ticked() {
  linkSel
    .attr('x1', d => d.source.x).attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
  nodeSel.attr('transform', d => `translate(${d.x},${d.y})`);
}

// ── controls ──────────────────────────────────────────────────────────────────
// labels toggle
document.getElementById('btn-labels').addEventListener('click', function() {
  showLabels = !showLabels;
  labelSel.attr('display', showLabels ? null : 'none');
  this.textContent = showLabels ? 'Labels On' : 'Labels Off';
  this.classList.toggle('active', showLabels);
});

// reset view
document.getElementById('btn-reset').addEventListener('click', () => {
  svg.transition().duration(600).call(zoom.transform, d3.zoomIdentity);
});

// edge type toggles
['category','source','dependency'].forEach(etype => {
  const btn = document.querySelector(`[data-etype="${etype}"]`);
  if (!btn) return;
  btn.addEventListener('click', function() {
    if (hiddenEtypes.has(etype)) {
      hiddenEtypes.delete(etype);
      this.classList.add('active');
    } else {
      hiddenEtypes.add(etype);
      this.classList.remove('active');
    }
    linkSel.attr('display', d => hiddenEtypes.has(d.type) ? 'none' : null);
  });
});

// el-item clicks in legend (mirror buttons)
document.querySelectorAll('.el-item[data-etype]').forEach(el => {
  el.addEventListener('click', () => {
    const btn = document.querySelector(`button[data-etype="${el.dataset.etype}"]`);
    if (btn) btn.click();
  });
});

// ── category legend ───────────────────────────────────────────────────────────
const catItems = document.getElementById('cat-items');
Object.entries(CAT_COLORS).forEach(([cat, clr]) => {
  const div = document.createElement('div');
  div.className = 'cl-item';
  div.innerHTML = `<div class="cl-dot" style="background:${clr}"></div>
                   <span class="cl-label">${cat.replace(/_/g,' ')}</span>`;
  div.addEventListener('click', () => highlightCat(cat, div));
  catItems.appendChild(div);
});

let activeCat = null;
function highlightCat(cat, el) {
  if (activeCat === cat) {
    activeCat = null;
    nodeSel.select('circle').attr('opacity', 1);
    linkSel.attr('stroke-opacity', .55);
    document.querySelectorAll('.cl-item').forEach(e => e.style.opacity = '1');
  } else {
    activeCat = cat;
    nodeSel.select('circle').attr('opacity', d => d._basecat === cat ? 1 : .2);
    linkSel.attr('stroke-opacity', l =>
      (l.source._basecat === cat || l.target._basecat === cat) ? .8 : .08);
    document.querySelectorAll('.cl-item').forEach(e =>
      e.style.opacity = e.querySelector('.cl-dot').style.background === CAT_COLORS[cat] ? '1' : '.35');
  }
}

// ── stats ─────────────────────────────────────────────────────────────────────
document.getElementById('stats').textContent =
  `${simNodes.length} datasets · ${simEdges.length} edges`;

// ── utility ───────────────────────────────────────────────────────────────────
function escHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// initial zoom-to-fit after simulation settles
sim.on('end', () => {
  const xs = simNodes.map(n => n.x), ys = simNodes.map(n => n.y);
  const xMin=Math.min(...xs),xMax=Math.max(...xs),yMin=Math.min(...ys),yMax=Math.max(...ys);
  const pad=60, gw=xMax-xMin+pad*2, gh=yMax-yMin+pad*2;
  const s = Math.min(W()/gw, H()/gh, 1);
  const tx = (W()-s*gw)/2-s*(xMin-pad);
  const ty = (H()-s*gh)/2-s*(yMin-pad);
  svg.transition().duration(900)
     .call(zoom.transform, d3.zoomIdentity.translate(tx,ty).scale(s));
});
</script>
</body>
</html>"""

if __name__ == "__main__":
    main()
