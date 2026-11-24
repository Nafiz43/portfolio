// All news since 2020. d = "YYYY-MM", or "YYYY" when the month is not known.
// The home page shows the newest 5 (data-limit on #news-list); news.html shows all.
(function () {
  const a = (text, href) => `<a href="${href}" target="_blank" rel="noopener">${text}</a>`;
  const news = [
    { d: "2026-07", t: `Paper ${a("Multi-Ecosystem Modeling of OSS Project Sustainability", "https://doi.org/10.1016/j.jss.2026.112985")} published in the <b>Journal of Systems and Software (JSS)</b>.` },
    { d: "2026-10", t: `Presented <a href="medvision/">MedVision</a> at the UC Davis Radiology Research Symposium.` },
    { d: "2026-08", t: `${a("RepoWise", "https://link.springer.com/chapter/10.1007/978-3-032-39763-8_16")} won the <b>Best Paper Award</b> at SEET (Springer CCIS).` },
    { d: "2026-06", t: `Started a summer internship at ${a("BetterHelp", "https://www.betterhelp.com/")}, working on reducing bias in language models.` },
    { d: "2026-05", t: `Paper ${a("Intelligent Documentation in Medical Education: Can AI Replace Manual Case Logging?", "https://doi.org/10.1093/jamiaopen/ooag067")} published in <b>JAMIA Open</b>.` },
    { d: "2026-03", t: `Became <b>Associate Lab Manager</b> at the ${a("UC Davis CS AI for Health Initiative", "https://ai4h.cs.ucdavis.edu/")}.` },
    { d: "2026-02", t: `Preprint ${a("Leveraging Language Models to Discover Evidence-Based Actions for OSS Sustainability", "https://arxiv.org/abs/2602.11746")} is out on arXiv.` },
    { d: "2026-02", t: `Preprint ${a("MammoWise: Multi-Model Local RAG Pipeline for Mammography Report Generation", "https://arxiv.org/abs/2602.22462")} is out on arXiv.` },
    { d: "2026", t: `Preprint ${a("Open-Source Software Sustainability: Defining and Measuring a Multifaceted Concept", "https://doi.org/10.2139/ssrn.6450770")} is out on SSRN.` },
    { d: "2026", t: `Paper ${a("Open-Source LLMs for Technical Q&amp;A: Lessons from StackExchange", "https://link.springer.com/chapter/10.1007/978-3-032-08977-9_41")} published at SEET (Springer).` },
    { d: "2025-11", t: `Paper ${a("OSSPREY: AI-Driven Forecasting and Intervention for OSS Project Sustainability", "https://ieeexplore.ieee.org/abstract/document/11334666")} published at the <b>ASE 2025</b> Tool Demonstrations track.` },
    { d: "2025-07", t: `Joined ${a("Scale AI", "https://scale.com/")} as a Human Frontier Collective Specialist (GenAI).` },
    { d: "2025-07", t: `Advanced to <b>PhD candidacy</b> at UC Davis.` },
    { d: "2025-07", t: `Received my MS in Computer Science from UC Davis (CGPA 3.91/4.00).` },
    { d: "2025-06", t: `Filed a <b>US patent</b> with Prof. Vladimir Filkov: "Systems and Methods for Artificial Intelligence-Driven Evidence-Based Action".` },
    { d: "2025-06", t: `Paper ${a("EvidenceBot: A Privacy-Preserving, Customizable RAG-Based Tool for Enhancing Large Language Model Interactions", "https://dl.acm.org/doi/10.1145/3696630.3728607")} published at the <b>FSE 2025</b> Tool Demonstrations track.` },
    { d: "2025-05", t: `Presented ${a("AI-Driven Automation of Procedural Case Log Documentation", "https://amia.secure-platform.com/cic/gallery/rounds/82015/details/17117")} at the AMIA 2025 Clinical Informatics Conference.` },
    { d: "2025-01", t: `Teaching Assistant for ECS 260 (Software Engineering) at UC Davis, Winter 2025.` },
    { d: "2025", t: `Selected as a ${a("<b>Leaders for the Future</b> Fellow", "https://innovate.ucdavis.edu/people/nafiz-imtiaz-khan")} (2025-2026) at the UC Davis Mike and Renée Child Institute for Innovation and Entrepreneurship.` },
    { d: "2025", t: `Received the UC Davis ${a("Graduate Student Travel Award", "https://grad.ucdavis.edu/travel-awards")}.` },
    { d: "2024-10", t: `Served as Volunteer Co-Chair and Session Chair at the 39th IEEE/ACM International Conference on Automated Software Engineering (<b>ASE 2024</b>).` },
    { d: "2024-10", t: `Paper by my students, ${a("AI Integrated Entertaining and Monitoring System for Daily Care of Elders", "https://doi.org/10.1145/3723178.3723221")} (the TWIN companion robot), published at ICCA 2024 (ACM).` },
    { d: "2024-07", t: `Paper ${a("From Models to Practice: Enhancing OSS Project Sustainability with Evidence-Based Advice", "https://dl.acm.org/doi/abs/10.1145/3663529.3663777")} published at <b>FSE 2024</b>.` },
    { d: "2024-07", t: `Paper ${a("Behavior Based Group Recommendation from Social Media Dataset by Using Deep Learning and Topic Modeling", "https://doi.org/10.1007/s42979-024-03055-1")} published in SN Computer Science (Springer).` },
    { d: "2024-06", t: `Received the GGCS Summer PhD Fellowship from the Graduate Group in Computer Science, UC Davis.` },
    { d: "2024-04", t: `Teaching Assistant for ECS 122A (Algorithm Design and Analysis) at UC Davis, Spring 2024.` },
    { d: "2024-04", t: `Paper by my students, ${a("A federated learning aided system for classifying cervical cancer using PAP-SMEAR images", "https://doi.org/10.1016/j.imu.2024.101496")}, published in Informatics in Medicine Unlocked (Elsevier).` },
    { d: "2024-01", t: `Paper by my students, ${a("A Multilingual Handwriting Learning System for Visually Impaired People", "https://doi.org/10.1109/ACCESS.2024.3353781")}, published in IEEE Access.` },
    { d: "2023-11", t: `Paper by my students, ${a("A Blockchain-based Framework to Develop a Sustainable Supply Chain Management System for Apparel Industry", "https://doi.org/10.1109/wiecon-ece60392.2023.10456466")}, published at IEEE WIECON-ECE 2023.` },
    { d: "2023-10", t: `Paper by my students, ${a("Proposing Novel Recurrent Neural Network Architectures for Infant Cry Detection in Domestic Context", "https://doi.org/10.1109/r10-htc57504.2023.10461731")}, published at IEEE R10-HTC 2023.` },
    { d: "2023-09", t: `Moved to Davis, California to start my PhD in Computer Science at the University of California, Davis, advised by Prof. Vladimir Filkov.` },
    { d: "2023-04", t: `Systematic review ${a("Designing User Interfaces for Illiterate and Semi-Literate Users: A Systematic Review and Future Research Agenda", "https://doi.org/10.1177/21582440231172741")} published in SAGE Open.` },
    { d: "2023", t: `Served on the Program Committee of the 3rd International Conference on Computer Vision &amp; Robotics (CVR 2023).` },
    { d: "2022-12", t: `Paper by my students, ${a("Towards Developing a Voice-Over-Guided System for Visually Impaired People to Learn Writing the Alphabets", "https://doi.org/10.1109/iccit57492.2022.10055542")}, published at ICCIT 2022.` },
    { d: "2022-10", t: `Paper by my students, ${a("Neurophysiological Feature Based Stress Classification Using Unsupervised Machine Learning Technique", "https://link.springer.com/chapter/10.1007/978-981-19-2445-3_42")}, published at IC4IR 2021 (Springer).` },
    { d: "2022-10", t: `Book chapter ${a("Monitoring the Health and Movement of Quarantined COVID-19 Patients with Wearable Devices", "https://link.springer.com/chapter/10.1007/978-3-031-10031-4_10")} published in Healthcare Technology Solutions for Pandemics (Springer).` },
    { d: "2022-09", t: `Paper ${a("Leveraging machine learning to analyze sentiment from COVID-19 tweets: A global perspective", "https://onlinelibrary.wiley.com/doi/full/10.1002/eng2.12572")} published in Engineering Reports (Wiley).` },
    { d: "2022-07", t: `Joined the Center for Advanced Computing Research (CACR) at MIST as a Software Engineer, alongside my lecturer role.` },
    { d: "2022-05", t: `Paper by my students, ${a("Towards Developing a Mobile Application for Detecting Intoxicated People through Interactive UIs", "https://link.springer.com/chapter/10.1007/978-981-19-0332-8_15")}, published at IJCACI 2021.` },
    { d: "2022-04", t: `Third paper from my undergraduate thesis, the systematic review ${a("Machine learning to predict pregnancy outcomes: a systematic review, synthesizing framework and future research agenda", "https://bmcpregnancychildbirth.biomedcentral.com/articles/10.1186/s12884-022-04594-2")}, published in BMC Pregnancy and Childbirth.` },
    { d: "2022-04", t: `Paper by my students, ${a("Exploring Design Attributes and Development of an Acoustic VR Game to Improve Ethical Values of Visually Impaired People", "https://ieeexplore.ieee.org/abstract/document/9824116")}, published at IEEE I2CT 2022.` },
    { d: "2022-03", t: `Paper ${a("UVC-PURGE: A Novel Cost-Effective Disinfection Robot for Combating COVID-19 Pandemic", "https://ieeexplore.ieee.org/abstract/document/9745041")} published in IEEE Access. This is the robot that won the Imperial College London challenge.` },
    { d: "2022", t: `Paper ${a("Machine Learning-Based Failure Mode Identification of Double Shear Bolted Connections in Structural Steel", "https://www.sciencedirect.com/science/article/abs/pii/S1350630722004459")} published in Engineering Failure Analysis (Elsevier).` },
    { d: "2022", t: `Received the Top Downloaded Article Award from Engineering Reports (Wiley).` },
    { d: "2022", t: `Served as Chief Technical Officer for the AFMC Admission Test, BEPZA Recruitment Exam and ICMAB 18th Council Election.` },
    { d: "2022", t: `Served on the Program Committee of the 2022 IEEE World Conference on Applied Intelligence and Computing (AIC 2022).` },
    { d: "2021-12", t: `Paper by my students, ${a("A Framework to Detect and Prevent Cyberbullying from Social Media by Exploring Machine Learning Algorithms", "https://ieeexplore.ieee.org/abstract/document/9768450")}, published at IC4ME2 2021.` },
    { d: "2021-12", t: `Paper by my students, ${a("An Efficient Transfer Learning Model for Predicting Forged (Handwritten) Signature", "https://ieeexplore.ieee.org/abstract/document/9768440")}, published at IC4ME2 2021.` },
    { d: "2021-11", t: `Paper ${a("Predicting Bearing Capacity of Double Shear Bolted Connections Using Machine Learning", "https://www.sciencedirect.com/science/article/abs/pii/S014102962101600X")} published in <b>Engineering Structures</b> (Elsevier).` },
    { d: "2021-11", t: `Paper ${a("COVID-19 and Black Fungus: Analysis of Public Perceptions through Machine Learning", "https://onlinelibrary.wiley.com/doi/10.1002/eng2.12475")} published in Engineering Reports (Wiley).` },
    { d: "2021-11", t: `Paper ${a("Design, Development and Evaluation of a Physical Exercise Monitoring and Managing System for Athletes", "https://dl.acm.org/doi/abs/10.1145/3487664.3487725")} published at iiWAS 2021.` },
    { d: "2021-11", t: `Paper by my students, ${a("Developing a Machine Learning Based Support System for Mitigating the Suppression Against Women and Children", "https://ieeexplore.ieee.org/document/9667924")}, published at ICEEICT 2021.` },
    { d: "2021-11", t: `Paper ${a("Prediction of Android Malicious Software using Boosting Algorithms", "https://link.springer.com/chapter/10.1007/978-3-030-90016-8_2")} published at iCETiC 2021.` },
    { d: "2021-10", t: `Paper ${a("Sentiment Analysis of Bangladesh-specific COVID-19 Tweets using Deep Neural Network", "https://ieeexplore.ieee.org/document/9615331")} published at ITMS 2021.` },
    { d: "2021-08", t: `Paper ${a("VGG-SCNet: A VGG Net-Based Deep Learning Framework for Brain Tumor Detection on MRI Images", "https://ieeexplore.ieee.org/abstract/document/9515947")} published in <b>IEEE Access</b>.` },
    { d: "2021-04", t: `Paper ${a("Data-driven shear strength prediction of steel fiber reinforced concrete beams using machine learning approach", "https://www.sciencedirect.com/science/article/abs/pii/S0141029620343443")} published in <b>Engineering Structures</b> (Elsevier).` },
    { d: "2021-03", t: `Joined the Department of CSE at the Military Institute of Science and Technology (MIST) as a <b>Lecturer</b>.` },
    { d: "2021-02", t: `Graduated with a BSc in Computer Science and Engineering from the Military Institute of Science and Technology (MIST).` },
    { d: "2021-02", t: `Paper ${a("Exploring the Machine Learning Algorithms to Find the Best Features for Predicting the Breast Cancer and its Recurrence", "https://link.springer.com/chapter/10.1007/978-3-030-68154-8_48")} published at ICO 2021.` },
    { d: "2021", t: `Received the Top Downloaded Article Award from Engineering Reports (Wiley).` },
    { d: "2021", t: `Served as Chief Technical Officer for the AFMC Admission Test.` },
    { d: "2020-12", t: `Second paper from my undergraduate thesis, ${a("Exploring machine learning algorithms to find the best features for predicting modes of childbirth", "https://ieeexplore.ieee.org/abstract/document/9296752")}, published in <b>IEEE Access</b>.` },
    { d: "2020-12", t: `Paper ${a("Evaluation of User's Emotional Experience through Neurological and Physiological Measures in Playing Serious Games", "https://link.springer.com/chapter/10.1007/978-3-030-71187-0_96")} published at ISDA 2020.` },
    { d: "2020-12", t: `Paper ${a("Towards Developing an Automated Attendance Management System using Fingerprint Sensor", "https://ieeexplore.ieee.org/document/9350882")} published at ETCCE 2020.` },
    { d: "2020-11", t: `First paper from my undergraduate thesis, ${a("Prediction of Cesarean Childbirth using Ensemble Machine Learning Methods", "https://dl.acm.org/doi/10.1145/3428757.3429138")}, published at iiWAS 2020.` },
    { d: "2020", t: `Our robot UVC-PURGE won the Medical Robotics Challenge for Contagious Diseases, organized by Imperial College London.` },
    { d: "2020", t: `Our team won 3rd Runner-up at the COVID-19 Combatants Unification Competition by the IEEE Bangladesh Chapter.` },
    { d: "2020", t: `Our MIST Blood Bank app won the Creative App Contest at the Tri Robo Cup Championship (MIST Robotics Club).` },
    { d: "2020", t: `Named to the MIST Dean's List of Honor for the third year (2018, 2019, 2020).` },
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
