"""Funciones de validación reutilizadas por los controladores."""

from app.utils.exceptions import DatosInvalidosError


def validar_texto_no_vacio(valor, nombre_campo):
    if valor is None or str(valor).strip() == "":
        raise DatosInvalidosError(f"El campo '{nombre_campo}' es obligatorio.")
    return str(valor).strip()


def validar_numero_positivo(valor, nombre_campo, permitir_cero=True):
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        raise DatosInvalidosError(f"El campo '{nombre_campo}' debe ser un número.")
    if permitir_cero and numero < 0:
        raise DatosInvalidosError(f"El campo '{nombre_campo}' no puede ser negativo.")
    if not permitir_cero and numero <= 0:
        raise DatosInvalidosError(f"El campo '{nombre_campo}' debe ser mayor que cero.")
    return numero


def validar_entero_positivo(valor, nombre_campo, permitir_cero=True):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise DatosInvalidosError(f"El campo '{nombre_campo}' debe ser un número entero.")
    if permitir_cero and numero < 0:
        raise DatosInvalidosError(f"El campo '{nombre_campo}' no puede ser negativo.")
    if not permitir_cero and numero <= 0:
        raise DatosInvalidosError(f"El campo '{nombre_campo}' debe ser mayor que cero.")
    return numero


def validar_documento(valor):
    valor = validar_texto_no_vacio(valor, "documento")
    if not valor.replace(" ", "").isalnum():
        raise DatosInvalidosError("El documento solo puede contener letras y números.")
    return valor
