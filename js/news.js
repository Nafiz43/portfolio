// All news since 2020. d = "YYYY-MM", or "YYYY" when the month is not known.
// The home page shows the newest 5 (data-limit on #news-list); news.html shows all.
(function () {
  const a = (text, href) => `<a href="${href}" target="_blank" rel="noopener">${text}</a>`;
  const news = [
    { d: "2026-07", t: `${a("OSS sustainability modeling", "https://doi.org/10.1016/j.jss.2026.112985")} paper published in <b>JSS</b>.` },
    { d: "2026-10", t: `Presented <a href="medvision/">MedVision</a> at the UCD Radiology Research Symposium.` },
    { d: "2026-08", t: `${a("RepoWise", "https://link.springer.com/chapter/10.1007/978-3-032-39763-8_16")} won the <b>Best Paper Award</b> at SEET (Springer CCIS).` },
    { d: "2026-06", t: `Started an AI internship at ${a("BetterHelp", "https://www.betterhelp.com/")} on reducing LLM bias.` },
    { d: "2026-05", t: `${a("AI for case logging", "https://doi.org/10.1093/jamiaopen/ooag067")} paper published in <b>JAMIA Open</b>.` },
    { d: "2026-03", t: `Became <b>Associate Lab Manager</b> at the ${a("UCD CS AI4H Initiative", "https://ai4h.cs.ucdavis.edu/")}.` },
    { d: "2026-02", t: `${a("LLMs for OSS sustainability actions", "https://arxiv.org/abs/2602.11746")} preprint on arXiv.` },
    { d: "2026-02", t: `${a("MammoWise", "https://arxiv.org/abs/2602.22462")} (local RAG for mammography reports) preprint on arXiv.` },
    { d: "2026", t: `${a("Defining OSS sustainability", "https://doi.org/10.2139/ssrn.6450770")} preprint on SSRN.` },
    { d: "2026", t: `${a("Open LLMs for technical Q&amp;A", "https://link.springer.com/chapter/10.1007/978-3-032-08977-9_41")} paper published at SEET (Springer).` },
    { d: "2025-11", t: `${a("OSSPREY", "https://ieeexplore.ieee.org/abstract/document/11334666")} published at the <b>ASE 2025</b> Tool Demo track.` },
    { d: "2025-07", t: `Joined ${a("Scale AI", "https://scale.com/")} as a GenAI Human Frontier Collective Specialist.` },
    { d: "2025-07", t: `Advanced to <b>PhD candidacy</b> at UCD.` },
    { d: "2025-07", t: `Received my MS in CS from UCD (CGPA 3.91/4.00).` },
    { d: "2025-06", t: `Filed a <b>US patent</b> on AI-driven evidence-based action with Prof. Filkov.` },
    { d: "2025-06", t: `${a("EvidenceBot", "https://dl.acm.org/doi/10.1145/3696630.3728607")} published at the <b>FSE 2025</b> Tool Demo track.` },
    { d: "2025-05", t: `Presented ${a("AI case log automation", "https://amia.secure-platform.com/cic/gallery/rounds/82015/details/17117")} at AMIA CIC 2025.` },
    { d: "2025-01", t: `TA for ECS 260 (Software Engineering) at UCD.` },
    { d: "2025", t: `Selected as a ${a("<b>Leaders for the Future</b> Fellow", "https://innovate.ucdavis.edu/people/nafiz-imtiaz-khan")} (2025-26) at UCD.` },
    { d: "2025", t: `Received the UCD ${a("Graduate Student Travel Award", "https://grad.ucdavis.edu/travel-awards")}.` },
    { d: "2024-10", t: `Volunteer Co-Chair and Session Chair at <b>ASE 2024</b>.` },
    { d: "2024-10", t: `Students' ${a("TWIN elder-care robot", "https://doi.org/10.1145/3723178.3723221")} paper published at ICCA 2024 (ACM).` },
    { d: "2024-07", t: `${a("Evidence-based OSS sustainability advice", "https://dl.acm.org/doi/abs/10.1145/3663529.3663777")} paper published at <b>FSE 2024</b>.` },
    { d: "2024-07", t: `${a("Social media group recommendation", "https://doi.org/10.1007/s42979-024-03055-1")} paper published in SN CS (Springer).` },
    { d: "2024-06", t: `Received the GGCS Summer PhD Fellowship at UCD.` },
    { d: "2024-04", t: `TA for ECS 122A (Algorithm Design and Analysis) at UCD.` },
    { d: "2024-04", t: `Students' ${a("federated learning cervical cancer", "https://doi.org/10.1016/j.imu.2024.101496")} paper published in IMU (Elsevier).` },
    { d: "2024-01", t: `Students' ${a("handwriting system for the blind", "https://doi.org/10.1109/ACCESS.2024.3353781")} paper published in IEEE Access.` },
    { d: "2023-11", t: `Students' ${a("blockchain apparel supply chain", "https://doi.org/10.1109/wiecon-ece60392.2023.10456466")} paper published at IEEE WIECON-ECE.` },
    { d: "2023-10", t: `Students' ${a("RNN infant cry detection", "https://doi.org/10.1109/r10-htc57504.2023.10461731")} paper published at IEEE R10-HTC 2023.` },
    { d: "2023-09", t: `Started my PhD in CS at UC Davis, advised by Prof. Vladimir Filkov.` },
    { d: "2023-04", t: `${a("UI for low-literacy users", "https://doi.org/10.1177/21582440231172741")} systematic review published in SAGE Open.` },
    { d: "2023", t: `Program Committee member, CVR 2023.` },
    { d: "2022-12", t: `Students' ${a("voice-guided alphabet writing", "https://doi.org/10.1109/iccit57492.2022.10055542")} paper published at ICCIT 2022.` },
    { d: "2022-10", t: `Students' ${a("EEG stress classification", "https://link.springer.com/chapter/10.1007/978-981-19-2445-3_42")} paper published at IC4IR 2021 (Springer).` },
    { d: "2022-10", t: `${a("Wearables for COVID-19 quarantine", "https://link.springer.com/chapter/10.1007/978-3-031-10031-4_10")} book chapter published (Springer).` },
    { d: "2022-09", t: `${a("Global COVID-19 tweet sentiment", "https://onlinelibrary.wiley.com/doi/full/10.1002/eng2.12572")} paper published in Eng. Reports (Wiley).` },
    { d: "2022-07", t: `Joined MIST CACR as a Software Engineer, alongside my lecturer role.` },
    { d: "2022-05", t: `Students' ${a("intoxication detection app", "https://link.springer.com/chapter/10.1007/978-981-19-0332-8_15")} paper published at IJCACI 2021.` },
    { d: "2022-04", t: `${a("ML for pregnancy outcomes", "https://bmcpregnancychildbirth.biomedcentral.com/articles/10.1186/s12884-022-04594-2")} systematic review published in BMC P&amp;C.` },
    { d: "2022-04", t: `Students' ${a("acoustic VR ethics game", "https://ieeexplore.ieee.org/abstract/document/9824116")} paper published at IEEE I2CT 2022.` },
    { d: "2022-03", t: `${a("UVC-PURGE", "https://ieeexplore.ieee.org/abstract/document/9745041")} disinfection robot paper published in IEEE Access.` },
    { d: "2022", t: `${a("ML bolted connection failure modes", "https://www.sciencedirect.com/science/article/abs/pii/S1350630722004459")} paper published in EFA (Elsevier).` },
    { d: "2022", t: `Received the Top Downloaded Article Award, Eng. Reports (Wiley).` },
    { d: "2022", t: `CTO for the AFMC, BEPZA and ICMAB exams and elections.` },
    { d: "2022", t: `Program Committee member, IEEE AIC 2022.` },
    { d: "2021-12", t: `Students' ${a("ML cyberbullying detection", "https://ieeexplore.ieee.org/abstract/document/9768450")} paper published at IC4ME2 2021.` },
    { d: "2021-12", t: `Students' ${a("forged signature detection", "https://ieeexplore.ieee.org/abstract/document/9768440")} paper published at IC4ME2 2021.` },
    { d: "2021-11", t: `${a("ML bolted connection capacity", "https://www.sciencedirect.com/science/article/abs/pii/S014102962101600X")} paper published in <b>Eng. Structures</b>.` },
    { d: "2021-11", t: `${a("COVID-19 and black fungus perception", "https://onlinelibrary.wiley.com/doi/10.1002/eng2.12475")} paper in Eng. Reports (Wiley).` },
    { d: "2021-11", t: `${a("Athlete exercise monitoring", "https://dl.acm.org/doi/abs/10.1145/3487664.3487725")} paper published at iiWAS 2021.` },
    { d: "2021-11", t: `Students' ${a("ML support against abuse of women", "https://ieeexplore.ieee.org/document/9667924")} paper published at ICEEICT 2021.` },
    { d: "2021-11", t: `${a("Android malware prediction", "https://link.springer.com/chapter/10.1007/978-3-030-90016-8_2")} paper published at iCETiC 2021.` },
    { d: "2021-10", t: `${a("Bangladesh COVID-19 tweet sentiment", "https://ieeexplore.ieee.org/document/9615331")} paper published at ITMS 2021.` },
    { d: "2021-08", t: `${a("VGG-SCNet", "https://ieeexplore.ieee.org/abstract/document/9515947")} brain tumor MRI paper published in <b>IEEE Access</b>.` },
    { d: "2021-04", t: `${a("SFRC beam shear strength ML", "https://www.sciencedirect.com/science/article/abs/pii/S0141029620343443")} paper published in <b>Eng. Structures</b>.` },
    { d: "2021-03", t: `Joined MIST CSE as a <b>Lecturer</b>.` },
    { d: "2021-02", t: `Graduated with a BSc in CSE from MIST.` },
    { d: "2021-02", t: `${a("Breast cancer feature selection", "https://link.springer.com/chapter/10.1007/978-3-030-68154-8_48")} paper published at ICO 2021.` },
    { d: "2021", t: `Received the Top Downloaded Article Award, Eng. Reports (Wiley).` },
    { d: "2021", t: `CTO for the AFMC Admission Test.` },
    { d: "2020-12", t: `Thesis paper 2, ${a("childbirth mode prediction", "https://ieeexplore.ieee.org/abstract/document/9296752")}, published in <b>IEEE Access</b>.` },
    { d: "2020-12", t: `${a("Serious game emotion measures", "https://link.springer.com/chapter/10.1007/978-3-030-71187-0_96")} paper published at ISDA 2020.` },
    { d: "2020-12", t: `${a("Fingerprint attendance system", "https://ieeexplore.ieee.org/document/9350882")} paper published at ETCCE 2020.` },
    { d: "2020-11", t: `Thesis paper 1, ${a("cesarean childbirth prediction", "https://dl.acm.org/doi/10.1145/3428757.3429138")}, published at iiWAS 2020.` },
    { d: "2020", t: `UVC-PURGE won the Imperial College London Medical Robotics Challenge.` },
    { d: "2020", t: `3rd Runner-up, IEEE Bangladesh COVID-19 Combatants Competition.` },
    { d: "2020", t: `MIST Blood Bank app won the Tri Robo Cup Creative App Contest.` },
    { d: "2020", t: `MIST Dean's List of Honor for the third year (2018-2020).` },
  ];

  const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const label = d => d.length > 4 ? `${MONTHS[+d.slice(5) - 1]} ${d.slice(0, 4)}` : d;
  // Newest first; a year-only item sorts after the dated items of its year ("2026" < "2026-01").
  news.sort((x, y) => y.d.localeCompare(x.d));

  document.addEventListener("DOMContentLoaded", () => {
    const list = document.getElementById("news-list");
    if (!list) return;
    const limit = +list.dataset.limit || news.length;
    const grouped = list.dataset.group === "year";
    let year = "";
    list.innerHTML = news.slice(0, limit).map(n => {
      const head = grouped && n.d.slice(0, 4) !== year ? `<li class="news-year"><h4>${year = n.d.slice(0, 4)}</h4></li>` : "";
      return `${head}<li><span class="news-date">${label(n.d)}</span> ${n.t}</li>`;
    }).join("");
  });
})();
