from flask import Blueprint, request,jsonify
#from bson.json_util import dumps
from datetime import datetime
from app.instancia_mysql import mysql
import pymysql

rol=Blueprint("rol",__name__)

@rol.route('/roles', methods=['GET', 'POST', 'PUT'])
def rol_es():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        if conn:
            try:
                cursor.execute("SELECT * FROM roles")
                responsa = cursor.fetchall()
                result = []
                for d in responsa:
                    result.append({'idRol': d[0], 'tipoRol': d[1], 'status': d[2]})
                return jsonify(result)
            except pymysql.MySQLError as e:
                print(f"Error during database query: {e}")
                return jsonify({"error": str(e)}), 500
            finally:
                conn.close()
        else:
            return jsonify({"error": "Failed to connect to database"}), 500
        

    if request.method == 'POST':
        if conn:
            try:
                data = request.get_json()
                tipoRol = data["tipoRol"]
                status="activo"
                cursor.execute("INSERT INTO roles (tipoRol, status) VALUES (%s, %s)", (tipoRol,status))
                conn.commit()
                return jsonify({'res': 'ok'}), 200
            except pymysql.MySQLError as e:
                print(f"Error during database query: {e}")
                return jsonify({"error": str(e)}), 500
            finally:
                conn.close()
        else:
            return jsonify({"error": "Failed to connect to database"}), 500
        

    if request.method == 'PUT':
        data = request.get_json()
        id_rol = data['idRol']
        tipo_rol = data['tipoRol']
        status = data['status']
        cursor.execute("UPDATE roles SET tipoRol = %s, status = %s WHERE idRol = %s", (tipo_rol, status, id_rol))
        conn.commit()
        return jsonify({'message': 'Rol updated successfully!'}), 200
