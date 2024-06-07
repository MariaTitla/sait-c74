from flask import Blueprint, request,jsonify, current_app
#from bson.json_util import dumps
from datetime import datetime
from app.instancia_mysql import mysql

import pymysql


deptos=Blueprint("dep",__name__)

@deptos.route('/departamentos', methods=['GET', 'POST', 'PUT','DELETE'])
def get_deptos():
    conn = mysql.connect()
    cursor = conn.cursor()
    

    if request.method == 'GET':
        cursor.execute("SELECT * FROM departamentos")
        departamentos = cursor.fetchall()
        result = []
        for d in departamentos:
            result.append({'idDepartamento': d[0], 'departamento': d[1], 'responsableId': d[2]})
        return jsonify(result)

    if request.method == 'POST':
        data = request.get_json()
        depa = data['departamento']
        respId = data['responsableId']
        cursor.execute("INSERT INTO departamentos (departamento, responsableId) VALUES (%s, %s)", 
                       (depa, respId))
        conn.commit()
        return jsonify({'res': 'ok'}), 200
    
    if request.method == 'PUT':
        data = request.get_json()
        id_departamento = data['idDepartamento']
        depa = data['departamento']

        try:
            sql="UPDATE departamentos SET departamento = %s WHERE idDepartamento = %s" 
            cursor.execute(sql, (depa, id_departamento))
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

    if request.method == 'DELETE':
        conn = mysql.connect()
        cursor = conn.cursor()
        data = request.get_json()
        id_ = data['idDepartamento']
        
        
        if not id_:
            return jsonify({"error": "ID is required"}), 400
        
        try:
            # Consulta SQL para eliminar el empleado
            sql = "DELETE FROM departamentos WHERE idDepartamento = %s"
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
