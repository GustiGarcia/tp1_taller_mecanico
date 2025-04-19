from flask import Blueprint, request, jsonify
from models.client import Client
from models.db import db

client= Blueprint('client', __name__)

@client.route('/api/client') #GET
def get_client():
    clients = Client.query.all()
    return jsonify([client.serialize() for client in clients])

@client.route('/api/client', methods=['POST'])
def create_client():
    data = request.get_json() #Tomar datos enviados en formato json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')

    #VALIDACION QUE NO FALTEN DATOS
    if not name or not email or not phone:
        return jsonify({'error': 'faltan datos'}),400
    
#Crear Cliente (instanciamos???)
    new_client = Client(name=name,email=email, phone=phone)

    #agregamos a base de datos
    db.session.add(new_client)
    db.session.commit() #confirma y escribre la base de datos

    return jsonify(new_client.serialize()), 201

@client.route('/api/clients', methods=['POST'])

def create_clients():
    data = request.get_json() #toma datos de clientes
    if isinstance(data, list):#verificar si es lista de clientes
        clients_added =[]
        for client_data in data:
            name= client_data.get('name')
            email=client_data.get('email')
            phone=client_data.get('phone')

            #validar
            if not name or not email or not phone:
                return jsonify({'error': 'faltan datos'}),400
            
            #crear cliente
            new_client = Client(name=name, email=email,phone=phone)

            #agregar a base de datos
            db.session.add(new_client)
            db.session.commit() #confirma y escribre la base de datos
            clients_added.append(new_client.serialize())#agregar
        return jsonify(clients_added),201 #retorna los clientes creados
    else:
        return jsonify({'error': 'se esperaba lista de clientes'}),400
    
