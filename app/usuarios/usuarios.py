from flask import Blueprint, request,jsonify
#from bson.json_util import dumps
from datetime import datetime
from app.instancia_mysql import mysql
import pymysql

usuario=Blueprint("usu",__name__)

@usuario.route('/usuarios', methods=['GET', 'POST','PUT', 'DELETE'])
def usuario_s():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        if conn:
            try:
                cursor.execute("SELECT * FROM usuarios")
                responsa = cursor.fetchall()
                result = []
                for d in responsa:
                    result.append({'idUsuario': d[0], 'id': d[1], 'email': d[2], 'status': d[3], 'fechaRegistro': d[4], 'rolId': d[5]})
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
        id = data['id']
        email=  data['email']
        email=email.lower()
        status = data['status']
        rolId = data['rolId']
        if conn:
            try:
                cursor.execute("INSERT INTO usuarios (id, email, status, fechaRegistro, rolId) VALUES (%s, %s, %s, %s, %s)", 
                            (id, email, status, datetime.now(), rolId))
                conn.commit()
                return jsonify({'resp': 'ok'}), 201
            except pymysql.MySQLError as e:
                error_code = e.args[0]
                error_message = e.args[1]

                if error_code == 1062:
                    if "for key 'email'" in error_message:
                        return jsonify({"error": "email Duplicado"}), 409
                    elif "for key 'id'" in error_message:
                        return jsonify({"error": "id Duplicado"}), 409
                else:
                    print(f"Error during database query: {e}")
                    return jsonify({"error": str(e)}), 500
                
                #"error": "(1062, \"Duplicate entry 'paco' for key 'email'\")"
                #"error": "(1062, \"Duplicate entry '33' for key 'id'\")"
            finally:
                conn.close()
        else:
            return jsonify({"error": "Failed to connect to database"}), 500
        
    if request.method == 'DELETE':
        conn = mysql.connect()
        cursor = conn.cursor()
        data = request.get_json()
        id_usuario = data['idUsuario']
        
        
        if not id_usuario:
            return jsonify({"error": "ID is required"}), 400
        
        try:
            # Consulta SQL para eliminar el empleado
            sql = "DELETE FROM usuarios WHERE idUsuario = %s"
            cursor.execute(sql, (id_usuario,))
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
        id_usuario = data['idUsuario']
        nuevo_id = data['id']
        nuevo_email = data['email']
        
    
        if not id_usuario or not nuevo_email or not nuevo_id:
            return jsonify({"error": "ID, email, and id usuario are required"}), 400
        
        try:
            # Consulta SQL para actualizar el email y el password
            sql = "UPDATE usuarios SET email = %s, id = %s WHERE idUsuario = %s"
            cursor.execute(sql, (nuevo_email, nuevo_id, id_usuario))
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

@usuario.route('/login', methods=['GET'])
def iniciar_sesion():
    conn = mysql.connect()
    cursor = conn.cursor()
    data = request.get_json()
    id = data['id']
    email = data['email']

    if conn:
        try:
            sql_query1 = "SELECT * FROM usuarios WHERE id = %s"
            #sql_query2 = "SELECT * FROM usuarios WHERE email = %s"
            
            cursor.execute(sql_query1, (id))
            result = cursor.fetchone()
            print(result)
            
            if cursor.rowcount == 0:
                    return jsonify({"res": "id incorrecto"}), 200
            else:
                if result[2]==email:
                        #return jsonify({"res": "id"}), 200
                        result1 = []
                        result1.append({'idUsuario': result[0], 'id': result[1], 'email': result[2], 'status': result[3], 'fechaRegistro':result[4], 'rolId': str(result[5])})
                        
                        # for d in result:
                        #     result1.append({'idUsuario': d[0], 'id': d[1], 'email': d[2], 'status': d[3],  'rolId': str(d[4])})
                        return jsonify(result1)
                    
                else:
                    return jsonify({"res": "email incorrecto"}), 200

        except pymysql.MySQLError as e:
                print(f"Error during database query: {e}")
                return jsonify({"error": str(e)}), 500
        finally:
                conn.close()
    else:
            return jsonify({"error": "Failed to connect to database"}), 500
        