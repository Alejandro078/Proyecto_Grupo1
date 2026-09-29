"""Modelo Empleado: también hereda de Persona (misma base, rol distinto)."""

from app.models.persona import Persona
from app.models.database import db


class Empleado(Persona):
    def __init__(self, nombre, documento, cargo="Vendedor", id=None, fecha_registro=None):
        super().__init__(nombre, documento)
        self.cargo = cargo
        self.id = id
        self.fecha_registro = fecha_registro

    def obtener_rol(self):
        # Misma interfaz que Cliente.obtener_rol(), distinta implementación
        return f"Empleado - {self.cargo}"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "documento": self.documento,
            "cargo": self.cargo,
            "fecha_registro": self.fecha_registro,
        }

    @staticmethod
    def _desde_fila(fila):
        if not fila:
            return None
        return Empleado(
            id=fila["id"], nombre=fila["nombre"], documento=fila["documento"],
            cargo=fila["cargo"], fecha_registro=fila["fecha_registro"],
        )

    @staticmethod
    def obtener_todos():
        filas = db.consultar_todas("SELECT * FROM empleados ORDER BY nombre")
        return [Empleado._desde_fila(f) for f in filas]

    @staticmethod
    def obtener_por_id(empleado_id):
        fila = db.consultar_una("SELECT * FROM empleados WHERE id = ?", (empleado_id,))
        return Empleado._desde_fila(fila)
