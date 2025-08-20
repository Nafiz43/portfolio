# Personal Portfolio Website

A simple, responsive portfolio site I built for my academic/professional profile. It's easy to customize and maintain. Feel free to fork and adapt it for your own use!

## Overview

A basic portfolio website with sections for education, work experience, research, projects, and contact info. Uses vanilla JavaScript to load content dynamically from separate data files, making it easy to update without touching the main HTML.

## Features

- Responsive design
- Fixed sidebar navigation 
- Dynamic content loading from JS modules
- PDF viewer for CV
- Simple animations and glass-effect styling

## Tech Stack

- HTML5/CSS3/JavaScript
- Bootstrap 4 for responsive grid
- Font Awesome icons
- Google Fonts (Inter, JetBrains Mono)

## Project Structure

```plaintext
├── index.html              # Main page
├── css/resume.css         # Custom styles
├── js/
│   ├── articles.js        # Research data
│   ├── projects.js        # Project data
│   ├── work_experience.js # Job history
│   ├── awards.js          # Awards/honors
│   ├── activities.js      # Professional activities
│   └── teaching_experience_mist.js # Teaching data
├── img/                   # Images and icons
└── vendor/               # Bootstrap, jQuery, etc.
```

## Setup

1. Clone or download the repo
2. Open [`index.html`](index.html) in your browser (or use a local server)
3. Replace the content in the JS files with your own data
4. Update personal info in [`index.html`](index.html)
5. Swap out the profile picture and favicon

## Customizing Content

The portfolio loads most content from JavaScript files, so you can update your info without digging into the HTML:

**Research/Publications** ([`js/articles.js`](js/articles.js)):
```javascript
const articles = [
    {
        title: "Your Paper Title",
        authors: "Author Names", 
        conference: "Venue",
        year: "2024"
    }
];
```

**Projects** ([`js/projects.js`](js/projects.js)):
```javascript
const projects = [
    {
        title: "Project Name",
        description: "What it does",
        link: "github.com/..."
    }
];
```

Same pattern for work experience ([`js/work_experience.js`](js/work_experience.js)), awards ([`js/awards.js`](js/awards.js)), and other sections. Check the existing files to see the data structure.

## Using This Template

Go ahead and fork this if it's useful to you. Just drop a credit somewhere (footer, readme, wherever) mentioning it was adapted from my template. Something like:

```plaintext
Template adapted from Nafiz Imtiaz Khan's portfolio
```

That's it. No need to ask permission or anything.

## Notes

- Tested on modern browsers (Chrome, Firefox, Safari, Edge)
- The glass effects use CSS backdrop-filter, which has decent browser support now
- All content is static - no backend needed
- PDF embedding uses Google Drive viewer, but you can swap in any PDF URL

## Need Help?

If you run into problems or have suggestions, feel free to open an issue or reach out:

- Email: imtiznafiz@gmail.com
- GitHub: [@Nafiz43](https://github.com/Nafiz43)
- LinkedIn: [nafiz43](https://www.linkedin.com/in/nafiz43)

## License

MIT License
