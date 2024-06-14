from flask import Flask
from app.instancia_mysql import mysql

import os
import dotenv

def create_app():
    app=Flask(__name__)

   # cargamos las variables de entorno
    dotenv.load_dotenv()  

    # leemos las varaibles de entorno
    usuariodb = os.getenv('USER')
    passwd = os.getenv('PASSWD')
    host=os.getenv('MYSQL_HOST')
    db=os.getenv('MYSQL_DB')
    puerto=os.getenv('MYSQL_DB')

    app.config["MYSQL_DATABASE_HOSTNAME"]=host
    app.config["MYSQL_DATABASE_USER"]= usuariodb  
    app.config["MYSQL_DATABASE_PASSWORD"]=passwd  
    app.config['MYSQL_DATABASE_DB']=db
    app.config['MYSQL_DATABASE_PORT']=puerto 
    
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
        
        
        mysql.init_app(app)
        print("usu",usuariodb)
        return app
