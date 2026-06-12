const fs = require('fs');
const { JSDOM } = require('jsdom');
const html = fs.readFileSync('/home/ronald/Escritorio/proyectos/pagina1/admin.html', 'utf-8');

const dom = new JSDOM(html, {
  url: "http://localhost:3000/admin.html",
  runScripts: "dangerously",
  resources: "usable"
});

dom.window.addEventListener("error", (event) => {
  console.error("DOM Error:", event.error);
});

setTimeout(() => {
  console.log("JSDOM initialization complete");
}, 2000);
