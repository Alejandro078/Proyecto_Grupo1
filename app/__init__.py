"""Application factory de Flask."""

from flask import Flask, render_template

from app.models.database import db


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "clave-secreta-proyecto-universitario-cambiar-en-produccion"

    # Inicializa la base de datos (crea el archivo .db si no existe)
    db.inicializar()

    # Registro de blueprints (controladores)
    from app.controllers.main_controller import main_bp
    from app.controllers.productos_controller import productos_bp
    from app.controllers.clientes_controller import clientes_bp
    from app.controllers.ventas_controller import ventas_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(ventas_bp)

    # Manejo global de errores no capturados en un controlador específico
    @app.errorhandler(404)
    def pagina_no_encontrada(error):
        return render_template("errores/404.html"), 404

    @app.errorhandler(500)
    def error_interno(error):
        return render_template("errores/500.html"), 500

    return app
