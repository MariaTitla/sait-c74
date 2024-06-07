from flask import Blueprint, request,jsonify
#from bson.json_util import dumps
from datetime import datetime
from app.instancia_mysql import mysql
import pymysql

direccion=Blueprint("dir",__name__)

@direccion.route('/direcciones', methods=['GET','POST','PUT', 'DELETE'])
def direccion_es():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM direcciones")
        responsa = cursor.fetchall()
        result = []
        for d in responsa:
            result.append({'idDireccion': d[0], 'calle': d[1], 'numeroExterior': d[2], 'numeroInterior': d[3], 'colonia': d[4], 'cp': d[5], 'municipioId': d[6]})
        return jsonify(result)

    if request.method == 'POST':
        if conn:
            try:
                data = request.get_json()
                calle = data['calle']
                numext = data['numeroExterior']
                numint = data['numeroInterior']
                colonia = data['colonia']
                cp = data['cp']
                muniId = data['municipioId']
                cursor.execute("INSERT INTO direcciones (calle, numeroExterior, numeroInterior, colonia, cp, municipioId) VALUES (%s, %s, %s, %s, %s, %s)", (calle, numext, numint, colonia, cp, muniId))
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
        id_ = data['idDireccion']
        
        
        if not id_:
            return jsonify({"error": "ID is required"}), 400
        
        try:
            # Consulta SQL para eliminar el empleado
            sql = "DELETE FROM direcciones WHERE idDireccion = %s"
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
        idDireccion = data['idDireccion']
        calle = data['calle']
        numext = data['numeroExterior']
        numint = data['numeroInterior']
        colonia = data['colonia']
        cp = data['cp']
        muniId = data['municipioId']
        
    
        if not idDireccion:
            return jsonify({"error": "ID, email, and id usuario are required"}), 400
        
        try:
            # Consulta SQL para actualizar el email y el password
            sql = "UPDATE direcciones SET calle= %s, numeroExterior= %s, numeroInterior= %s, colonia= %s, cp= %s, municipioId = %s WHERE idDireccion= %s"
            cursor.execute(sql, (calle, numext, numint, colonia, cp, muniId, idDireccion))
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
