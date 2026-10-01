"""Modelo Cliente: hereda de Persona y agrega persistencia en SQLite."""

from app.models.persona import Persona
from app.models.database import db
from app.utils.exceptions import ClienteNoEncontradoError


class Cliente(Persona):
    def __init__(self, nombre, documento, email=None, telefono=None,
                 direccion=None, id=None, fecha_registro=None):
        super().__init__(nombre, documento)
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.id = id
        self.fecha_registro = fecha_registro

    def obtener_rol(self):
        # Sobrescritura del método abstracto -> polimorfismo
        return "Cliente"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "documento": self.documento,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "fecha_registro": self.fecha_registro,
        }

    # ---------- Persistencia (patrón Active Record simplificado) ----------

    @staticmethod
    def _desde_fila(fila):
        if not fila:
            return None
        return Cliente(
            id=fila["id"], nombre=fila["nombre"], documento=fila["documento"],
            email=fila["email"], telefono=fila["telefono"],
            direccion=fila["direccion"], fecha_registro=fila["fecha_registro"],
        )

    @staticmethod
    def obtener_todos(busqueda=None):
        if busqueda:
            filas = db.consultar_todas(
                "SELECT * FROM clientes WHERE nombre LIKE ? OR documento LIKE ? "
                "ORDER BY nombre",
                (f"%{busqueda}%", f"%{busqueda}%"),
            )
        else:
            filas = db.consultar_todas("SELECT * FROM clientes ORDER BY nombre")
        return [Cliente._desde_fila(f) for f in filas]

    @staticmethod
    def obtener_por_id(cliente_id):
        fila = db.consultar_una("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
        cliente = Cliente._desde_fila(fila)
        if cliente is None:
            raise ClienteNoEncontradoError(cliente_id)
        return cliente

    def guardar(self):
        if self.id is None:
            self.id = db.ejecutar(
                "INSERT INTO clientes (nombre, documento, email, telefono, direccion) "
                "VALUES (?, ?, ?, ?, ?)",
                (self.nombre, self.documento, self.email, self.telefono, self.direccion),
            )
        else:
            db.ejecutar(
                "UPDATE clientes SET nombre=?, documento=?, email=?, telefono=?, "
                "direccion=? WHERE id=?",
                (self.nombre, self.documento, self.email, self.telefono,
                 self.direccion, self.id),
            )
        return self

    @staticmethod
    def eliminar(cliente_id):
        db.ejecutar("DELETE FROM clientes WHERE id = ?", (cliente_id,))
