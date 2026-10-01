"""Modelo Producto. El stock es un atributo encapsulado: solo puede
cambiar a través de métodos que validan la operación."""

from app.models.database import db
from app.utils.exceptions import ProductoNoEncontradoError, StockInsuficienteError


class Producto:
    def __init__(self, nombre, precio, stock=0, descripcion=None, categoria=None,
                 stock_minimo=5, id=None, fecha_registro=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.precio = precio
        self._stock = 0
        self.stock = stock  # pasa por el setter validado
        self.stock_minimo = stock_minimo
        self.fecha_registro = fecha_registro

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        valor = int(valor)
        if valor < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = valor

    @property
    def stock_bajo(self):
        return self._stock <= self.stock_minimo

    def reducir_stock(self, cantidad):
        """Descuenta unidades del inventario, validando disponibilidad."""
        if cantidad <= 0:
            raise ValueError("La cantidad a reducir debe ser mayor que cero.")
        if cantidad > self._stock:
            raise StockInsuficienteError(self.nombre, self._stock, cantidad)
        self._stock -= cantidad

    def aumentar_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a aumentar debe ser mayor que cero.")
        self._stock += cantidad

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
            "stock_minimo": self.stock_minimo,
            "stock_bajo": self.stock_bajo,
            "fecha_registro": self.fecha_registro,
        }

    # ---------------------------- Persistencia ----------------------------

    @staticmethod
    def _desde_fila(fila):
        if not fila:
            return None
        return Producto(
            id=fila["id"], nombre=fila["nombre"], descripcion=fila["descripcion"],
            categoria=fila["categoria"], precio=fila["precio"], stock=fila["stock"],
            stock_minimo=fila["stock_minimo"], fecha_registro=fila["fecha_registro"],
        )

    @staticmethod
    def obtener_todos(busqueda=None, categoria=None):
        consulta = "SELECT * FROM productos WHERE 1=1"
        parametros = []
        if busqueda:
            consulta += " AND nombre LIKE ?"
            parametros.append(f"%{busqueda}%")
        if categoria:
            consulta += " AND categoria = ?"
            parametros.append(categoria)
        consulta += " ORDER BY nombre"
        filas = db.consultar_todas(consulta, tuple(parametros))
        return [Producto._desde_fila(f) for f in filas]

    @staticmethod
    def obtener_por_id(producto_id):
        fila = db.consultar_una("SELECT * FROM productos WHERE id = ?", (producto_id,))
        producto = Producto._desde_fila(fila)
        if producto is None:
            raise ProductoNoEncontradoError(producto_id)
        return producto

    @staticmethod
    def obtener_categorias():
        filas = db.consultar_todas(
            "SELECT DISTINCT categoria FROM productos WHERE categoria IS NOT NULL "
            "ORDER BY categoria"
        )
        return [f["categoria"] for f in filas]

    @staticmethod
    def con_stock_bajo():
        filas = db.consultar_todas(
            "SELECT * FROM productos WHERE stock <= stock_minimo ORDER BY stock ASC"
        )
        return [Producto._desde_fila(f) for f in filas]

    def guardar(self):
        if self.id is None:
            self.id = db.ejecutar(
                "INSERT INTO productos (nombre, descripcion, categoria, precio, "
                "stock, stock_minimo) VALUES (?, ?, ?, ?, ?, ?)",
                (self.nombre, self.descripcion, self.categoria, self.precio,
                 self.stock, self.stock_minimo),
            )
        else:
            db.ejecutar(
                "UPDATE productos SET nombre=?, descripcion=?, categoria=?, "
                "precio=?, stock=?, stock_minimo=? WHERE id=?",
                (self.nombre, self.descripcion, self.categoria, self.precio,
                 self.stock, self.stock_minimo, self.id),
            )
        return self

    def actualizar_stock_en_bd(self):
        """Persiste solo el campo stock (usado tras una venta)."""
        db.ejecutar("UPDATE productos SET stock = ? WHERE id = ?", (self.stock, self.id))

    @staticmethod
    def eliminar(producto_id):
        db.ejecutar("DELETE FROM productos WHERE id = ?", (producto_id,))
