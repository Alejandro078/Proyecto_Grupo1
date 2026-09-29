-- Esquema de base de datos: Sistema de Gestión de Inventario y Ventas
-- SQLite

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS detalle_ventas;
DROP TABLE IF EXISTS ventas;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS empleados;

-- Tabla base conceptual: clientes y empleados heredan de "Persona" a nivel de
-- clases Python (app/models/persona.py). A nivel de base de datos se manejan
-- como tablas independientes por simplicidad relacional.

CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    documento TEXT NOT NULL UNIQUE,
    email TEXT,
    telefono TEXT,
    direccion TEXT,
    fecha_registro TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE empleados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    documento TEXT NOT NULL UNIQUE,
    cargo TEXT NOT NULL,
    fecha_registro TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    categoria TEXT,
    precio REAL NOT NULL CHECK (precio >= 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    stock_minimo INTEGER NOT NULL DEFAULT 5,
    fecha_registro TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    empleado_id INTEGER,
    fecha TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    subtotal REAL NOT NULL DEFAULT 0,
    descuento REAL NOT NULL DEFAULT 0,
    total REAL NOT NULL DEFAULT 0,
    tipo_descuento TEXT NOT NULL DEFAULT 'ninguno',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE SET NULL
);

CREATE TABLE detalle_ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Datos de ejemplo para probar la app inmediatamente
INSERT INTO clientes (nombre, documento, email, telefono, direccion) VALUES
    ('Valentina Rojas', '1005678901', 'valentina@example.com', '3001234567', 'Cra 5 # 10-20, Palmira'),
    ('Carlos Pérez', '1098765432', 'carlos@example.com', '3109876543', 'Cll 15 # 8-30, Cali');

INSERT INTO empleados (nombre, documento, cargo) VALUES
    ('Nicolas Arteaga', '1002003004', 'Vendedor'),
    ('Alejandro Campo', '1003004005', 'Administrador');

INSERT INTO productos (nombre, descripcion, categoria, precio, stock, stock_minimo) VALUES
    ('Forro para celular', 'Forro de silicona universal', 'Accesorios', 15000, 40, 10),
    ('Cargador tipo C', 'Cargador rápido 20W', 'Accesorios', 35000, 25, 8),
    ('Audífonos Bluetooth', 'Audífonos inalámbricos con estuche', 'Audio', 65000, 12, 5),
    ('Vidrio templado', 'Protector de pantalla 9H', 'Accesorios', 12000, 3, 10),
    ('Power bank 10000mAh', 'Batería portátil de carga rápida', 'Accesorios', 55000, 18, 5);
