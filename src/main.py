"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favoritespeople, Favoritesplanet, Favoritesvehicles, People, Planet, Vehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    query_people = People.query.all()
    query_people = list(map(lambda x: x.serialize(), query_people))
    response_body = {
        "msg": "Hello, this is your GET /people response ",
        "people": query_people
    }

    return jsonify(response_body), 200


@app.route('/people/<int:id>', methods=['DELETE'])
def delete_people(id):
    people_delete = People.query.get(id)
    if not people_delete:
        response_body = {
            "msg": "Hello, this is your DELETE /people response ",
            "people": "people no existe, no puede ser eliminado"
        }
        return jsonify(response_body), 200        
    db.session.delete(people_delete)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your DELETE /people response ",
        "people": "personaje eliminado"
    }
    return jsonify(response_body), 200

@app.route('/people', methods=['POST'])
def post_people():
    body = request.get_json()
    people = People(name=body['name'], homeworld=body['homeworld'])
    db.session.add(people)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your POST /people response "
    }

    return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    query_planet = Planet.query.all()
    query_planet = list(map(lambda x: x.serialize(), query_planet))
    print(query_planet)
    response_body = {
        "msg": "Hello, this is your GET /planet response ",
        "planet": query_planet
    }

    return jsonify(response_body), 200

@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet_delete = Planet.query.get(id)
    if not planet_delete:
        response_body = {
            "msg": "Hello, this is your DELETE /planet response ",
            "planet": "planeta no existe, no puede ser eliminado"
        }
        return jsonify(response_body), 200        
    db.session.delete(planet_delete)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your DELETE /planet response ",
        "planet": "planeta eliminado"
    }
    return jsonify(response_body), 200

@app.route('/planet', methods=['POST'])
def post_planet():
    body = request.get_json()
    planet = Planet(name=body['name'],density=body['density'],gravity=body['gravity'])
    db.session.add(planet)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your POST /planet response "
    }

    return jsonify(response_body), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    query_vehicles = Vehicles.query.all()
    query_vehicles = list(map(lambda x: x.serialize(), query_vehicles))
    print(query_vehicles)
    response_body = {
        "msg": "Hello, this is your GET /vehicles response ",
        "vehicles": query_vehicles
    }

    return jsonify(response_body), 200

@app.route('/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicles(id):
    vehicles_delete = Vehicles.query.get(id)
    if not vehicles_delete:
        response_body = {
            "msg": "Hello, this is your DELETE /vehicles response ",
            "vehicles": "vehicles no existe, no puede ser eliminado"
        }
        return jsonify(response_body), 200        
    db.session.delete(vehicles_delete)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your DELETE /vehicles response ",
        "vehicles": "vehiculo eliminado"
    }
    return jsonify(response_body), 200      

@app.route('/vehicles', methods=['POST'])
def post_vehicles():
    body = request.get_json()
    vehicles = Vehicles(name=body['name'],model=body['model'],manufacturer=body['manufacturer'],pilots=body['pilots'])
    db.session.add(vehicles)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your POST /vehicles response "
    }

    return jsonify(response_body), 200  


@app.route('/user', methods=['GET'])
def handle_hello():
    query_user = User.query.all()
    query_user = list(map(lambda x: x.serialize(), query_user))
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "users":query_user
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
