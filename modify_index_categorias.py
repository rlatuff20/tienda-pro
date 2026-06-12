import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Clear category list in sidebar
sidebar_old = """        <ul class="category-list">
            <li><a href="javascript:void(0)" onclick="filtrarCategoria('Todas'); return false;"><span class="cat-icon"><i class='bx bx-grid-alt'></i></span> Todo el Catálogo</a></li>
            <li><a href="javascript:void(0)" onclick="filtrarCategoria('Cables Lightning y USB'); return false;"><span class="cat-icon"><i class='bx bx-plug'></i></span> Cables Lightning y USB</a></li>
            <li><a href="javascript:void(0)" onclick="filtrarCategoria('Cubos y Cargadores'); return false;"><span class="cat-icon"><i class='bx bx-bolt-circle'></i></span> Cubos y Cargadores</a></li>
            <li><a href="javascript:void(0)" onclick="filtrarCategoria('Audifonos'); return false;"><span class="cat-icon"><i class='bx bx-headphone'></i></span> Audífonos</a></li>
            <li><a href="javascript:void(0)" onclick="filtrarCategoria('Forros y Accesorios'); return false;"><span class="cat-icon"><i class='bx bx-mobile-alt'></i></span> Forros y Accesorios</a></li>
        </ul>"""
sidebar_new = """        <ul class="category-list" id="sidebar-categories">
            <li><a href="javascript:void(0)" onclick="filtrarCategoria('Todas'); return false;"><span class="cat-icon"><i class='bx bx-grid-alt'></i></span> Todo el Catálogo</a></li>
        </ul>"""
content = content.replace(sidebar_old, sidebar_new)

# 2. Clear chips scroll
chips_old = """        <div class="chips-scroll" id="chips-bar">
            <button class="chip active" onclick="chipClick(this, 'Todas')"><i class='bx bx-grid-alt'></i> Todo</button>
            <button class="chip" onclick="chipClick(this, 'Cables Lightning y USB')"><i class='bx bx-plug'></i> Cables</button>
            <button class="chip" onclick="chipClick(this, 'Cubos y Cargadores')"><i class='bx bx-bolt-circle'></i> Cargadores</button>
            <button class="chip" onclick="chipClick(this, 'Audifonos')"><i class='bx bx-headphone'></i> Audífonos</button>
            <button class="chip" onclick="chipClick(this, 'Forros y Accesorios')"><i class='bx bx-mobile-alt'></i> Forros</button>
        </div>"""
chips_new = """        <div class="chips-scroll" id="chips-bar">
            <button class="chip active" onclick="chipClick(this, 'Todas')"><i class='bx bx-grid-alt'></i> Todo</button>
        </div>"""
content = content.replace(chips_old, chips_new)

# 3. Add JS functions
js_code = """
    let categoriasGlobales = [];

    function renderCategoriasTienda() {
        const chipsBar = document.getElementById('chips-bar');
        const sidebarCats = document.getElementById('sidebar-categories');
        
        let chipsHTML = `<button class="chip active" onclick="chipClick(this, 'Todas')"><i class='bx bx-grid-alt'></i> Todo</button>`;
        let sidebarHTML = `<li><a href="javascript:void(0)" onclick="filtrarCategoria('Todas'); return false;"><span class="cat-icon"><i class='bx bx-grid-alt'></i></span> Todo el Catálogo</a></li>`;
        
        categoriasGlobales.forEach(c => {
            chipsHTML += `<button class="chip" onclick="chipClick(this, '${c.nombre}')"><i class='bx ${c.icono}'></i> ${c.nombre}</button>`;
            sidebarHTML += `<li><a href="javascript:void(0)" onclick="filtrarCategoria('${c.nombre}'); return false;"><span class="cat-icon"><i class='bx ${c.icono}'></i></span> ${c.nombre}</a></li>`;
        });
        
        if (chipsBar) chipsBar.innerHTML = chipsHTML;
        if (sidebarCats) sidebarCats.innerHTML = sidebarHTML;
    }
"""

content = content.replace("let productosGlobales = [];", "let productosGlobales = [];\n" + js_code)

# 4. Fetch categorias in DOMContentLoaded
fetch_code = """
        fetch('/categorias')
            .then(res => res.json())
            .then(cats => {
                categoriasGlobales = cats;
                renderCategoriasTienda();
            })
            .catch(err => console.error('Error al cargar categorias:', err));
"""

# Insert fetch_code right before fetch('/productos')
content = content.replace("fetch('/productos')", fetch_code + "\n        fetch('/productos')")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html modificado exitosamente con categorias dinamicas")
