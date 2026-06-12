import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add "Categorías" tab to navbar
navbar_tab = """        <button class="nav-tab" data-tab="historial"><i class='bx bx-list-ul'></i> Historial</button>
        <button class="nav-tab" data-tab="categorias"><i class='bx bx-purchase-tag-alt'></i> Categorías</button>"""
content = content.replace("<button class=\"nav-tab\" data-tab=\"historial\"><i class='bx bx-list-ul'></i> Historial</button>", navbar_tab)

# 2. Add "Categorías" tab content after Historial tab
categorias_tab_content = """      <!-- ── Categorías Tab ── -->
      <section id="categorias-tab" class="tab-content">
        <div class="header-action">
          <h2><i class='bx bx-purchase-tag-alt'></i> Gestionar Categorías</h2>
        </div>
        
        <div class="form-card" style="margin-bottom: 24px;">
          <h3>Añadir Nueva Categoría</h3>
          <form id="formNuevaCategoria">
            <div class="form-group">
              <label>Nombre de la Categoría</label>
              <input type="text" id="nuevaCatNombre" class="dark-input" placeholder="Ej: Smartwatches" required />
            </div>
            <div class="form-group">
              <label>Icono (Boxicons)</label>
              <select id="nuevaCatIcono" class="dark-input" required>
                <option value="bx-purchase-tag-alt">Etiqueta (Predeterminado)</option>
                <option value="bx-mobile">Móvil / Celular</option>
                <option value="bx-headphone">Audífonos</option>
                <option value="bx-plug">Cable / Enchufe</option>
                <option value="bx-bolt-circle">Energía / Cargador</option>
                <option value="bx-laptop">Laptop / Computadora</option>
                <option value="bx-game">Juegos</option>
                <option value="bx-watch">Reloj Inteligente</option>
                <option value="bx-camera">Cámara</option>
                <option value="bx-mouse">Mouse</option>
                <option value="bx-speaker">Parlante / Corneta</option>
              </select>
            </div>
            <button type="submit" class="btn-submit"><i class='bx bx-plus'></i> Guardar Categoría</button>
          </form>
        </div>

        <div class="table-container">
          <table class="dark-table">
            <thead>
              <tr>
                <th>Icono</th>
                <th>Nombre</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody id="tablaCategorias">
              <tr><td colspan="3" class="empty-state"><p>Cargando categorías...</p></td></tr>
            </tbody>
          </table>
        </div>
      </section>
"""

content = content.replace("<!-- ── Editar Producto Modal ── -->", categorias_tab_content + "\n      <!-- ── Editar Producto Modal ── -->")

# 3. Change "Categoría" text input to <select> in Nuevo Producto
nuevo_prod_input = '<input type="text" class="dark-input" name="category" placeholder="Ej: Audio" required />'
nuevo_prod_select = '<select class="dark-input" name="category" id="selectNuevoCategoria" required><option value="">Cargando...</option></select>'
content = content.replace(nuevo_prod_input, nuevo_prod_select)

# 4. Change "Categoría" text input to <select> in Editar Producto
edit_prod_input = '<input type="text" id="editCategoria" class="dark-input" required />'
edit_prod_select = '<select id="editCategoria" class="dark-input" required><option value="">Cargando...</option></select>'
content = content.replace(edit_prod_input, edit_prod_select)

# 5. Inject Javascript functions for categories
js_functions = """
    let categoriasCache = [];

    async function cargarCategoriasAdmin() {
      try {
        const res = await fetch('/categorias');
        const categorias = await res.json();
        categoriasCache = categorias;
        
        // Llenar selects
        const selectNuevo = document.getElementById('selectNuevoCategoria');
        const selectEdit = document.getElementById('editCategoria');
        let options = '';
        categorias.forEach(c => {
          options += `<option value="${c.nombre}">${c.nombre}</option>`;
        });
        if(selectNuevo) selectNuevo.innerHTML = options;
        if(selectEdit) selectEdit.innerHTML = options;

        // Llenar tabla de categorías
        const tbody = document.getElementById('tablaCategorias');
        if(!tbody) return;
        if (!categorias.length) {
          tbody.innerHTML = `<tr><td colspan="3" class="empty-state">No hay categorías</td></tr>`;
          return;
        }
        tbody.innerHTML = categorias.map(c => `
          <tr>
            <td><i class='bx ${c.icono}' style="font-size: 1.5rem;"></i></td>
            <td>${c.nombre}</td>
            <td>
              <button class="btn-action delete" onclick="borrarCategoria('${c._id}')"><i class='bx bx-trash'></i> Eliminar</button>
            </td>
          </tr>
        `).join('');

      } catch (err) {
        console.error('Error al cargar categorias', err);
      }
    }

    // Submit nueva categoría
    const formCat = document.getElementById('formNuevaCategoria');
    if(formCat) {
      formCat.addEventListener('submit', async (e) => {
        e.preventDefault();
        const nombre = document.getElementById('nuevaCatNombre').value.trim();
        const icono = document.getElementById('nuevaCatIcono').value;
        try {
          const res = await fetch('/categorias', {
            method: 'POST',
            headers: { ...authHeaders(), 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, icono })
          });
          const data = await res.json();
          if (res.ok) {
            showToast('Categoría añadida', 'success');
            document.getElementById('nuevaCatNombre').value = '';
            cargarCategoriasAdmin();
          } else {
            showToast(data.mensaje || 'Error al añadir', 'error');
          }
        } catch (err) {
          showToast('Error de conexión', 'error');
        }
      });
    }

    async function borrarCategoria(id) {
      if (!confirm('¿Seguro que deseas eliminar esta categoría? Los productos dentro de ella pasarán a "Otros".')) return;
      try {
        const res = await fetch(`/categorias/${id}`, {
          method: 'DELETE',
          headers: authHeaders()
        });
        if (res.ok) {
          showToast('Categoría eliminada', 'success');
          cargarCategoriasAdmin();
          cargarProductosAdmin(); // Update product table since their categories might have changed to 'Otros'
        } else {
          showToast('Error al eliminar', 'error');
        }
      } catch (err) {
        showToast('Error de conexión', 'error');
      }
    }

"""

# Insert JS before "/* ── Load Products ── */"
content = content.replace("/* ── Load Products ── */", js_functions + "\n    /* ── Load Products ── */")

# Also call cargarCategoriasAdmin() inside mostrarPanel()
content = content.replace("cargarHistorial();", "cargarHistorial();\n      cargarCategoriasAdmin();")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("admin.html modificado exitosamente con categorias dinamicas")
