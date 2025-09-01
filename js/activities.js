
  document.addEventListener("DOMContentLoaded", function () {
    const roles = [
      {
        title: "Volunteer Co-Chair",
        link: "https://conf.researchr.org/committee/ase-2024/ase-2024-student-volunteers-program-committee",
        venue: "ASE-2024",
        venueLink: "https://conf.researchr.org/home/ase-2024"
      },
      {
        title: "Session Chair: SE for AI",
        link: "https://conf.researchr.org/track/ase-2024/ase-2024-research?",
        venue: "ASE-2024",
        venueLink: "https://conf.researchr.org/home/ase-2024"
      },
      {
        title: "Session Chair: Smart Contract & BlockChain",
        link: "https://conf.researchr.org/track/ase-2024/ase-2024-research?",
        venue: "ASE-2024",
        venueLink: "https://conf.researchr.org/home/ase-2024"
      },
      {
        title: "Reviewer",
        venue: "SAGE Open, CHI 2023, Academia Oncology, Deep Science Publishing"
      },
      {
        title: "Program Committee Member and Reviewer",
        venue: "IEEE World Conference on Applied Intelligence and Computing (AIC) 2022",
        venueLink: "https://aic2022.scrs.in/"
      },
      {
        title: "Chief Technical Officer",
        venue: "BEPZA Recruitment Exam - 2022",
        venueLink: "https://www.bepza.gov.bd/"
      },
      {
        title: "Chief Technical Officer",
        venue: "AFMC Admission Test - 2021",
        venueLink: "https://afmc.edu.bd/"
      },
      {
        title: "Event Coordinator",
        venue: "Mobile App Contest, MIST Inter-University ICT Innovation Fest 2021"
      },
      {
        title: "Technical Member",
        venue: "MIST Inter-University ICT Innovation Fest 2021"
      }
    ];

    const listContainer = document.getElementById("activity-list");

    roles.forEach(role => {
      const listItem = document.createElement("li");
      listItem.innerHTML = `
        <p>
          <i class="fa fa-tasks" aria-hidden="true"></i>
          ${role.link ? `<a href="${role.link}" target="_blank">${role.title}</a>,` : `${role.title},`}
          ${role.venueLink ? `<a href="${role.venueLink}" target="_blank">${role.venue}</a>` : role.venue}
        </p>
      `;
      listContainer.appendChild(listItem);
    });
  });



//   <!-- <li><p><i class="fa fa-tasks" aria-hidden="true"></i>
//   Participated in Intra MIST Programming and Gaming Competition 2018</a></p></li>
 
//  <li><p><i class="fa fa-tasks" aria-hidden="true"></i>
//   Participated in MIST CSE Fest Programming Contest 2018.</a></p></li>

  


//   <li><p><i class="fa fa-tasks" aria-hidden="true"></i>
//   Participated in MIST Inter-University Programming Contest (IUPC) 2019.</a></p></li> -->
//   <!-- https://conf.researchr.org/home/ase-2024 -->