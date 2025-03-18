




document.addEventListener("DOMContentLoaded", function () {
    const articles = [
        {
          "title": "CMH Plasma bank",
          "link": "",
          "authors": "",
          "image": "img/childbicrth.jpg",
          "description": "CMH Plasma Bank is a platform for managing plasma donors and accumulated plasma in Combined Military Hospital (CMH), situated in Dhaka, Bangladesh. The app works as a database for storing details about donors and plasma information. This app is developed to help patients in CMH to get the required plasma fast. This app also helps doctors to check the availability of plasma in the plasma bank. Eventually, the endeavor of CMH and MIST for making the Plasma bank app enhanced the capability of CMH to give better treatment to COVID-19 Patients"
        },
        {
          "title": "MAAS: MIST Automated Attendance System",
          "link": "",
          "authors": "",
          "image": "img/vggs.png",
          "description": "MIST Automated Attendance System, is an integrated, embedded, and fully automated attendance system that makes use of edge and cloud computing, biometric sensors, and a real-time cloud database."
        },
        {
          "title": "UVC-PURGE V2.0",
          "link": "https://mist.ac.bd/blog/cse/post/uvc_purge_v20-146",
          "authors": "",
          "image": "img/sfrc1.jpeg",
          "description": "UVC-PURGE\u201d is a semi-autonomous UVC disinfection robot to fight against COVID-19 Pandemic. UVC-PURGE is robust, compact, and user-friendly in nature. This robot has been equipped with six T5 UVC (254 nm) lamps to destroy the SARS-CoV-2 virus (coronavirus) effectively in a standard 12\u2019 x 16\u2019 room with a disinfection time of 2-3 minutes. The Robot provides real-time camera feedback for better navigation. While disinfecting this semi-autonomous robot is capable enough to avoid any obstacles in that room. Being fully wireless and controlled by a mobile app or computer, UVC- PURGE is very user-friendly with 1600 square feet of coverage area and provides a battery backup of 2 hours. It is applicable for any indoor environment such as an Empty COVID patient ward, Empty ICU, Operation Theatre, Office room, Classroom, Corridor, Personal Apartment, etc."
        },
        {
          "title": "AFMC Admission Test System",
          "link": "https://mist.ac.bd/department/cse/announcement/346/department_of_cse_successfully_conducted_the_armed_forces_medical_college_afmc_admission_test_2021",
          "authors": "",
          "image": "img/uvc1.gif",
          "description": "AFMC Admission Test Module is developed for conducting the yearly AFMC Entrance exam. The software\n            module generates randomized MCQ questions for all the students, registered for the admission test. Thus\n            each of the students, participating in the exam, appears on the test with a unique set of questions. Next, the\n            solution evaluates each unique answer script and provides the students\u2019 ranking based on their merit. The\n            software has been used for conducting the AFMC admission Test 2021, where the number of candidates was\n            approximately 30,000."
        },
        {
          "title": "M-OMR: MIST OMR-Based Exam System",
          "link": "",
          "authors": "",
          "image": "img/bolt1.png",
          "description": "M-OMR is a generic system for conducting OMR Based exams. The system generates OMR sheets for each\n            individual candidate participating in the exam. Next, the system evaluates the OMR sheets by enumerating\n            subject-wise marking for each student and provides students\u2019 ranking based on their merit."
        },
        {
          "title": "C-Archive: MIST CSE Department Data Archive",
          "link": "",
          "authors": "",
          "image": "img/failure1.png",
          "description": "The CSE Department Data Archive is a collaborative effort of students and faculty members of the CSE\n            Department, MIST to keep the memories of the CSE Department alive. The archive stores detailed infor-\n            mation regarding Projects, Thesis, Activities, Achievements, Labs, Lab equipment, Publications, Student\n            Profiles, and Faculty Profiles of the CSE Department, MIST."
        }
      ];

    const researchSection = document.getElementById("project-container");
    articles.forEach((article, index) => {
      const isOdd = index % 2 !== 0; // Alternate layout
      const articleHTML = `
        <div class="resume-item d-flex flex-column flex-md-row justify-content-between mb-5 ${isOdd ? 'flex-md-row-reverse' : ''}">
          <div class="col-lg-4 col-md-4 col-sm-12">
            <img class="img-fluid" src="${article.image}" alt="">
          </div>
          <div class="resume-content">
            <h3 class="mb-0"><a href="${article.link}" target="_blank">${article.title}</a></h3>
            <div class="subheading mb-3">${article.authors}</div>
            <p style="text-align: justify;">${article.description}</p>
          </div>
        </div>
      `;
      researchSection.innerHTML += articleHTML;
    });
  });