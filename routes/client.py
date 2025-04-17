from flask import Blueprint, jsonify
from models.client import Client

client= Blueprint('client', __name__)

@client.route('/api/client')
def get_client():
    clients = Client.query.all()
    return jsonify([client.serialize() for client in clients])