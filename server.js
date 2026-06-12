require('dotenv').config(); // <-- Esta línea lee tu archivo .env
const express = require('express');
const cors = require('cors');
const path = require('path');
const mongoose = require('mongoose');

// IMPORTACIONES PARA LAS FOTOS
const multer = require('multer');
const cloudinary = require('cloudinary').v2;
const { CloudinaryStorage } = require('multer-storage-cloudinary');

const app = express();

app.use(express.json());
app.use(cors());
app.use(express.static(path.join(__dirname)));

// 1. Conexión a MongoDB
mongoose.connect(process.env.MONGO_URI)
    .then(() => console.log('¡Conectado a MongoDB Atlas!'))
    .catch(err => console.error('Error conectando a MongoDB:', err));

// 2. Configuración de Cloudinary
cloudinary.config({
    cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
    api_key: process.env.CLOUDINARY_API_KEY,
    api_secret: process.env.CLOUDINARY_API_SECRET
});

// 3. Configuración de Multer (La bóveda)
const storage = new CloudinaryStorage({
    cloudinary: cloudinary,
    params: {
        folder: 'ConectaTech', // Tu carpeta en Cloudinary
        allowedFormats: ['jpeg', 'png', 'jpg', 'webp']
    }
});
const upload = multer({ storage: storage });

// 4. Esquemas de Base de Datos
const productoSchema = new mongoose.Schema({
    name: String,
    category: String,
    price: Number,
    img: String, 
    stock: Number,
    features: [String]
});
const Producto = mongoose.model('Producto', productoSchema);

const historialSchema = new mongoose.Schema({
    accion: { type: String, required: true },
    detalles: { type: String, required: true },
    fecha: { type: Date, default: Date.now }
});
const Historial = mongoose.model('Historial', historialSchema);

const usuariosAdministradores = [
    { usuario: "admin", password: "udo2026" },
    { usuario: "ronald", password: "candy" }
];
const TOKEN_SECRETO = "credencial-secreta-caps-store-2026";

// ================= RUTAS =================

app.post('/login', (req, res) => {
    const { usuario, password } = req.body;
    const usuarioValido = usuariosAdministradores.find(u => u.usuario === usuario && u.password === password);

    if (usuarioValido) {
        res.json({ exito: true, token: TOKEN_SECRETO, mensaje: "Acceso concedido" });
    } else {
        res.status(401).json({ exito: false, mensaje: "Usuario o contraseña incorrectos" });
    }
});

app.get('/productos', async (req, res) => {
    try {
        const productos = await Producto.find().sort({ category: 1, name: 1 });
        res.json(productos);
    } catch (err) {
        res.status(500).json({ mensaje: "Error al leer la base de datos" });
    }
});

// RUTA DE ESTADÍSTICAS PARA EL DASHBOARD ADMIN
app.get('/stats', async (req, res) => {
    try {
        const token = req.headers['authorization'];
        if (token !== TOKEN_SECRETO) return res.status(401).json({ mensaje: "No autorizado" });

        const totalProductos = await Producto.countDocuments();
        const productos = await Producto.find();
        const stockBajo = productos.filter(p => p.stock <= 3).length;
        const sinStock = productos.filter(p => p.stock === 0).length;
        const categoriasUnicas = [...new Set(productos.map(p => p.category))];
        const valorInventario = productos.reduce((sum, p) => sum + (p.price * p.stock), 0);

        res.json({
            totalProductos,
            stockBajo,
            sinStock,
            totalCategorias: categoriasUnicas.length,
            valorInventario: valorInventario.toFixed(2)
        });
    } catch (err) {
        res.status(500).json({ mensaje: "Error al obtener estadísticas" });
    }
});

// RUTA DE CREAR PRODUCTO (Soporta la foto de Cloudinary)
app.post('/productos', upload.single('image'), async (req, res) => {
    try {
        const tokenCliente = req.headers['authorization'];
        if (tokenCliente !== TOKEN_SECRETO) return res.status(403).json({ mensaje: "No autorizado." });

        const { name, category, price, stock, features } = req.body;
        
        // Atrapamos el link de Cloudinary (si no hay foto, guarda un string vacío)
        const imageUrl = req.file ? req.file.path : '';

        const nuevoProducto = new Producto({
            name,
            category,
            price: parseFloat(price),
            stock: parseInt(stock),
            img: imageUrl,
            features: features ? features.split(',') : []
        });
        await nuevoProducto.save();

        const nuevoLog = new Historial({
            accion: "CREAR",
            detalles: `Se agregó el producto: ${nuevoProducto.name}`
        });
        await nuevoLog.save();

        res.json({ mensaje: "¡Producto y foto guardados con éxito!", producto: nuevoProducto });
    } catch (error) {
        console.error("Error en POST /productos:", error);
        res.status(500).json({ mensaje: "Error al guardar el producto", error });
    }
});

