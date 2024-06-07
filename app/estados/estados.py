from flask import Blueprint, request,jsonify
#from bson.json_util import dumps
from datetime import datetime
from app.instancia_mysql import mysql

estado=Blueprint("est",__name__)

@estado.route('/estados', methods=['GET','POST'])
def estado_s():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM estados")
        responsa = cursor.fetchall()
        result = []
        for d in responsa:
            result.append({'idEstado': d[0], 'nombre': d[1], 'paisId': d[2]})
        return jsonify(result)

    if request.method == 'POST':
        data = request.get_json()
        nombre = data['nombre']
        paisId = data['paisId']
        cursor.execute("INSERT INTO estados (nombre, paisId) VALUES (%s, %s)", (nombre, paisId))
        conn.commit()
        return jsonify({'res': 'ok'}), 200