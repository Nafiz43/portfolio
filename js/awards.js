  document.addEventListener("DOMContentLoaded", function () {
    const awards = [
      {
        year: "2026",
        title: "Best Paper Award, Software Engineering of Emerging Technologies (Springer CCIS), for <a href=\"https://link.springer.com/chapter/10.1007/978-3-032-39763-8_16\" target=\"_blank\">RepoWise</a>"
      },
      {
        year: "2020",
        title: "Champion in the application category of the ",
        event: "Medical Robotics Challenge for Contagious Diseases",
        eventLink: "https://www.hamlynsymposium.org/challenges/medical-robotics-for-contagious-diseases/",
        organizer: "Imperial College London",
        organizerLink: "https://www.imperial.ac.uk/",
        ref: "[REF]",
        refLink: "https://mist.ac.bd/department/cse/announcement/193/team_uvc_purge_conquered_international_medical_robotics_challege"
      },
      {
        year: "2025-2026",
        title: "<a href=\"https://innovate.ucdavis.edu/people/nafiz-imtiaz-khan\" target=\"_blank\">Leaders for the Future</a> Fellowship, Mike and Renée Child Institute for Innovation and Entrepreneurship"
      },

      {
        year: "2025",
        title: "<a href=\"https://grad.ucdavis.edu/travel-awards\" target=\"_blank\">Graduate Student Travel Award</a>"
      },
      {
        year: "",
        title: "Champion in the creative app contest of the ",
        event: "Tri Robo Cup",
        eventLink: "",
        organizer: "MIST Robotics Club",
        organizerLink: "https://mist.ac.bd/page/robotics-club",
        ref: "[REF]",
        refLink: "https://drive.google.com/file/d/1fWp9PXR1GYYmgZY76oHXcJ-EOUPXFaop/view?usp=sharing"
      },
      {
        year: "2020",
        title: "Top Downloaded Article Award, issued by ",
        event: "Engineering Reports",
        eventLink: "",
        ref: "[REF]",
        refLink: "https://drive.google.com/file/d/15FRjKlYTPpc7f4MiKO8ry2pez2X-cZ5P/view?usp=sharing"
      },
      {
        year: "2021",
        title: "Top Downloaded Article Award, issued by ",
        event: "Engineering Reports",
        eventLink: "",
        ref: "[REF]",
        refLink: "https://drive.google.com/file/d/1vzAHdLtPQgW8uY1vK2QUrCbUdfOwiO42/view?usp=sharing"
      },
      {
        year: "2017-2021",
        title: "MIST Dean's List Award - Three Consecutive Academic Years"
      },
      {
        year: "2017-2021",
        title: "MIST Merit Scholarship - Six Academic Semesters"
      },
      {
        year: "2024",
        title: "UC Davis GGCS Summer PhD Fellowship"
      }
    ];

    const awardsContainer = document.getElementById("awards-list");
    // Newest first; undated entries sink to the bottom.
    awards.sort((a, b) => b.year.localeCompare(a.year));
    awards.forEach(award => {
      const awardItem = document.createElement("li");
      awardItem.innerHTML = `
        ${award.title}${award.event ? `<a href="${award.eventLink}" target="_blank">${award.event}</a>` : ""}${award.organizer ? `, organized by <a href="${award.organizerLink}" target="_blank">${award.organizer}</a>` : ""}
        ${award.ref ? `<a href="${award.refLink}" target="_blank">${award.ref}</a>` : ""}
        <span class="item-year">${award.year}</span>
      `;
      awardsContainer.appendChild(awardItem);
    });
  });
