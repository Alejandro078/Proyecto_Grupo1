"""
Excepciones personalizadas del sistema.

Centralizar las excepciones en un módulo propio permite manejar cada
tipo de error de forma específica en los controladores (try/except),
en vez de capturar Exception genérica.
"""


class ErrorInventario(Exception):
    """Excepción base para todos los errores propios del sistema."""
    pass


class StockInsuficienteError(ErrorInventario):
    """Se lanza cuando se intenta vender más unidades de las disponibles."""

    def __init__(self, producto_nombre, stock_disponible, cantidad_solicitada):
        self.producto_nombre = producto_nombre
        self.stock_disponible = stock_disponible
        self.cantidad_solicitada = cantidad_solicitada
        mensaje = (
            f'Stock insuficiente para "{producto_nombre}": '
            f'disponible {stock_disponible}, solicitado {cantidad_solicitada}.'
        )
        super().__init__(mensaje)


class ProductoNoEncontradoError(ErrorInventario):
    """Se lanza cuando se busca un producto que no existe."""

    def __init__(self, producto_id):
        super().__init__(f"No se encontró el producto con id {producto_id}.")


class ClienteNoEncontradoError(ErrorInventario):
    """Se lanza cuando se busca un cliente que no existe."""

    def __init__(self, cliente_id):
        super().__init__(f"No se encontró el cliente con id {cliente_id}.")


class DatosInvalidosError(ErrorInventario):
    """Se lanza cuando los datos de un formulario no pasan la validación."""

    def __init__(self, mensaje):
        super().__init__(mensaje)


class VentaSinDetalleError(ErrorInventario):
    """Se lanza al intentar registrar una venta sin ningún producto."""

    def __init__(self):
        super().__init__("La venta debe tener al menos un producto.")
