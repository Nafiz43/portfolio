  document.addEventListener("DOMContentLoaded", function () {
    const experiences = [
      {
        title: "Human Frontier Collective Specialist – GenAI (Internship)",
        company: "Scale AI",
        companyLink: "https://scale.com/",
        logo: "https://media.licdn.com/dms/image/v2/D560BAQFLIeQFxapL7Q/company-logo_200_200/B56Za2650hGgAI-/0/1746825617004/scaleai_logo?e=1758153600&v=beta&t=ALCwhJxT6gX4JzkzeKojp4k5Vnf2LLLZyT7QTsU176M",
        date: "Aug 2025 – Sep 2025",
        width: 80,
        height: 80,
        tasks: [
          "Designed and critiqued complex, domain-specific problem sets to rigorously test cutting-edge generative AI models, identifying limitations and refining performance.",
          "Collaborated with Scale researchers in interdisciplinary sessions to analyze model behavior, shape AI research directions, and explore experimental applications."
        ]
      },
      {
        title: "Founding Engineer and Project Manager",
        company: "ELTA AI",
        companyLink: "https://www.elta.ai/",
        logo: "https://raw.githubusercontent.com/Nafiz43/portfolio/refs/heads/main/img/elta.png",
        date: "June 2025 – Present",
        width: 80,
        height: 80,
        tasks: [
          "Building ELTA AI safety and emergency planning app with Flutter, LLM-powered RAG checklists, agentic AI for real-time monitoring, and privacy-compliant emergency contact workflows."
        ]
      },
      {
        title: "Graduate Research Fellow",
        company: "UC Davis",
        companyLink: "https://www.ucdavis.edu/",
        logo: "img/ucd_logo.png",
        date: "September 2023 - Present",
        width: 80,
        height: 80,
        tasks: [
          "Spearheaded a team to develop the <a href='https://oss-prey.github.io/OSSPREY-Website/' target='_blank'>OSSPREY</a> tool to support sustainable open-source development by providing real-time project analytics, temporal AI-driven sustainability forecasts, and evidence-based recommendations using LLMs.",
          "Developed <a href='https://github.com/Nafiz43/ReACT-GPT'  target='_blank'>ReACT-GPT</a>, an <strong>LLM</strong>-powered framework utilizing <strong>LangChain</strong>, <strong>ChromaDB</strong>, and <strong>Ollama</strong> to synthesize actionable insights and key findings from scientific articles.",
          "Developed <a href='https://nafiz43.github.io/EvidenceBot/'><strong>EvidenceBot</strong></a>, an open-source application using <strong>Streamlit</strong> and the <strong>ReACT-GPT</strong> framework, enabling users to query and extract information from various documents effectively.",
          "Developed <a href='https://nafiz43.github.io/PCL-Fetcher/'><strong>PCL-Fetcher</strong></a>, a pipeline that automates the documentation of procedural case logs using LLMs. The system analyzes procedural reports by posing targeted questions and generating structured responses",
          "Developed <a href='https://github.com/Nafiz43/VLMs-for-Mammograms' target='_blank'>MammoGen-RAG</a>, a multi-modal RAG-based pipeline integrated with Vision-Language Models(VLMs) to automate the generation of mammography reports.",
          "Enhanced the performance of foundational language models (<strong>Llama</strong>, <strong>Mixtral</strong>) on targeted tasks through strategic fine-tuning techniques.",
          "Engineered and optimized various LSTM-based models (<strong>Dilated-LSTM</strong>, <strong>Bi-LSTM</strong>, <strong>Stacked-LSTM</strong>) to improve accuracy in forecasting the graduation status of <strong>Open Source Software (OSS)</strong> projects.",
          "Developed <a href='https://nafiz43.github.io/ReACTive/feature.html#section1' target='_blank'>ReACTive</a>, a visualization tool for ReACTs (Researched ACTionables) with <strong>Pyvis</strong> and <strong>Bootstrap</strong>",
        ]
      },
      {
        title: "Lecturer",
        company: "MIST",
        companyLink: "https://www.mist.ac.bd/",
        logo: "img/mist_logo.png",
        date: "March 2021 - August 2023",
        width: 80,
        height: 80,
        tasks: [
          "Instructed six theory courses (<strong>Data Structure</strong>, <strong>Software Engineering</strong>, <strong>Programming Language</strong>, <strong>Discrete Mathematics</strong>, etc.).",
          "Co-supervised <strong>ten undergraduate</strong> thesis teams, guiding students in their research and project development.",
          "Collaborated in <strong>25 ML-based</strong> research projects with students and faculty members."
        ]
      },
      {
        title: "Software Engineer",
        company: "CACR, MIST",
        companyLink: "https://www.mist.ac.bd/",
        logo: "img/mist_logo.png",
        date: "July 2022 - August 2023",
        width: 80,
        height: 80,
        tasks: [
          "Developed the <strong>AFMC Admission Test</strong> Module, a software solution for the AFMC Entrance exam.",
          "Spearheaded a team to develop <strong>C-Archive</strong> using <strong>PHP</strong>, <strong>MySQL</strong>, and <strong>Bootstrap</strong>.",
          "Developed a <strong>Digital Plot Distribution</strong> system in collaboration with <a href='https://rajuk.gov.bd/' target='_blank'>RAJUK</a>."
        ]
      },
      {
        title: "Software Engineer",
        company: "GuardForce Securities",
        logo: "img/guard_force.png",
        date: "August 2019 - February 2020",
        width: 140,
        height: 60,
        tasks: [
          "Designed and implemented an <strong>Employee Management System (EMS)</strong> using <strong>JavaFX</strong> and <strong>MySQL</strong> database with multiple levels of security authorizations, which is used to maintain over 3500 employees."
        ]
      }
    ];

    const experienceContainer = document.getElementById("experience-section");

    experiences.forEach(exp => {
      const experienceItem = document.createElement("div");
      experienceItem.classList.add("resume-item", "flex-column", "mb-5");
      
      experienceItem.innerHTML = `
        <div class="resume-content">
          <span>
            <a href="${exp.companyLink}" target="_blank">
              <img src="${exp.logo}" width="${exp.width}" height="${exp.height}" style="padding: 2px;" />
            </a>
            <b style="margin-left: 10px">
              <font size="+2" color="black">${exp.title}, <a href="${exp.companyLink}" target="_blank">${exp.company}</a></font>
            </b>
          </span>
        </div>
        <div class="resume-date text-md-right">
          <span class="text-primary">${exp.date}</span>
        </div>
        <div>
          <ul style="list-style-type: disc; padding-left: 60px;">
            ${exp.tasks.map(task => `<li>${task}</li>`).join("")}
          </ul>
        </div>
      `;

      experienceContainer.appendChild(experienceItem);
    });
  });
