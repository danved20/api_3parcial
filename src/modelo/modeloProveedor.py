from flask import jsonify,request
from modelo.coneccion import db_connection

def buscar_proveedor(codigo):
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT ci, nombre, edad, ciudad FROM proveedor WHERE ci=%s", (codigo,))
        datos = cur.fetchone()
        conn.close()
        
        if datos is not None:
            proveedor = {
                'ci': datos[0],
                'nombre': datos[1],
                'edad': datos[2],
                'ciudad': datos[3]
            }
            return proveedor
        else:
            return None
    except Exception as ex:
        raise ex 



class ProveedorModel:
    @classmethod
    def listar_proveedores(cls):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("SELECT ci, nombre, edad, ciudad FROM proveedor")
            datos = cur.fetchall()
            conn.close()

            proveedores = []

            for fila in datos:
                proveedor = {
                    'ci': fila[0],
                    'nombre': fila[1],
                    'edad': fila[2],
                    'ciudad': fila[3]
                }
                proveedores.append(proveedor)

            return jsonify({'proveedores': proveedores, 'mensaje': "Proveedores listados."})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

    @classmethod
    def crear_proveedor(cls):
        try:
            conn = db_connection()
            proveedor = buscar_proveedor(request.json['ci'])
            if proveedor is not None:
                return jsonify({'mensaje': "Cédula de identidad ya existe, no se puede añadir"})
            else:
                cur = conn.cursor()
                cur.execute('INSERT INTO proveedor (ci, nombre, edad, ciudad) VALUES (%s, %s, %s, %s)', (
                    request.json['ci'], request.json['nombre'], request.json['edad'], request.json['ciudad']))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Proveedor registrado", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
        
    @staticmethod
    def modificar_proveedor():
        try:
            data = request.get_json()  # Obtener el JSON del cuerpo de la solicitud
            ci = data.get('ci')  # Obtener la cédula del proveedor del JSON

            # Verificar si el proveedor existe antes de actualizarlo
            proveedor = buscar_proveedor(ci)
            if proveedor is None:
                return jsonify({'mensaje': "Proveedor no encontrado", 'exito': False})

            # Actualizar los datos del proveedor con los valores del JSON
            proveedor['nombre'] = data.get('nombre', proveedor['nombre'])
            proveedor['edad'] = data.get('edad', proveedor['edad'])
            proveedor['ciudad'] = data.get('ciudad', proveedor['ciudad'])

            # Aquí puedes realizar la lógica para actualizar los datos del proveedor en la base de datos

            return jsonify({'mensaje': "Proveedor modificado", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error al modificar proveedor", 'exito': False})
    
    """ @classmethod
    def modificar_proveedor(cls,ci):
        try:
            conn = db_connection()
            proveedor = buscar_proveedor(request.json['ci'])
            if proveedor is None:
                return jsonify({'mensaje': "Proveedor no encontrado"})
            else:
                cur = conn.cursor()
                cur.execute('UPDATE proveedor SET nombre=%s, edad=%s, ciudad=%s WHERE ci=%s', (
                    request.json['nombre'], request.json['edad'], request.json['ciudad'], request.json['ci']))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Proveedor modificado", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False}) """


    @staticmethod
    def buscar_proveedor(ci):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("SELECT ci, nombre, edad, ciudad FROM proveedor WHERE ci=%s", (ci,))
            datos = cur.fetchone()
            conn.close()
        
            if datos is not None:
                proveedor = {
                    'ci': datos[0],
                    'nombre': datos[1],
                    'edad': datos[2],
                    'ciudad': datos[3]
                }
                return jsonify(proveedor)
            else:
                return jsonify(None)
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False}) 
        
    @staticmethod
    def delete_proveedor(ci):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM proveedor WHERE ci=%s", (ci,))
            conn.commit()
            conn.close()
            return jsonify({'mensaje': "Proveedor eliminado", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error al eliminar proveedor", 'exito': False})
        

    @classmethod
    def consulta(cls):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""SELECT p.descripcion, pr.nombre AS proveedor, c.nombre AS cliente
                        FROM productos p
                        JOIN proveedor pr ON p.cod_proveedor = pr.ci
                        JOIN clientes c ON p.cod_cliente = c.cod_cli;
                        """)
            datos = cur.fetchall()
            conn.close()

            resultados = []

            for fila in datos:
                resultado = {
                    'descripcion': fila[0],
                    'proveedor': fila[1],
                    'cliente': fila[2]
                }
                resultados.append(resultado)

            return jsonify({'resultados': resultados, 'mensaje': "Consulta exitosa."})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})