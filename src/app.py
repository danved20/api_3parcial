from flask import Flask, jsonify,request
from modelo.modeloProveedor import ProveedorModel
from decouple import config
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/proveedores/*": {"origins": "http://192.168.31.204:5000/proveedores"}})

@app.route('/')
def hello_world():
    host = config('PG_USER')
    print(host)
    return '¡Hola mundo!'

@app.route('/proveedores', methods=['GET'])
def listar_proveedores():
    proveedores = ProveedorModel.listar_proveedores()
    return proveedores

@app.route('/proveedores', methods=['POST'])
def crear_proveedor():
    proveedor = ProveedorModel.crear_proveedor()
    return proveedor

@app.route('/proveedores/<ci>', methods=['PUT'])
def buscar_proveedor(ci):
    proveedor = ProveedorModel.buscar_proveedor(ci)
    return proveedor

@app.route('/proveedores/<ci>', methods=['GET', 'PUT'])
def modificar_proveedor(ci):
    if request.method == 'GET':
        proveedor = ProveedorModel.buscar_proveedor(ci)
        return proveedor
    elif request.method == 'PUT':
        proveedor = ProveedorModel.modificar_proveedor(ci)
        return proveedor 

@app.route('/proveedores/<ci>', methods=['DELETE'])
def eliminar_proveedor(ci):
    return ProveedorModel.delete_proveedor(ci)
""" @app.route('/proveedores/<ci>', methods=['PUT'])
def modificar_proveedor(ci):
    proveedor = ProveedorModel.modificar_proveedor(ci)
    return proveedor  """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
