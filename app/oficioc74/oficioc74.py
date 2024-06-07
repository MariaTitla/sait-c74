from flask import Blueprint, request,jsonify
#from bson.json_util import dumps
from datetime import datetime
from app.instancia_mysql import mysql
import pymysql

oficio=Blueprint("ofi",__name__)

@oficio.route('/oficios', methods=['GET', 'POST', 'DELETE'])
def oficio_s():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        if conn:
            try:
                cursor.execute("SELECT * FROM oficiosC74")
                responsa = cursor.fetchall()
                #print("h",responsa)
                result = []
                for d in responsa:
                    result.append({
                        'idOficio': d[0], 'id': d[1], 'folio': d[2], 'fecha1': d[3], 'fecha2': d[4], 'fecha3': d[5], 
                        'nombre': d[6], 'apellidoPaterno': d[7], 'apellidoMaterno': d[8], 'departamento': d[9], 
                        'tituloJefeRH':d[10],'jefeRH': d[11], 'fechaSolicitud': d[12], 
                        'tituloResponsable':d[13],'nombreResponsable': d[14], 
                        'puestoResponsable': d[15], 'tituloSecretarioGeneral': d[16],'nombreSecretarioGeneral': d[17]
                        
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
        id = data['id']
        folio = data['folio']
        fecha_str1 = data['fecha1']
        #2024-11-13
        if fecha_str1 != "":
            fecha1=datetime.strptime(fecha_str1, "%Y-%m-%d")
       
        fecha_str2 = data['fecha2']
        if fecha_str2!="":
            fecha2=datetime.strptime(fecha_str2, "%Y-%m-%d")
        
        fecha_str3 = data['fecha3']
        if fecha_str3 !="":
            fecha3=datetime.strptime(fecha_str3, "%Y-%m-%d")
        else:
            fecha3=None
        nombre = data['nombre']
        apellidoPa = data['apellidoPaterno']
        apellidoMa = data['apellidoMaterno']
        depa = data['departamento']
        jefeRH = data['jefeRH']
        tit=data['titulojefeRH']
        tituloResponsable=data['tituloResponsable']
        nombreResp = data['nombreResponsable']
        puestoResp = data['puestoResponsable']
        tituloSecretarioGeneral=data['tituloSecretarioGeneral']
        nombreSecreGral = data['nombreSecretarioGeneral']
        empleadoId=data['empleadoId']
        fecha_solic=datetime.now()
        if conn:
            try:
                cursor.execute(
                    "INSERT INTO oficiosC74 (id, folio, fecha1, fecha2, fecha3, nombre, apellidoPaterno, apellidoMaterno, departamento, tituloJefeRH, jefeRH, fechaSolicitud,  tituloResponsable,nombreResponsable, puestoResponsable, tituloSecretarioGeneral, nombreSecretarioGeneral, empleadoId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s,%s,%s,%s)",
                                            (id, folio, fecha1, fecha2, fecha3, nombre, apellidoPa,      apellidoMa,     depa,    tit,   jefeRH,    fecha_solic, tituloResponsable, nombreResp, puestoResp, tituloSecretarioGeneral,nombreSecreGral, empleadoId)
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
        id_oficio = data['idOficio']
        
        
        if not id_oficio:
            return jsonify({"error": "ID is required"}), 400
        
        try:
            # Consulta SQL para eliminar el empleado
            sql = "DELETE FROM oficiosc74 WHERE idOficio = %s"
            cursor.execute(sql, (id_oficio,))
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



   

@oficio.route('/getOficiosByIdEmpleado/<int:empleado_id>', methods=['GET'])
def obtener_oficios(empleado_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    #data = request.get_json()
    #empleado_id = data['empleadoId']
    
    
    if not empleado_id:
        return jsonify({"error": "empleadoId is required"}), 400
    
    try:
        # Consulta SQL para obtener las tuplas
        sql = """
            SELECT id, folio, fecha1, fecha2, fecha3, nombre, apellidoPaterno, apellidoMaterno, fechaSolicitud
            FROM oficiosC74
            WHERE empleadoId = %s
              AND YEAR(fechaSolicitud) = YEAR(CURDATE());
        """
        cursor.execute(sql, (empleado_id,))
        result = cursor.fetchall()
        result1 = []
        for d in result:
            result1.append({
                'id': d[0], 'folio': d[1], 'fecha1': d[2], 
                'fecha2': d[3], 'fecha3': d[4], 
                'nombre': d[5], 'apellidoPaterno': d[6],
                 'apellidoMaterno': d[7], 
                'fechaSolicitud': d[8]
                    
            })
        return jsonify(result1)
        #return jsonify(result), 200
    except pymysql.MySQLError as e:
        error_code = e.args[0]
        error_message = e.args[1]
        print(f"Error during database query: {error_code}, {error_message}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
