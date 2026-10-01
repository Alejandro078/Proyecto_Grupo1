"""Controlador CRUD de clientes."""

from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.models.cliente import Cliente
from app.utils.exceptions import ErrorInventario, ClienteNoEncontradoError
from app.utils.validators import validar_texto_no_vacio, validar_documento

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@clientes_bp.route("/")
def listar():
    busqueda = request.args.get("q", "").strip() or None
    clientes = Cliente.obtener_todos(busqueda=busqueda)
    return render_template("clientes/listar.html", clientes=clientes, busqueda=busqueda or "")


@clientes_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        try:
            nombre = validar_texto_no_vacio(request.form.get("nombre"), "nombre")
            documento = validar_documento(request.form.get("documento"))
            email = request.form.get("email", "").strip()
            telefono = request.form.get("telefono", "").strip()
            direccion = request.form.get("direccion", "").strip()

            cliente = Cliente(
                nombre=nombre, documento=documento, email=email,
                telefono=telefono, direccion=direccion,
            )
            cliente.guardar()
            flash(f'Cliente "{nombre}" registrado correctamente.', "success")
            return redirect(url_for("clientes.listar"))
        except ErrorInventario as e:
            flash(str(e), "danger")
        except ValueError as e:
            flash(str(e), "danger")
        except Exception as e:
            # Ej: UNIQUE constraint failed por documento duplicado
            if "UNIQUE" in str(e):
                flash("Ya existe un cliente registrado con ese documento.", "danger")
            else:
                flash("Ocurrió un error inesperado al guardar el cliente.", "danger")

    return render_template("clientes/formulario.html", cliente=None)


@clientes_bp.route("/<int:cliente_id>/editar", methods=["GET", "POST"])
def editar(cliente_id):
    try:
        cliente = Cliente.obtener_por_id(cliente_id)
    except ClienteNoEncontradoError as e:
        flash(str(e), "danger")
        return redirect(url_for("clientes.listar"))

    if request.method == "POST":
        try:
            cliente.nombre = validar_texto_no_vacio(request.form.get("nombre"), "nombre")
            cliente.documento = validar_documento(request.form.get("documento"))
            cliente.email = request.form.get("email", "").strip()
            cliente.telefono = request.form.get("telefono", "").strip()
            cliente.direccion = request.form.get("direccion", "").strip()
            cliente.guardar()
            flash(f'Cliente "{cliente.nombre}" actualizado.', "success")
            return redirect(url_for("clientes.listar"))
        except ErrorInventario as e:
            flash(str(e), "danger")
        except ValueError as e:
            flash(str(e), "danger")
        except Exception as e:
            if "UNIQUE" in str(e):
                flash("Ya existe un cliente registrado con ese documento.", "danger")
            else:
                flash("Ocurrió un error inesperado al actualizar el cliente.", "danger")

    return render_template("clientes/formulario.html", cliente=cliente)


@clientes_bp.route("/<int:cliente_id>/eliminar", methods=["POST"])
def eliminar(cliente_id):
    try:
        Cliente.obtener_por_id(cliente_id)
        Cliente.eliminar(cliente_id)
        flash("Cliente eliminado.", "success")
    except ErrorInventario as e:
        flash(str(e), "danger")
    return redirect(url_for("clientes.listar"))
