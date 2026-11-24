// Research tools shown as cards in the Projects section (after Publications). Newest first.
// The old MIST projects that were here are in git history (before 2026-11-23).
document.addEventListener("DOMContentLoaded", function () {
  const projects = [
    {
      title: "MedVision",
      image: "img/projects/medvision.jpg",
      venue: "UC Davis Radiology Research Symposium 2026",
      description: "Ask a hospital imaging archive questions in words, with an image, or both. It runs on premises inside the hospital network.",
      links: { Page: "medvision/" }
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
        Demo: "https://repowise.netlify.app"
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
    }
  ];

  const container = document.getElementById("project-container");
  if (!container) return;
  container.innerHTML = projects.map(p => `
    <div class="project-card">
      <a href="${p.links.Page}" target="_blank" rel="noopener"><img src="${p.image}" alt="${p.title} screenshot" loading="lazy" decoding="async"></a>
      <div class="project-body">
        <h3>${p.title}</h3>
        <div class="project-venue">${p.venue}${p.award ? ` <span class="pub-award">🏆 ${p.award}</span>` : ""}</div>
        <p>${p.description}</p>
        <div class="project-links">${Object.entries(p.links).map(([k, u]) => `<a href="${u}" target="_blank" rel="noopener">${k}</a>`).join(" · ")}</div>
      </div>
    </div>`).join("");
});
