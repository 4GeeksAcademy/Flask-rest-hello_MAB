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
from models import db, User, Planets, People, Favorites
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


#from models import Person



# api = Blueprint("api", __name__)
app = Flask(__name__)
bcrypt= Bcrypt(app)
app.url_map.strict_slashes = False

app.config["JWT_SECRET_KEY"]=os.getenv("FLASK_APP_KEY")
jwt=JWTManager(app)

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/signup', methods=["POST"])
def user_create():
    data=request.get_json()
    print(data)
    new_user=User.query.filter_by(email=data["email"]).first()
    if (new_user is not None):
        return jsonify({
            "msg": "Email registrado"
        }),400
    secure_password=bcrypt.generate_password_hash(data["password"], rounds=None).decode("utf-8")
    print(new_user is None)
    new_user= User(email=data["email"], 
                   password=secure_password, 
                   is_active=True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201


@app.route("/login", methods=["POST"])
def user_login():
    user_email=request.json.get("email")
    user_password=request.json.get("password")
    #buscar el usario por el correo
    user=User.query.filter_by(email=user_email).first()
    if user is None:
        return jsonify({"message":"User not found"}), 401
    #Verificar la clave 
    if not bcrypt.check_password_hash(user.password, user_password):
        return jsonify({"message":"wrong password"}), 401
    #generar el token
    access_token=create_access_token(identity=user.id)
    #returnma el token
    return jsonify({"accessToken": access_token})

@app.route("/hello", methods=["GET"])
def hello_get():
    return jsonify ({"message": "hello"})


@app.route("/helloprotected", methods=["GET"])
@jwt_required()
def hello_protected_get():
    user_id=get_jwt_identity()
    return jsonify({"userId":user_id, 
                    "message":"hello protected route"})

#[GET] /people
@app.route("/people", methods=["GET"])
def people_get():
    people= People.query.all()
    people = list(map(lambda p: p.serialize(), people))
    return jsonify(people)

#[GET] /people/ <int:people_id>
@app.route("/people/<int:people_id>", methods=["GET"])
def people_id_get(people_id):
    people= People.query.get(people_id)
    # planets = list(map(lambda p: p.serialize(), planets))
    return jsonify(people.serialize())

#[GET] /planets
@app.route("/planets", methods=["GET"])
def planets_get():
    planets= Planets.query.all()
    planets = list(map(lambda p: p.serialize(), planets))
    return jsonify(planets)

#[GET] /planets/ <int:planet_id>
@app.route("/planets/<int:planets_id>", methods=["GET"])
def planets_id_get(planets_id):
    planets= Planets.query.get(planets_id)
    # planets = list(map(lambda p: p.serialize(), planets))
    return jsonify(planets.serialize())

#[GET] /users
@app.route("/user/<int:user_id>", methods=["GET"])
def user_get(user_id):
    user=User.query.get(user_id)
    if(user is None):
        return jsonify ({"Usuario no registrado"}), 404
    return jsonify(user.serialize())

#[GET] /users/favorites  
@app.route("/user/<int:user_id>/favorites", methods=["GET"])
def user_favorite_get(user_id):
    favorites=Favorites.query.filter_by(user_id=user_id).all()
    favorites=list(map(lambda fav : fav.serialize(), favorites))
    return jsonify (favorites)

#[POST] /favorite/planet/<int:planet_id> 
#[POST] /favorite/planet/<int:people_id>
@app.route("/favorites/<string:element>/<int:element_id>", methods=["POST"])
def favorite_planet_create(element, element_id):
    user_id=request.get_json()["user_id"]
    new_favorite= Favorites(type=element, element_id=element_id, user_id=user_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify ({"msg":"Favorite created"}), 201

#[DELETE] /favorite/planet/<int:planet_id>
#[DELETE] /favorite/people/<int:people_id>
@app.route("/favorites/<string:element>/<int:element_id>", methods=["DELETE"])
def favorite_planet_delete(element, element_id):
    user_id=request.get_json()["userId"]
    favorite = Favorites.query.filter_by (
        type=element, element_id=element_id, user_id=user_id).first()
    if (favorite is None):
        return jsonify({"msg":"Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200
# this only runs if `$ python src/app.py` is executed

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
