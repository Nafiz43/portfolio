

  document.addEventListener("DOMContentLoaded", function () {
    const courses = [
      { code: "CSE - 105", name: "Structured Programming Language", term: "Fall '21" },
      { code: "CSE - 101", name: "Discrete Mathematics", term: "Spring '21" },
      { code: "CSE - 121", name: "Introduction to Computer Science and Programming Language", term: "Fall '22" },
      { code: "CSE - 319", name: "Software Engineering", term: "Fall '22" },
      { code: "CSE - 203", name: "Data Structure & Algorithm" },
      { code: "CSE - 205", name: "Object Oriented Programming Language" },
      { code: "CSE - 402", name: "Information System Design and Development Sessional", term: "Spring '21, Spring '22" },
      { code: "CSE - 206", name: "Object Oriented Programming Sessional", term: "Spring '21, Spring '22" },
      { code: "CSE - 106", name: "Structured Programming Language Sessional", term: "Fall '21" },
      { code: "CSE - 224", name: "Advanced Programming Language Sessional", term: "Fall '21" },
      { code: "CSE - 360", name: "Integrated Design Project - I", term: "Spring '22" },
      { code: "CSE - 460", name: "Integrated Design Project - II", term: "Fall '22" },
      { code: "CSE - 122", name: "Introduction to Computer Science and Programming Language Sessional", term: "Fall '22" },
      { code: "CSE - 204", name: "Data Structure & Algorithm Sessional" },
      { code: "CSE - 206", name: "Object Oriented Programming Language Sessional" }
    ];

    const coursesList = document.getElementById("courses-taught-mist");

    courses.forEach(course => {
      const listItem = document.createElement("li");
      listItem.innerHTML = `<b>${course.code}:</b> ${course.name} ${course.term ? `(${course.term})` : ""}`;
      coursesList.appendChild(listItem);
    });
  });