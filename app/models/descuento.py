"""
Estrategias de descuento (patrón Strategy).

Todas comparten la misma interfaz (calcular), pero cada una calcula el
descuento de forma distinta: es POLIMORFISMO aplicado a una regla de
negocio real, no solo a las clases Persona.
"""

from abc import ABC, abstractmethod


class EstrategiaDescuento(ABC):
    @abstractmethod
    def calcular(self, subtotal):
        """Devuelve el valor del descuento (no el total) para un subtotal dado."""
        raise NotImplementedError

    @property
    @abstractmethod
    def nombre(self):
        raise NotImplementedError


class SinDescuento(EstrategiaDescuento):
    def calcular(self, subtotal):
        return 0.0

    @property
    def nombre(self):
        return "ninguno"


class DescuentoPorcentaje(EstrategiaDescuento):
    """Descuento fijo (ej. 10%) sin importar el monto de la compra."""

    def __init__(self, porcentaje):
        if not (0 <= porcentaje <= 100):
            raise ValueError("El porcentaje debe estar entre 0 y 100.")
        self.porcentaje = porcentaje

    def calcular(self, subtotal):
        return round(subtotal * (self.porcentaje / 100), 2)

    @property
    def nombre(self):
        return f"porcentaje_{self.porcentaje}"


class DescuentoClienteFrecuente(EstrategiaDescuento):
    """Descuento escalonado: entre más grande la compra, mayor el %."""

    def calcular(self, subtotal):
        if subtotal >= 200000:
            porcentaje = 15
        elif subtotal >= 100000:
            porcentaje = 10
        elif subtotal >= 50000:
            porcentaje = 5
        else:
            porcentaje = 0
        return round(subtotal * (porcentaje / 100), 2)

    @property
    def nombre(self):
        return "cliente_frecuente"


ESTRATEGIAS_DISPONIBLES = {
    "ninguno": SinDescuento,
    "cliente_frecuente": DescuentoClienteFrecuente,
}


def obtener_estrategia(tipo, porcentaje=None):
    """Fábrica simple: construye la estrategia según el tipo pedido en el formulario."""
    if tipo == "porcentaje" and porcentaje is not None:
        return DescuentoPorcentaje(float(porcentaje))
    clase = ESTRATEGIAS_DISPONIBLES.get(tipo, SinDescuento)
    return clase()
