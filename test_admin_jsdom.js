const fs = require('fs');
const { JSDOM } = require('jsdom');
const html = fs.readFileSync('admin.html', 'utf-8');

const dom = new JSDOM(html, {
  url: "http://localhost:3000/admin.html",
  runScripts: "dangerously",
  resources: "usable"
});

setTimeout(() => {
  console.log("formCat:", dom.window.document.getElementById('formNuevaCategoria'));
  console.log("tbody:", dom.window.document.getElementById('tablaCategorias').innerHTML.trim());
}, 2000);
