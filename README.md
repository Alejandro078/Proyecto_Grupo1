# Sistema de Gestión de Inventario y Ventas

Proyecto universitario — aplicación web con Flask, SQLite y arquitectura MVC.

## Requisitos

- Python 3.9 o superior
- pip

## Instalación y ejecución

```bash
# 1. Clonar el repositorio (si aún no lo tienes)
git clone https://github.com/Alejandro078/Proyecto_Grupo1.git
cd Proyecto_Grupo1

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python run.py
```

Abre el navegador en **http://localhost:5000**

La base de datos (`inventario.db`) se crea automáticamente la primera vez que
se ejecuta la app, con datos de ejemplo (2 clientes, 2 empleados y 5 productos)
para poder probar todo de inmediato.

## Estructura del proyecto (MVC)

```
Proyecto_Grupo1/
├── run.py                     # Punto de entrada
├── schema.sql                 # Estructura de la base de datos + datos de ejemplo
├── requirements.txt
└── app/
    ├── __init__.py             # Application factory, registra blueprints
    ├── models/                 # MODELO — clases y acceso a datos
    │   ├── database.py         # Encapsula la conexión SQLite (Singleton)
    │   ├── persona.py          # Clase base abstracta (ABC)
    │   ├── cliente.py          # Hereda de Persona
    │   ├── empleado.py         # Hereda de Persona
    │   ├── producto.py         # Encapsula el stock con validaciones
    │   ├── descuento.py        # Estrategias de descuento (patrón Strategy)
    │   └── venta.py            # Venta + DetalleVenta, lógica transaccional
    ├── controllers/             # CONTROLADOR — rutas de Flask (Blueprints)
    │   ├── main_controller.py
    │   ├── productos_controller.py
    │   ├── clientes_controller.py
    │   └── ventas_controller.py
    ├── templates/                # VISTA — HTML con Jinja2 + Bootstrap 5
    │   ├── base.html
    │   ├── index.html
    │   ├── productos/
    │   ├── clientes/
    │   ├── ventas/
    │   └── errores/
    ├── static/css/style.css
    └── utils/
        ├── exceptions.py        # Excepciones personalizadas
        └── validators.py        # Validación de formularios
```

## Funcionalidades

- **Dashboard**: resumen de ventas del día, productos con stock bajo, últimas ventas.
- **Productos (CRUD)**: crear, listar (con búsqueda y filtro por categoría), editar y eliminar.
- **Clientes (CRUD)**: crear, listar (con búsqueda), editar y eliminar.
- **Ventas**: registrar una venta con varios productos, aplicar un tipo de descuento,
  ver historial y el detalle de cada venta. El stock se descuenta automáticamente
  y de forma transaccional (si algo falla, no se descuenta nada).

## Conceptos de Programación Orientada a Objetos aplicados

| Concepto | Dónde se aplica |
|---|---|
| **Abstracción** | `Persona` y `EstrategiaDescuento` son clases base abstractas (`ABC`) que no se pueden instanciar directamente. |
| **Herencia** | `Cliente` y `Empleado` heredan de `Persona`. `SinDescuento`, `DescuentoPorcentaje` y `DescuentoClienteFrecuente` heredan de `EstrategiaDescuento`. |
| **Polimorfismo** | Cada subclase de `Persona` implementa `obtener_rol()` de forma distinta. Cada estrategia de descuento implementa `calcular()` de forma distinta, y `Venta` la usa sin saber cuál es. |
| **Encapsulamiento** | `Producto.stock` es una propiedad privada (`_stock`) que solo se puede modificar mediante `reducir_stock()` / `aumentar_stock()`, nunca queda en negativo. `Persona.nombre` y `.documento` usan `@property` con validación. |

## Manejo de excepciones

Todas las excepciones propias del negocio están en `app/utils/exceptions.py`
(heredan de `ErrorInventario`): `StockInsuficienteError`, `ProductoNoEncontradoError`,
`ClienteNoEncontradoError`, `DatosInvalidosError`, `VentaSinDetalleError`.
Los controladores las capturan específicamente y muestran un mensaje claro al
usuario en vez de un error genérico de servidor.

## Integrantes

- Nicolas Arteaga
- (agregar aquí los demás integrantes del equipo)
