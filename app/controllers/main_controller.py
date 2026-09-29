"""Controlador del dashboard principal."""

from flask import Blueprint, render_template

from app.models.venta import Venta
from app.models.producto import Producto

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def dashboard():
    resumen = Venta.resumen_dashboard()
    productos_stock_bajo = Producto.con_stock_bajo()
    ultimas_ventas = Venta.obtener_todas()[:5]
    return render_template(
        "index.html",
        resumen=resumen,
        productos_stock_bajo=productos_stock_bajo,
        ultimas_ventas=ultimas_ventas,
    )
