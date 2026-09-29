"""Modelo Venta + DetalleVenta.

Registrar una venta implica: validar stock de cada producto, calcular
subtotal/descuento/total, descontar el stock y guardar todo. Si algo
falla a mitad de camino, no debe quedar stock descontado a medias.
"""

from app.models.database import db
from app.models.producto import Producto
from app.utils.exceptions import VentaSinDetalleError


class DetalleVenta:
    def __init__(self, producto_id, cantidad, precio_unitario, producto_nombre=None):
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.producto_nombre = producto_nombre

    @property
    def subtotal(self):
        return round(self.cantidad * self.precio_unitario, 2)

    def to_dict(self):
        return {
            "producto_id": self.producto_id,
            "producto_nombre": self.producto_nombre,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal,
        }


class Venta:
    def __init__(self, cliente_id=None, empleado_id=None, detalles=None,
                 estrategia_descuento=None, id=None, fecha=None):
        self.id = id
        self.cliente_id = cliente_id
        self.empleado_id = empleado_id
        self.detalles = detalles or []
        self.estrategia_descuento = estrategia_descuento
        self.fecha = fecha
        self.subtotal = 0.0
        self.descuento = 0.0
        self.total = 0.0

    def agregar_detalle(self, detalle):
        self.detalles.append(detalle)

    def calcular_totales(self):
        if not self.detalles:
            raise VentaSinDetalleError()
        self.subtotal = round(sum(d.subtotal for d in self.detalles), 2)
        self.descuento = (
            self.estrategia_descuento.calcular(self.subtotal)
            if self.estrategia_descuento else 0.0
        )
        self.total = round(self.subtotal - self.descuento, 2)
        return self.total

    def registrar(self):
        """Valida stock, descuenta inventario y persiste todo. Usa una sola
        transacción SQLite para que, si algo falla, no quede a medias."""
        if not self.detalles:
            raise VentaSinDetalleError()

        # 1. Cargar productos y validar stock ANTES de tocar la base de datos
        productos = {}
        for detalle in self.detalles:
            producto = Producto.obtener_por_id(detalle.producto_id)
            producto.reducir_stock(detalle.cantidad)  # lanza StockInsuficienteError si no alcanza
            productos[detalle.producto_id] = producto
            detalle.producto_nombre = producto.nombre
            detalle.precio_unitario = producto.precio

        self.calcular_totales()

        nombre_estrategia = self.estrategia_descuento.nombre if self.estrategia_descuento else "ninguno"

        conexion = db.obtener_conexion()
        try:
            cursor = conexion.execute(
                "INSERT INTO ventas (cliente_id, empleado_id, subtotal, descuento, "
                "total, tipo_descuento) VALUES (?, ?, ?, ?, ?, ?)",
                (self.cliente_id, self.empleado_id, self.subtotal, self.descuento,
                 self.total, nombre_estrategia),
            )
            self.id = cursor.lastrowid

            for detalle in self.detalles:
                conexion.execute(
                    "INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, "
                    "precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?)",
                    (self.id, detalle.producto_id, detalle.cantidad,
                     detalle.precio_unitario, detalle.subtotal),
                )
                producto = productos[detalle.producto_id]
                conexion.execute(
                    "UPDATE productos SET stock = ? WHERE id = ?",
                    (producto.stock, producto.id),
                )

            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

        return self

    # ------------------------------ Consultas ------------------------------

    @staticmethod
    def obtener_todas():
        filas = db.consultar_todas(
            """
            SELECT v.*, c.nombre AS cliente_nombre, e.nombre AS empleado_nombre
            FROM ventas v
            LEFT JOIN clientes c ON c.id = v.cliente_id
            LEFT JOIN empleados e ON e.id = v.empleado_id
            ORDER BY v.fecha DESC
            """
        )
        return filas

    @staticmethod
    def obtener_por_id(venta_id):
        venta = db.consultar_una(
            """
            SELECT v.*, c.nombre AS cliente_nombre, e.nombre AS empleado_nombre
            FROM ventas v
            LEFT JOIN clientes c ON c.id = v.cliente_id
            LEFT JOIN empleados e ON e.id = v.empleado_id
            WHERE v.id = ?
            """,
            (venta_id,),
        )
        if venta is None:
            return None, []
        detalles = db.consultar_todas(
            """
            SELECT dv.*, p.nombre AS producto_nombre
            FROM detalle_ventas dv
            JOIN productos p ON p.id = dv.producto_id
            WHERE dv.venta_id = ?
            """,
            (venta_id,),
        )
        return venta, detalles

    @staticmethod
    def resumen_dashboard():
        total_ventas_hoy = db.consultar_una(
            "SELECT COUNT(*) AS cantidad, COALESCE(SUM(total), 0) AS total "
            "FROM ventas WHERE date(fecha) = date('now', 'localtime')"
        )
        total_productos = db.consultar_una("SELECT COUNT(*) AS cantidad FROM productos")
        total_clientes = db.consultar_una("SELECT COUNT(*) AS cantidad FROM clientes")
        return {
            "ventas_hoy_cantidad": total_ventas_hoy["cantidad"],
            "ventas_hoy_total": total_ventas_hoy["total"],
            "total_productos": total_productos["cantidad"],
            "total_clientes": total_clientes["cantidad"],
        }
