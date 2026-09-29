"""
Clase base abstracta Persona.

Demuestra ABSTRACCIÓN (no se puede instanciar directamente) y sirve de
base para HERENCIA en Cliente y Empleado. El método obtener_rol() se
sobrescribe en cada subclase, demostrando POLIMORFISMO.
"""

from abc import ABC, abstractmethod


class Persona(ABC):
    def __init__(self, nombre, documento):
        # Atributos "privados" (encapsulamiento) accesibles solo vía @property
        self._nombre = None
        self._documento = None
        self.nombre = nombre          # usa el setter con validación
        self.documento = documento    # usa el setter con validación

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = str(valor).strip()

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El documento no puede estar vacío.")
        self._documento = str(valor).strip()

    @abstractmethod
    def obtener_rol(self):
        """Cada subclase define su propio rol dentro del sistema."""
        raise NotImplementedError

    def presentarse(self):
        # Método concreto que reutiliza el polimorfismo de obtener_rol()
        return f"{self.nombre} ({self.obtener_rol()}) - Documento: {self.documento}"
