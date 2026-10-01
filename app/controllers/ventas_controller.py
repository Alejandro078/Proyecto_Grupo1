"""Controlador de ventas: es el que más lógica de negocio concentra
(valida stock, aplica descuentos y descuenta inventario en una sola
operación transaccional)."""

from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.models.venta import Venta, DetalleVenta
from app.models.producto import Producto
from app.models.cliente import Cliente
from app.models.empleado import Empleado
from app.models.descuento import obtener_estrategia
from app.utils.exceptions import ErrorInventario

ventas_bp = Blueprint("ventas", __name__, url_prefix="/ventas")


@ventas_bp.route("/")
def listar():
    ventas = Venta.obtener_todas()
    return render_template("ventas/listar.html", ventas=ventas)


@ventas_bp.route("/nueva", methods=["GET", "POST"])
def nueva():
    if request.method == "POST":
        try:
            cliente_id = request.form.get("cliente_id") or None
            empleado_id = request.form.get("empleado_id") or None
            tipo_descuento = request.form.get("tipo_descuento", "ninguno")
            porcentaje = request.form.get("porcentaje_descuento") or None

            productos_ids = request.form.getlist("producto_id[]")
            cantidades = request.form.getlist("cantidad[]")

            detalles = []
            for pid, cant in zip(productos_ids, cantidades):
                if not pid or not cant:
                    continue
                detalles.append(DetalleVenta(producto_id=int(pid), cantidad=int(cant), precio_unitario=0))

            estrategia = obtener_estrategia(tipo_descuento, porcentaje)

            venta = Venta(
                cliente_id=int(cliente_id) if cliente_id else None,
                empleado_id=int(empleado_id) if empleado_id else None,
                detalles=detalles,
                estrategia_descuento=estrategia,
            )
            venta.registrar()

            flash(f"Venta #{venta.id} registrada. Total: ${venta.total:,.0f}", "success")
            return redirect(url_for("ventas.detalle", venta_id=venta.id))

        except ErrorInventario as e:
            flash(str(e), "danger")
        except (ValueError, TypeError):
            flash("Revisa los productos y cantidades ingresadas.", "danger")

    clientes = Cliente.obtener_todos()
    empleados = Empleado.obtener_todos()
    productos = Producto.obtener_todos()
    return render_template(
        "ventas/formulario.html", clientes=clientes, empleados=empleados, productos=productos
    )


@ventas_bp.route("/<int:venta_id>")
def detalle(venta_id):
    venta, detalles = Venta.obtener_por_id(venta_id)
    if venta is None:
        flash("Venta no encontrada.", "danger")
        return redirect(url_for("ventas.listar"))
    return render_template("ventas/detalle.html", venta=venta, detalles=detalles)
