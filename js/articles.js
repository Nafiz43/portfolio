// Publications come from data/publications.json, built nightly by tools/sync_publications.py
// (curated entries in data/publications.manual.json + new ORCID works). Edit the manual file, not this one.
document.addEventListener("DOMContentLoaded", function () {
  const researchSection = document.getElementById("research-container");
  fetch("data/publications.json", { cache: "no-cache" })
    .then(r => r.json())
    .then(articles => {
      // Newest first, grouped by year; "TBD" (under review) sits on top. The JSON is already sorted.
      const groupOf = a => /^\d{4}$/.test(a.year) ? a.year : "Under Review";
      // Map keeps insertion order (a plain object would sort the year keys ascending).
      const groups = new Map();
      articles.forEach(a => groups.set(groupOf(a), [...(groups.get(groupOf(a)) || []), a]));
      const item = a => `
            <li>
              <a class="pub-title" href="${a.link}" target="_blank" rel="noopener">${a.title}</a>${a.award ? ` <span class="pub-award">🏆 ${a.award}</span>` : ""}
              <div class="pub-authors">${a.authors}</div>
              ${a.venue ? `<div class="pub-venue">${a.venue}</div>` : ""}
              ${a.description ? `<details><summary>Abstract</summary><p>${a.description}</p></details>` : ""}
            </li>`;
      // Selected papers (flagged "selected" in the manual file) on top; the full year-by-year list folds below.
      const all = [...groups].map(([g, items]) => `
        <h3 class="pub-year">${g}</h3>
        <ol class="pub-list">${items.map(item).join("")}</ol>`).join("");
      researchSection.innerHTML = `
        <h3 class="pub-year">Selected</h3>
        <ol class="pub-list">${articles.filter(a => a.selected).map(item).join("")}</ol>
        <details class="pub-all"><summary>Show all ${articles.length} publications</summary>${all}</details>`;
    })
    .catch(() => {
      researchSection.innerHTML = `<p>See the full list on <a href="https://scholar.google.com/citations?user=UDxK99QAAAAJ&hl=en" target="_blank">Google Scholar</a>.</p>`;
    });
});
