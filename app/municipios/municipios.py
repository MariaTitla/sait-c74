from flask import Blueprint, request,jsonify
#from bson.json_util import dumps
from datetime import datetime
from app.instancia_mysql import mysql
import pymysql

municipio=Blueprint("muni",__name__)

@municipio.route('/municipios', methods=['GET','POST', 'DELETE'])
def municipio_s():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM municipios")
        responsa = cursor.fetchall()
        result = []
        for d in responsa:
            result.append({'idMunicipio': d[0], 'nombre': d[1], 'estadoId': d[2]})
        return jsonify(result)

    if request.method == 'POST':
        data = request.get_json()
        nombre = data['nombre']
        estadoId = data['estadoId']
        cursor.execute("INSERT INTO municipios (nombre, estadoId) VALUES (%s, %s)", (nombre, estadoId))
        conn.commit()
        return jsonify({'res': 'ok'}), 200
    
    if request.method == 'DELETE':
        conn = mysql.connect()
        cursor = conn.cursor()
        data = request.get_json()
        id_ = data['idMunicipio']
        
        
        if not id_:
            return jsonify({"error": "ID is required"}), 400
        
        try:
            # Consulta SQL para eliminar el empleado
            sql = "DELETE FROM municipios WHERE idMunicipio = %s"
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
