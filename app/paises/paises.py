from flask import Blueprint, request,jsonify
#from bson.json_util import dumps
from datetime import datetime
from app.instancia_mysql import mysql
import pymysql

pais=Blueprint("pai",__name__)

@pais.route('/paises', methods=['GET','POST'])
def pais_es():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        if conn:
            try:
                cursor.execute("SELECT * FROM paises")
                responsa = cursor.fetchall()
                result = []
                for d in responsa:
                    result.append({'idPais': d[0], 'nombre': d[1]})
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
        nombre = data['nombre']
        if conn:
            try:
                cursor.execute("INSERT INTO paises (nombre) VALUES (%s)", (nombre))
                conn.commit()
                return jsonify({'res': 'ok'}), 200
            except pymysql.MySQLError as e:
                print(f"Error during database query: {e}")
                return jsonify({"error": str(e)}), 500
            finally:
                conn.close()
        else:
            return jsonify({"error": "Failed to connect to database"}), 500
        