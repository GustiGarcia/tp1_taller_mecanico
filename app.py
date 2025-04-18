from flask import Flask
from routes.client import client
from models.db import db
from config.config import DATABASE_CONNECTION_URI

app = Flask (__name__)


app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db.init_app(app)

app.register_blueprint(client)

with app.app_context():
    from models.client import Client
    db.create_all()

@app.route("/")
def algo():
    return "<p>Hola! este es el proyecto ''TALLER MECANICO''<p>"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
