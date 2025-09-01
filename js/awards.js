  document.addEventListener("DOMContentLoaded", function () {
    const awards = [
      {
        title: "Champion in the application category of the ",
        event: "Medical Robotics Challenge for Contagious Diseases",
        eventLink: "https://www.hamlynsymposium.org/challenges/medical-robotics-for-contagious-diseases/",
        organizer: "Imperial College London",
        organizerLink: "https://www.imperial.ac.uk/",
        ref: "[REF]",
        refLink: "https://mist.ac.bd/department/cse/announcement/193/team_uvc_purge_conquered_international_medical_robotics_challege"
      },
      {
        title: "<a href=\"https://innovate.ucdavis.edu/leaders-future\" target=\"_blank\">Leaders for the Future</a> Fellowship, 2025-2026"
      },
      {
        title: "<a href=\"https://grad.ucdavis.edu/travel-awards\" target=\"_blank\">Graduate Student Travel Award</a>, 2025"
      },
      {
        title: "Champion in the creative app contest of the ",
        event: "Tri Robo Cup",
        eventLink: "",
        organizer: "MIST Robotics Club",
        organizerLink: "https://mist.ac.bd/page/robotics-club",
        ref: "[REF]",
        refLink: "https://drive.google.com/file/d/1fWp9PXR1GYYmgZY76oHXcJ-EOUPXFaop/view?usp=sharing"
      },
      {
        title: "Top Downloaded Article Award - 2020, issued by ",
        event: "Engineering Reports",
        eventLink: "",
        ref: "[REF]",
        refLink: "https://drive.google.com/file/d/15FRjKlYTPpc7f4MiKO8ry2pez2X-cZ5P/view?usp=sharing"
      },
      {
        title: "Top Downloaded Article Award - 2021, issued by ",
        event: "Engineering Reports",
        eventLink: "",
        ref: "[REF]",
        refLink: "https://drive.google.com/file/d/1vzAHdLtPQgW8uY1vK2QUrCbUdfOwiO42/view?usp=sharing"
      },
      {
        title: "MIST Dean's List Award - Three Consecutive Academic Years"
      },
      {
        title: "MIST Merit Scholarship - Six Academic Semesters"
      },
      {
        title: "GGCS Summer Ph.D Fellowship - 2024"
      }
    ];

    const awardsContainer = document.getElementById("awards-list");

    awards.forEach(award => {
      const awardItem = document.createElement("li");

      awardItem.innerHTML = `
        <i class="fa fa-tasks" aria-hidden="true"></i>
        ${award.title}
        ${award.event ? `<a href="${award.eventLink}" target="_blank">${award.event}</a>` : ""}
        ${award.organizer ? `, organized by <a href="${award.organizerLink}" target="_blank">${award.organizer}</a>` : ""}
        ${award.ref ? `<a href="${award.refLink}" target="_blank">${award.ref}</a>` : ""}
      `;

      awardsContainer.appendChild(awardItem);
    });
  });
