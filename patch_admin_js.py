import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the form to have a hidden input for edit mode
form_old = """          <form id="formNuevaCategoria">
            <div class="form-group">
              <label>Nombre de la Categoría</label>"""
form_new = """          <form id="formNuevaCategoria">
            <input type="hidden" id="editCatId" value="">
            <div class="form-group">
              <label>Nombre de la Categoría</label>"""
content = content.replace(form_old, form_new)

# 2. Extract and replace the entire javascript block for categories
js_new = """
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
            <td style="display: flex; gap: 8px;">
              <button class="btn-action edit" onclick="prepararEdicionCategoria('${c._id}', '${c.nombre}', '${c.icono}')"><i class='bx bx-pencil'></i> Editar</button>
              <button class="btn-action delete" onclick="borrarCategoria('${c._id}')"><i class='bx bx-trash'></i> Eliminar</button>
            </td>
          </tr>
        `).join('');

      } catch (err) {
        console.error('Error al cargar categorias', err);
      }
    }

    function prepararEdicionCategoria(id, nombre, icono) {
        document.getElementById('editCatId').value = id;
        document.getElementById('nuevaCatNombre').value = nombre;
        document.getElementById('nuevaCatIcono').value = icono;
        document.querySelector('#formNuevaCategoria .btn-submit').innerHTML = "<i class='bx bx-save'></i> Actualizar Categoría";
        
        // Scroll to the form
        document.getElementById('formNuevaCategoria').scrollIntoView({ behavior: 'smooth' });
    }

    function limpiarFormCategoria() {
        document.getElementById('editCatId').value = '';
        document.getElementById('nuevaCatNombre').value = '';
        document.getElementById('nuevaCatIcono').value = 'bx-purchase-tag-alt';
        document.querySelector('#formNuevaCategoria .btn-submit').innerHTML = "<i class='bx bx-plus'></i> Guardar Categoría";
    }

    // Usar DOMContentLoaded para asegurar que el DOM existe
    document.addEventListener('DOMContentLoaded', () => {
      const formCat = document.getElementById('formNuevaCategoria');
      if(formCat) {
        formCat.addEventListener('submit', async (e) => {
          e.preventDefault();
          const id = document.getElementById('editCatId').value;
          const nombre = document.getElementById('nuevaCatNombre').value.trim();
          const icono = document.getElementById('nuevaCatIcono').value;
          
          try {
            const isEdit = id !== '';
            const url = isEdit ? `/categorias/${id}` : '/categorias';
            const method = isEdit ? 'PUT' : 'POST';

            const res = await fetch(url, {
              method: method,
              headers: { ...authHeaders(), 'Content-Type': 'application/json' },
              body: JSON.stringify({ nombre, icono })
            });
            const data = await res.json();
            
            if (res.ok) {
              showToast(isEdit ? 'Categoría actualizada' : 'Categoría añadida', 'success');
              limpiarFormCategoria();
              cargarCategoriasAdmin();
              cargarProductosAdmin(); // Refrescar tabla por si hubo cambios de nombre
            } else {
              showToast(data.mensaje || 'Error al guardar', 'error');
            }
          } catch (err) {
            showToast('Error de conexión', 'error');
          }
        });
      }
    });

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
          cargarProductosAdmin(); 
        } else {
          showToast('Error al eliminar', 'error');
        }
      } catch (err) {
        showToast('Error de conexión', 'error');
      }
    }
"""

# Replace the old JS block
pattern = re.compile(r'let categoriasCache = \[\];.*?async function borrarCategoria\(id\) \{.*?\}\s*\}', re.DOTALL)
content = pattern.sub(js_new, content)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("admin JS modificado")
