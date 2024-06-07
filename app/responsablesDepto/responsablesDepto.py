from flask import Blueprint, request,jsonify
#from bson.json_util import dumps
from datetime import datetime
from app.instancia_mysql import mysql
import pymysql

respon=Blueprint("resp",__name__)

@respon.route('/responsables', methods=['GET','POST', 'DELETE', 'PUT'])
def repsonsables_deptos():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        if conn:
            try:
                cursor.execute("SELECT * FROM responsablesDepto")
                responsa = cursor.fetchall()
                result = []
                for d in responsa:
                    result.append({'idResponsable': d[0], 'tituloResponsable': d[1], 'nombreResponsable': d[2], 'puesto':d[3]})
                return jsonify(result)
            except pymysql.MySQLError as e:
                print(f"Error during database query: {e}")
                return jsonify({"error": str(e)}), 500
            finally:
                conn.close()
        else:
            return jsonify({"error": "Failed to connect to database"}), 500
        

    if request.method == 'POST':
        data = request.get_json()
        titulo = data['titulo']
        nombre = data['nombre']
        puesto = data['puesto']
        if conn:
            try:
                cursor.execute("INSERT INTO responsablesDepto (tituloResponsable,nombreResponsable, puesto, fechaRegistro) VALUES (%s, %s, %s,%s)", (titulo,nombre, puesto, datetime.now()))
                conn.commit()
                return jsonify({'res': 'ok'}), 200
            except pymysql.MySQLError as e:
                print(f"Error during database query: {e}")
                return jsonify({"error": str(e)}), 500
            finally:
                conn.close()
        else:
            return jsonify({"error": "Failed to connect to database"}), 500
        
    
    if request.method == 'DELETE':
        conn = mysql.connect()
        cursor = conn.cursor()
        data = request.get_json()
        id_ = data['idResponsable']
        
        
        if not id_:
            return jsonify({"error": "ID is required"}), 400
        
        try:
            # Consulta SQL para eliminar el empleado
            sql = "DELETE FROM responsablesDepto WHERE idResponsable = %s"
            cursor.execute(sql, (id_,))
            conn.commit()
            
            # Verificar si se eliminó alguna fila
            if cursor.rowcount == 0:
                return jsonify({"res": "fallo"}), 404
            
            return jsonify({"res": "ok"}), 200
        except pymysql.MySQLError as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    if request.method == 'PUT':
        data = request.get_json()
        id_ = data['idResponsable']
        titulo = data['titulo']
        nombre = data['nombre']
        puesto = data['puesto']
        
    
        if not id_ or not titulo or not nombre or not puesto:
            return jsonify({"error": "ID,  is required"}), 400
        
        try:
            # Consulta SQL para actualizar el email y el password
            sql = "UPDATE responsablesDepto SET  tituloResponsable= %s,nombreResponsable= %s, puesto= %s WHERE idResponsable = %s"
            cursor.execute(sql, (titulo, nombre, puesto, id_))
            conn.commit()
            
            # Verificar si se actualizó alguna fila
            if cursor.rowcount == 0:
                return jsonify({"message": "No user found with the given ID"}), 404
            
            return jsonify({"res": "ok"}), 200
        except pymysql.MySQLError as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()


