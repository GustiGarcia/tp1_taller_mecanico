from flask import Blueprint, request, jsonify
from models.client import Client
from models.db import db

client= Blueprint('client', __name__)

@client.route('/api/client', methods=['GET']) #GET
def get_client():
    clients = Client.query.all()
    return jsonify([client.serialize() for client in clients])

@client.route('/api/client/<id>', methods=['GET'])# GET BY ID / busqueda por id
def get_client_id(id):
    one_client=Client.query.get(id)
    if not one_client:
        return jsonify({'error': 'dueño/a no encontrado'}),404
    return jsonify(one_client.serialize())

@client.route('/api/client', methods=['POST']) #POST INDIVIDUAL
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

@client.route('/api/clients', methods=['POST']) # POST GRUPAL
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

@client.route('/api/client/<id>', methods=['PUT'])#metodo PUT , se coloca el id en la direccion y se pasa el json
def update_client(id):
    update = Client.query.get(id)
    if not update:
        return jsonify({'Error': 'no se encontro cliente'}),404
    new_name=request.json['name']
    new_email=request.json['email']
    new_phone=request.json['phone']

    update.name= new_name
    update.email=new_email
    update.phone=new_phone

    db.session.commit()
    return jsonify (update.serialize())

@client.route('/api/client/<id>', methods=(['PATCH']))
def patch_client(id):
    patch = Client.query.get(id)
    if not patch:
        return jsonify({'error': 'no se encontro cliente'}),404
    
    data = request.json
    if 'name' in data:
        patch.name= data['name']
    if 'email' in data:
        patch.email = data['email']
    if 'phone' in data:
        patch.phone= data['phone']
    
    db.session.commit()
    return jsonify(patch.serialize())


@client.route('/api/client/<id>', methods = ['DELETE']) #Funciona con cliente sin vehiculo, revisar para eliminar vehiculos tambien
def delete_client(id):
    delete = Client.query.get(id)
    if not delete:
        return jsonify({'error': 'cliente no encontrado/registrado'}),404
    db.session.delete(delete)
    db.session.commit()

    return jsonify(delete.serialize())