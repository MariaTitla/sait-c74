from flask import Blueprint, request,jsonify
#from bson.json_util import dumps
from datetime import datetime
from app.instancia_mysql import mysql
import pymysql

empleado=Blueprint("emp",__name__)

@empleado.route('/empleados', methods=['GET', 'POST', 'DELETE', 'PUT'])
def empleado_s():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        if conn:
            try:
                cursor.execute("SELECT * FROM empleados")
                responsa = cursor.fetchall()
                result = []
                for d in responsa:
                    result.append({
                        'idEmpleado': d[0], 'nombre': d[1], 'apellidoPaterno': d[2], 'apellidoMaterno': d[3], 
                        'telefono': d[4], 'curp': d[5], 'puesto': d[6], 'sexo': d[7], 'fechaContratacion': d[8], 
                        'fechaRegistro': d[9], 'status': d[10], 'usuarioId': d[11], 'departamentoId': d[12]
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
        nombre = data['nombre']
        apellidoPa = data['apellidoPaterno']
        apellidoMa = data['apellidoMaterno']
        tel = data['telefono']
        curp = data['curp']
        puesto = data['puesto']
        sexo = data['sexo']
        fecha_str = data['fechaContratacion']
        fechaCon=datetime.strptime(fecha_str, "%Y-%m-%d") 
        status = data['status']
        usuarioId = data['usuarioId']
        depaId = data['departamentoId']
        direccionId=data['direccionId']


        if conn:
            try:
                cursor.execute(
                    "INSERT INTO empleados (nombre, apellidoPaterno, apellidoMaterno, telefono, curp, puesto, sexo, fechaContratacion, fechaRegistro, status, usuarioId, departamentoId, direccionId) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)", 
                    (nombre, apellidoPa, apellidoMa, tel, curp, puesto, sexo, fechaCon,datetime.now(),"activo", usuarioId, depaId, direccionId)
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
        id_ = data['idEmpleado']
        
        
        if not id_:
            return jsonify({"error": "ID is required"}), 400
        
        try:
            # Consulta SQL para eliminar el empleado
            sql = "DELETE FROM empleados WHERE idEmpleado = %s"
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
        id_ = data['idEmpleado']
        nombre = data['nombre']
        apellidoPa = data['apellidoPaterno']
        apellidoMa = data['apellidoMaterno']
        tel = data['telefono']
        curp = data['curp']
        puesto = data['puesto']
        sexo = data['sexo']
        fecha_str = data['fechaContratacion']
        fechaCon=datetime.strptime(fecha_str, "%Y-%m-%d") 
        status = data['status']
        depaId = data['departamentoId']
    
        if not id_ :
            return jsonify({"error": "ID,  is required"}), 400
        
        try:
            # Consulta SQL para actualizar el email y el password
            sql = "UPDATE empleados SET  nombre= %s, apellidoPaterno= %s, apellidoMaterno= %s, telefono= %s, curp= %s, puesto= %s, sexo= %s, fechaContratacion= %s, status= %s, departamentoId = %s WHERE idEmpleado= %s"
            cursor.execute(sql, (nombre, apellidoPa, apellidoMa,tel, curp, puesto, sexo, fechaCon, status,depaId, id_))
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






@empleado.route('/empleadoByUserId/<int:usuarioId>', methods=['GET'])
def emple(usuarioId):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    sql_1="select emp.idEmpleado, emp.nombre, emp.apellidoPaterno,"
    sql_2= " emp.apellidoMaterno, emp.sexo, dep.departamento, resp.tituloResponsable, resp.nombreResponsable, resp.puesto,emp.usuarioId"
    sql_3=" from empleados as emp"
    sql_4=" inner join departamentos as dep"
    sql_5=" on emp.departamentoId=dep.idDepartamento"
    sql_6=" inner join responsablesDepto as resp"
    sql_7=" on dep.responsableId=resp.idResponsable"
    sql_8 = " WHERE emp.usuarioId = %s;"
    sql=sql_1+sql_2+sql_3+sql_4+sql_5+sql_6+sql_7+sql_8
    
    if conn:
        try:
            cursor.execute(sql, usuarioId)
            result = cursor.fetchall()
            #print(result)
            
            result1 = []
            for d in result:
                result1.append({
                        'idEmpleado': d[0],'nombre': d[1], 'apellidoPaterno': d[2], 'apellidoMaterno': d[3], 
                        'sexo': d[4], 'departamento': d[5], 'tituloResponsable': d[6],
                        'nombreResponsable': d[7], 'puesto': d[8], 'usuarioId':d[9]
                        
                    }) 
            #print (result1) 
            return result1 
        
        except pymysql.MySQLError as e:
            print(f"Error during database query: {e}")
            return jsonify({"error": str(e)}), 500
        finally:
                conn.close()
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

   
@empleado.route('/updateEmpleado', methods=['POST'])
def update_empleado():
    conn = mysql.connect()
    cursor = conn.cursor()
    data = request.get_json()
    idEmpleado = data.get('idEmpleado')
    if not idEmpleado:
        return jsonify({"error": "idEmpleado is required"}), 400

    # Campos permitidos para la actualización
    fields = {
        'nombre': data.get('nombre'),
        'apellidoPaterno': data.get('apellidoPaterno'),
        'apellidoMaterno': data.get('apellidoMaterno'),
        'telefono': data.get('telefono'),
        'curp': data.get('curp'),
        'puesto': data.get('puesto'),
        'sexo': data.get('sexo'),
        'fechaContratacion': data.get('fechaCon'),
        'status': data.get('status'),
        'departamentoId': data.get('depaId')
    }

    # Filtrar los campos que no son None
    update_fields = {k: v for k, v in fields.items() if v is not None}
    
    if not update_fields:
        return jsonify({"error": "No fields to update"}), 400

    # Construir la consulta de actualización dinámicamente
    set_clause = ', '.join([f"{key} = %s" for key in update_fields.keys()])

    
    sql = f"UPDATE empleados SET {set_clause} WHERE idEmpleado = %s"

    values = list(update_fields.values())
    values.append(idEmpleado)  # Añadir usuarioId al final de los valores

    if conn:
        try:
            cursor.execute(sql, values)
            conn.commit()
            return jsonify({"res": "ok"}), 200
        except pymysql.MySQLError as e:
            print(f"Error during database query: {e}")
            return jsonify({"error": str(e)}), 500
        finally:
                conn.close()
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

    # Ejecutar la consulta


