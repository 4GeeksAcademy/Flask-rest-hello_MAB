from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__="people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    mass = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    homeworld_id = db.Column(db.Integer,db.ForeignKey('planets.id'))



    def serialize(self):
         return {
                "name" : self.name,
                "height" : self.height,
                "mass" : self.mass,
                "hair_color" : self.hair_color, 
                "eye_color" : self.eye_color,
                "gender" : self.gender,
                "birth_year" : self.birth_year, 
                "homeworld_id" : self.homeworld_id
    
         }

    def __repr__(self):
        return '<People %r>' % self.name
  

class Planets(db.Model):
    __tablename__="planets"
    id = db.Column(db.Integer, primary_key=True)
    climate= db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    # terrain = db.Column(db.String(10), nullable=False)
    # people = db.relationship ("People", backref='planets', lazy=True)

    def serialize(self): 
        return {
         "climate": self.climate,
         "name": self.name,
         "population": self.population
        #  "terrain": self.terrain
        #  "people": self.people
    }

    def __repr__(self):
        return '<Planets %r>' % self.name
   
class Favorites(db.Model):  
     id = db.Column(db.Integer, primary_key=True) 
     type= db.Column(db.String(20), nullable=False)
     element_id= db.Column(db.Integer, nullable=False)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
     user =  db.relationship ("User")
    #  planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    #  people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

def __repr__(self):
        return '<Favorites %r/%r>' % self.type % self.element_id

def serialize(self):
     return{
          "type": self.type,
          "element_id": self.element_id,
          "userInfo": self.user
     }

    

def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }