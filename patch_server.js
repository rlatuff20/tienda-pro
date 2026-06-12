const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

const putRoute = `
app.put('/categorias/:id', async (req, res) => {
    try {
        const token = req.headers['authorization'];
        if (token !== TOKEN_SECRETO) return res.status(401).json({ mensaje: "No autorizado" });

        const { nombre, icono } = req.body;
        if (!nombre) return res.status(400).json({ mensaje: "Falta el nombre" });

        const cat = await Categoria.findById(req.params.id);
        if(!cat) return res.status(404).json({ mensaje: "Categoría no encontrada" });

        const oldName = cat.nombre;
        cat.nombre = nombre;
        if (icono) cat.icono = icono;
        await cat.save();

        // Actualizar todos los productos que tenían el nombre viejo
        if (oldName !== nombre) {
            await Producto.updateMany({ category: oldName }, { category: nombre });
        }

        const nuevaEntrada = new Historial({
            accion: 'EDITAR CATEGORÍA',
            detalles: \`Editó la categoría: \${oldName} -> \${nombre}\`
        });
        await nuevaEntrada.save();

        res.json({ exito: true, mensaje: "Categoría actualizada", categoria: cat });
    } catch (err) {
        res.status(500).json({ mensaje: "Error al actualizar categoría", error: err.message });
    }
});
`

if (!code.includes("app.put('/categorias/:id'")) {
    code = code.replace("app.delete('/categorias/:id'", putRoute + "\napp.delete('/categorias/:id'");
    fs.writeFileSync('server.js', code);
    console.log("Ruta PUT añadida a server.js");
} else {
    console.log("Ruta PUT ya existe");
}
