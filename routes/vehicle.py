from flask import Blueprint,request, jsonify
from models.vehicle import Vehicle
from models.client import Client
from models.db import db

vehicle= Blueprint('vehicle', __name__)

@vehicle.route('/api/vehicle')
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


    for vehicle_data in data:#buvle for para iterar sobre cada vehiculo
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