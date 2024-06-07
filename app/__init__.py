from flask import Flask
from app  import config
from app.instancia_mysql import mysql




def create_app():
    app=Flask(__name__)

   
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rosa54ROSA@localhost/saitutpdb'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#  app.config['SQLALCHEMY_DATABASE_URI']=(
 #   'mysql+pymysql://USER:PASSWORD@/DATABASE_NAME?unix_socket=/cloudsql/PROJECT_ID:REGION:INSTANCE_NAME'
#) 


    app.config["MYSQL_DATABASE_HOSTNAME"]=config.MYSQL_HOST
    app.config["MYSQL_DATABASE_USER"]=config.MYSQL_USER
    app.config["MYSQL_DATABASE_PASSWORD"]=config.MYSQL_PASSWORD
    app.config['MYSQL_DATABASE_DB']=config.MYSQL_DB
    app.config['MYSQL_DATABASE_PORT']=config.MYSQL_PORT 
    #app.config_class['MYSQL_DATABASE_CHARSET']=config.MYSQL_DATABASE_CHARSET

    # Inicializa SQLAlchemy
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
        return app
