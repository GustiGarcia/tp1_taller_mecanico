from flask import Blueprint,request, jsonify
from models.vehicle import Vehicle
from models.client import Client
from models.db import db

vehicle= Blueprint('vehicle', __name__)

@vehicle.route('/api/vehicle')#metodo GET
def get_vehicle():
    vehicles= Vehicle.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles])


@vehicle.route('/api/add_vehicle', methods=['POST'])
def create_vehicle():#funcion declarada
    data= request.get_json()#toma el contenido y lo convierte para que lo lea python

    if isinstance(data,dict): #comprobacion si es data lo convierte en una lista con un elemento
        data=[data]
    elif not isinstance(data,list):
        return jsonify({'error': ' se esperaba lista o vehiculo '}),400
    
    vehicles_added=[]


    for vehicle_data in data:#bucle for para iterar sobre cada vehiculo
        marca= vehicle_data.get('marca')
        modelo=vehicle_data.get('modelo')  
        client_id=vehicle_data.get('client_id')
    
        if not marca or not modelo or not client_id:
            return jsonify({'error': 'faltan datos'}),400
    
    #validar que el cliente exista
        client= Client.query.get(client_id)
        if not client:
            return jsonify({'error': 'El cliente no existe'}),404
    
        new_vehicle = Vehicle(marca=marca,modelo=modelo,client_id=client_id)
        db.session.add(new_vehicle)
        vehicles_added.append(new_vehicle)
    db.session.commit()
    return jsonify([v.serialize() for v in vehicles_added]),201


@vehicle.route('/api/vehicle/<id>', methods=['PUT'])#metodo PUT , se coloca el id en la direccion y se pasa el json
def update_vehicle(id):
    update = Vehicle.query.get(id)
    if not update:
        return jsonify({'Error': 'no se encontro Vehiculo'}),404
    new_marca=request.json['marca']
    new_modelo=request.json['modelo']

    update.marca=new_marca
    update.modelo=new_modelo

    db.session.commit()
    return jsonify (update.serialize())


@vehicle.route('/api/vehicle/<id>', methods=(['PATCH']))
def patch_client(id):
    patch = Vehicle.query.get(id)
    if not patch:
        return jsonify({'error': 'no se encontro Vehiculo'}),404
    
    data = request.json
    if 'marca' in data:
        patch.marca= data['marca']
    if 'modelo' in data:
        patch.modelo = data['modelo']
    
    db.session.commit()
    return jsonify(patch.serialize())



@vehicle.route('/api/vehicle/<id>', methods = ['DELETE']) #Funciona con cliente sin vehiculo, revisar para eliminar vehiculos tambien
def delete_vehicle(id):
    delete = Vehicle.query.get(id)
    if not delete:
        return jsonify({'error': 'Auto no Encontrado'}),404
    db.session.delete(delete)
    db.session.commit()

    return jsonify("Borrado")