from flask import Blueprint, request,jsonify
#from bson.json_util import dumps
from datetime import datetime
from app.instancia_mysql import mysql
import pymysql

sindicato=Blueprint("sindi",__name__)

@sindicato.route('/sindicato', methods=['GET', 'POST', 'PUT', 'DELETE'])
def sindicato_s():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        if conn:
            try:
                cursor.execute("SELECT * FROM sindicato")
                responsa = cursor.fetchall()
                result = []
                for d in responsa:
                    result.append({
                        'id': d[0], 'nombreSecretarioGeneral': d[1], 'FechaEleccion': d[2], 
                        'fotofirma': d[3], 'fotologo': d[4], 'fotoSello': d[5]
                    })
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
        tituloSecretarioGeneral=data['tituloSecretarioGeneral']
        nombre = data['nombreSecretarioGeneral']
        eleccion = data['fechaEleccion']
        firma = data['fotofirma']
        logo = data['fotologo']
        sello = data['fotoSello']
        if conn:
            try:
                cursor.execute(
                    "INSERT INTO sindicato (tituloSecretarioGeneral,nombreSecretarioGeneral, fechaEleccion, fotofirma, fotologo, fotoSello) VALUES (%s, %s, %s, %s, %s,%s)", 
                    (tituloSecretarioGeneral,nombre, eleccion, firma, logo, sello)
                )
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
        id_ = data['idSindicato']
        
        
        if not id_:
            return jsonify({"error": "ID is required"}), 400
        
        try:
            # Consulta SQL para eliminar el empleado
            sql = "DELETE FROM sindicato WHERE id = %s"
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
        if conn:
            try:
                data = request.get_json()
                id_sindicato = data['id']
                nombre = data['nombre']
                firma = data['firma']

                sql="UPDATE sindicato SET nombreSecretarioGeneral = %s, fotofirma = %s WHERE idSindicato = %s"
                cursor.execute(sql, (nombre, firma, logo, id_sindicato))
                conn.commit()
                return jsonify({'res': 'ok'}), 200
            except pymysql.MySQLError as e:
                print(f"Error during database query: {e}")
                return jsonify({"error": str(e)}), 500
            finally:
                conn.close()
        else:
            return jsonify({"error": "Failed to connect to database"}), 500
        