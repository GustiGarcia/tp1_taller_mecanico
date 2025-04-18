from models.db import db
from models.client import Client

class Vehicle(db.Model):
    __tablename__= 'vehicle'

    id= db.Column(db.Integer, primary_key=True)
    marca= db.Column(db.String(20), nullable=False)
    modelo=db.Column (db.String(20), nullable=False)
    client_id=db.Column(db.Integer,db.ForeignKey('client.id'), nullable=False)

    def __init__(self, client_id, marca, modelo):
        self.client_id= client_id
        self.marca=marca
        self.modelo=modelo

    def serialize(self):
        return{
            'id': self.id,
            'client_id':self.client_id,
            'marca': self.marca,
            'modelo': self.modelo
        }