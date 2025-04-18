from flask import Blueprint, jsonify
from models.vehicle import Vehicle

vehicle= Blueprint('vehicle', __name__)

@vehicle.route('/api/vehicle')
def get_vehicle():
    vehicles= Vehicle.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles])
