from flask import Flask
from app.instancia_mysql import mysql

import os
import sqlalchemy
import dotenv

import os
import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dotenv

# Cargar las variables de entorno desde el archivo .env
dotenv.load_dotenv(override=True)

# Inicializar SQLAlchemy
db = SQLAlchemy()

def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a TCP connection pool for a Cloud SQL instance of MySQL."""
    db_host = os.getenv("INSTANCE_HOST")  # e.g. '127.0.0.1'
    db_user = os.getenv("DB_USER")  # e.g. 'my-db-user'
    db_pass = os.getenv("DB_PASS")  # e.g. 'my-db-password'
    db_name = os.getenv("DB_NAME")  # e.g. 'my-database'
    db_port = os.getenv("DB_PORT")  # e.g. 3306

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        ),
    )
    return pool

def create_app():
    app = Flask(__name__)

    # Configuración de SQLAlchemy para usar la conexión TCP
    app.config['SQLALCHEMY_DATABASE_URI'] = str(connect_tcp_socket().url)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar la aplicación con SQLAlchemy
    db.init_app(app)

    # Registrar Blueprints
    with app.app_context():
        from app.responsablesDepto.responsablesDepto import respon
        from app.paises.paises import pais
        from app.estados.estados import estado
        from app.municipios.municipios import municipio
        from app.direcciones.direcciones import direccion
        from app.sindicato.sindicato import sindicato
        from app.oficioc74.oficioc74 import oficio
        from app.departamentos.departamentos import deptos
        from app.empleados.empleados import empleado
        from app.usuarios.usuarios import usuario
        from app.roles.roles import rol

        app.register_blueprint(respon)
        app.register_blueprint(pais)
        app.register_blueprint(estado)
        app.register_blueprint(municipio)
        app.register_blueprint(direccion)
        app.register_blueprint(sindicato)
        app.register_blueprint(oficio)
        app.register_blueprint(deptos)
        app.register_blueprint(empleado)
        app.register_blueprint(usuario)
        app.register_blueprint(rol)

        return app