app.delete('/productos/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const token = req.headers['authorization'];
        
        if (token !== TOKEN_SECRETO) return res.status(401).json({ mensaje: "No autorizado" });

        const productoEliminado = await Producto.findByIdAndDelete(id);
        if (!productoEliminado) return res.status(404).json({ mensaje: "Producto no encontrado" });

        const nuevoLog = new Historial({
            accion: "ELIMINAR",
            detalles: `Se eliminó el producto: ${productoEliminado.name}`
        });
        await nuevoLog.save();

        res.json({ mensaje: "Producto eliminado con éxito" });
    } catch (error) {
        res.status(500).json({ mensaje: "Error al eliminar el producto", error });
    }
});

// RUTA DE EDITAR PRODUCTO COMPLETO
app.put('/productos/:id', upload.single('image'), async (req, res) => {
    try {
        const { id } = req.params;
        const token = req.headers['authorization'];
        if (token !== TOKEN_SECRETO) return res.status(403).json({ mensaje: "No autorizado." });

        const producto = await Producto.findById(id);
        if (!producto) return res.status(404).json({ mensaje: "Producto no encontrado" });

        const { name, category, price, stock, features } = req.body;
        if (name) producto.name = name;
        if (category) producto.category = category;
        if (price) producto.price = parseFloat(price);
        if (stock !== undefined) producto.stock = parseInt(stock);
        if (features) producto.features = features.split(',');
        if (req.file) producto.img = req.file.path;

        await producto.save();

        const nuevoLog = new Historial({
            accion: "EDITAR",
            detalles: `Se editó el producto: ${producto.name}`
        });
        await nuevoLog.save();

        res.json({ mensaje: "Producto actualizado con éxito", producto });
    } catch (error) {
        console.error("Error en PUT /productos/:id:", error);
        res.status(500).json({ mensaje: "Error al editar el producto", error });
    }
});

app.put('/productos/:id/stock', async (req, res) => {
    try {
        const { id } = req.params;
        const { accion } = req.body;
        const token = req.headers['authorization'];
        
        if (token !== TOKEN_SECRETO) return res.status(401).json({ mensaje: "No autorizado" });

        const producto = await Producto.findById(id);
        if (!producto) return res.status(404).json({ mensaje: "Producto no encontrado" });

        if (accion === 'sumar') {
            producto.stock += 1;
        } else if (accion === 'restar') {
            if (producto.stock > 0) producto.stock -= 1;
            else return res.status(400).json({ mensaje: "El stock ya está en 0." });
        }

        await producto.save();

        const nuevoLog = new Historial({
            accion: "ACTUALIZAR STOCK",
            detalles: `Se modificó el stock de "${producto.name}". Nuevo stock: ${producto.stock}`
        });
        await nuevoLog.save();

        res.json({ mensaje: "Stock actualizado", stock: producto.stock });
    } catch (error) {
        res.status(500).json({ mensaje: "Error al actualizar el stock", error });
    }
});

// RUTA DE HISTORIAL DE ACCIONES
app.get('/historial', async (req, res) => {
    try {
        const token = req.headers['authorization'];
        if (token !== TOKEN_SECRETO) return res.status(401).json({ mensaje: "No autorizado" });

        const historial = await Historial.find().sort({ fecha: -1 }).limit(50);
        res.json(historial);
    } catch (error) {
        res.status(500).json({ mensaje: "Error al obtener el historial", error });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Servidor corriendo en puerto ${PORT}`);
});
app.get('/sitemap.xml', async (req, res) => {
    try {
        const productos = await Producto.find();
        let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
        
        // La URL base de tu tienda
        const baseUrl = 'https://conectatech.onrender.com';
        
        // Agregar la página principal
        xml += `  <url>\n    <loc>${baseUrl}/</loc>\n    <changefreq>daily</changefreq>\n  </url>\n`;

        // Agregar cada producto
        productos.forEach(p => {
            xml += `  <url>\n    <loc>${baseUrl}/?id=${p._id}</loc>\n    <lastmod>${new Date().toISOString()}</lastmod>\n  </url>\n`;
        });

        xml += '</urlset>';
        res.header('Content-Type', 'application/xml');
        res.send(xml);
    } catch (err) {
        res.status(500).send("Error generando sitemap");
    }
});