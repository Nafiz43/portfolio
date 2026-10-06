
  document.addEventListener("DOMContentLoaded", function () {
    const roles = [
      {
        year: "2024",
        title: "Volunteer Co-Chair",
        link: "https://conf.researchr.org/committee/ase-2024/ase-2024-student-volunteers-program-committee",
        venue: "ASE-2024",
        venueLink: "https://conf.researchr.org/home/ase-2024"
      },
      {
        year: "2024",
        title: "Session Chair: SE for AI",
        link: "https://conf.researchr.org/track/ase-2024/ase-2024-research?",
        venue: "ASE-2024",
        venueLink: "https://conf.researchr.org/home/ase-2024"
      },
      {
        year: "2024",
        title: "Session Chair: Smart Contract & BlockChain",
        link: "https://conf.researchr.org/track/ase-2024/ase-2024-research?",
        venue: "ASE-2024",
        venueLink: "https://conf.researchr.org/home/ase-2024"
      },
      {
        year: "2023",
        title: "Reviewer",
        venue: "SAGE Open, CHI 2023, Academia Oncology, Deep Science Publishing"
      },
      {
        year: "2022",
        title: "Program Committee Member and Reviewer",
        venue: "IEEE World Conference on Applied Intelligence and Computing (AIC) 2022",
        venueLink: "https://aic2022.scrs.in/"
      },
      {
        year: "2022",
        title: "Chief Technical Officer",
        venue: "AFMC Admission Test - 2021 & 2022, BEPZA Recruitment Exam - 2022"
      },
      {
        year: "2021",
        title: "Event Coordinator",
        venue: "Mobile App Contest, MIST Inter-University ICT Innovation Fest 2021"
      },
      {
        year: "2021",
        title: "Technical Member",
        venue: "MIST Inter-University ICT Innovation Fest 2021"
      }
    ];

    const listContainer = document.getElementById("activity-list");
    roles.sort((a, b) => b.year.localeCompare(a.year));
    roles.forEach(role => {
      const listItem = document.createElement("li");
      listItem.innerHTML = `
        ${role.link ? `<a href="${role.link}" target="_blank">${role.title}</a>,` : `${role.title},`}
        ${role.venueLink ? `<a href="${role.venueLink}" target="_blank">${role.venue}</a>` : role.venue}
        <span class="item-year">${role.year}</span>
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