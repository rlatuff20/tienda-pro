const fs = require('fs');
const { JSDOM } = require('jsdom');
const html = fs.readFileSync('admin.html', 'utf-8');

const dom = new JSDOM(html, {
  url: "http://localhost:3000/admin.html",
  runScripts: "dangerously",
  resources: "usable"
});

// Polyfill fetch in JSDOM
dom.window.fetch = async (url, options) => {
    // If relative url, prepend localhost
    if (url.startsWith('/')) {
        url = 'http://localhost:3000' + url;
    }
    const res = await fetch(url, options);
    return res;
};

setTimeout(async () => {
  try {
      await dom.window.cargarCategoriasAdmin();
      console.log("TBODY: ", dom.window.document.getElementById('tablaCategorias').innerHTML);
      console.log("SELECT: ", dom.window.document.getElementById('selectNuevoCategoria').innerHTML);
  } catch (e) {
      console.error("FAIL:", e);
  }
}, 2000);
