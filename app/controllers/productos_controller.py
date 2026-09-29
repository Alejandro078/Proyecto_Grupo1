"""Controlador CRUD de productos."""

from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.models.producto import Producto
from app.utils.exceptions import ErrorInventario, ProductoNoEncontradoError
from app.utils.validators import validar_texto_no_vacio, validar_numero_positivo, validar_entero_positivo

productos_bp = Blueprint("productos", __name__, url_prefix="/productos")


@productos_bp.route("/")
def listar():
    busqueda = request.args.get("q", "").strip() or None
    categoria = request.args.get("categoria", "").strip() or None
    productos = Producto.obtener_todos(busqueda=busqueda, categoria=categoria)
    categorias = Producto.obtener_categorias()
    return render_template(
        "productos/listar.html", productos=productos, categorias=categorias,
        busqueda=busqueda or "", categoria_actual=categoria or "",
    )


@productos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        try:
            nombre = validar_texto_no_vacio(request.form.get("nombre"), "nombre")
            precio = validar_numero_positivo(request.form.get("precio"), "precio", permitir_cero=False)
            stock = validar_entero_positivo(request.form.get("stock", 0), "stock")
            stock_minimo = validar_entero_positivo(request.form.get("stock_minimo", 5), "stock mínimo")
            descripcion = request.form.get("descripcion", "").strip()
            categoria = request.form.get("categoria", "").strip()

            producto = Producto(
                nombre=nombre, precio=precio, stock=stock, stock_minimo=stock_minimo,
                descripcion=descripcion, categoria=categoria,
            )
            producto.guardar()
            flash(f'Producto "{nombre}" creado correctamente.', "success")
            return redirect(url_for("productos.listar"))
        except ErrorInventario as e:
            flash(str(e), "danger")
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("productos/formulario.html", producto=None)


@productos_bp.route("/<int:producto_id>/editar", methods=["GET", "POST"])
def editar(producto_id):
    try:
        producto = Producto.obtener_por_id(producto_id)
    except ProductoNoEncontradoError as e:
        flash(str(e), "danger")
        return redirect(url_for("productos.listar"))

    if request.method == "POST":
        try:
            producto.nombre = validar_texto_no_vacio(request.form.get("nombre"), "nombre")
            producto.precio = validar_numero_positivo(request.form.get("precio"), "precio", permitir_cero=False)
            producto.stock = validar_entero_positivo(request.form.get("stock", 0), "stock")
            producto.stock_minimo = validar_entero_positivo(request.form.get("stock_minimo", 5), "stock mínimo")
            producto.descripcion = request.form.get("descripcion", "").strip()
            producto.categoria = request.form.get("categoria", "").strip()
            producto.guardar()
            flash(f'Producto "{producto.nombre}" actualizado.', "success")
            return redirect(url_for("productos.listar"))
        except ErrorInventario as e:
            flash(str(e), "danger")
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("productos/formulario.html", producto=producto)


@productos_bp.route("/<int:producto_id>/eliminar", methods=["POST"])
def eliminar(producto_id):
    try:
        Producto.obtener_por_id(producto_id)  # valida que exista
        Producto.eliminar(producto_id)
        flash("Producto eliminado.", "success")
    except ErrorInventario as e:
        flash(str(e), "danger")
    return redirect(url_for("productos.listar"))
