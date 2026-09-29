"""
Capa de acceso a datos.

La clase Database encapsula toda la interacción con SQLite: nadie fuera
de este módulo debería abrir una conexión directamente (encapsulamiento).
"""

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "inventario.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


class Database:
    """Encapsula la conexión a SQLite y expone operaciones de bajo nivel."""

    _instancia = None

    def __new__(cls):
        # Patrón singleton simple: una sola instancia de acceso a datos.
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def obtener_conexion(self):
        conexion = sqlite3.connect(DB_PATH)
        conexion.row_factory = sqlite3.Row
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    def inicializar(self, forzar=False):
        """Crea la base de datos a partir de schema.sql si no existe todavía."""
        existe = os.path.exists(DB_PATH)
        if existe and not forzar:
            return
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            script = f.read()
        conexion = sqlite3.connect(DB_PATH)
        try:
            conexion.executescript(script)
            conexion.commit()
        finally:
            conexion.close()

    def ejecutar(self, consulta, parametros=()):
        """INSERT/UPDATE/DELETE. Devuelve el id de la última fila insertada."""
        conexion = self.obtener_conexion()
        try:
            cursor = conexion.execute(consulta, parametros)
            conexion.commit()
            return cursor.lastrowid
        finally:
            conexion.close()

    def consultar_una(self, consulta, parametros=()):
        conexion = self.obtener_conexion()
        try:
            fila = conexion.execute(consulta, parametros).fetchone()
            return dict(fila) if fila else None
        finally:
            conexion.close()

    def consultar_todas(self, consulta, parametros=()):
        conexion = self.obtener_conexion()
        try:
            filas = conexion.execute(consulta, parametros).fetchall()
            return [dict(f) for f in filas]
        finally:
            conexion.close()


db = Database()
