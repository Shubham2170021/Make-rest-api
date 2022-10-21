import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/random")
def get_random():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe={
    "id": random_cafe.id,
    "name": random_cafe.name,
    "map_url": random_cafe.map_url,
    "img_url": random_cafe.img_url,
    "location": random_cafe.location,
    "seats": random_cafe.seats,
    "has_toilet": random_cafe.has_toilet,
    "has_wifi": random_cafe.has_wifi,
    "has_sockets": random_cafe.has_sockets,
    "can_take_calls": random_cafe.can_take_calls,
    "coffee_price": random_cafe.coffee_price,
})
@app.route("/all")
def get_all():
    cafes = db.session.query(Cafe).all()
    cafes1=[]
    for cafe in cafes:
        cafes1.append(cafe.to_dict())
    return jsonify(cafes1)
# @app.route("/search/<location>")
@app.route("/search/")
def search():
    query_location = request.args.get("loc")
    cafes = Cafe.query.filter_by(location=query_location).first()
    if cafes:
        return jsonify(cafe={
        "id": cafes.id,
        "name": cafes.name,
        "map_url": cafes.map_url,
        "img_url": cafes.img_url,
        "location": cafes.location,
        "seats": cafes.seats,
        "has_toilet": cafes.has_toilet,
        "has_wifi": cafes.has_wifi,
        "has_sockets": cafes.has_sockets,
        "can_take_calls": cafes.can_take_calls,
        "coffee_price": cafes.coffee_price,
    })
    else:
        return {
            "error":{
                "Not found":"Sorry,we don't have a cafe at this location"
            }
        }
## HTTP POST - Create Record
@app.route("/add",methods=["POST"])
def add_cafe():
    new_cafe = Cafe(
    name=request.form["name"],
    map_url=request.form["map_url"],
    img_url=request.form["img_url"],
    location=request.form["loc"],
    has_sockets=bool(request.form["sockets"]),
    has_toilet=bool(request.form["toilet"]),
    has_wifi=bool(request.form["wifi"]),
    can_take_calls=bool(request.form["calls"]),
    seats=request.form["seats"],
    coffee_price=request.form["coffee_price"],)
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


## HTTP PUT/PATCH - Update Record
@app.route("/updateprice/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    new_price = request.args.get("new_price") #get new price 
    cafe = db.session.query(Cafe).get(cafe_id)#get cafe id
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})
## HTTP DELETE - Delete Record
@app.route("/reportclosed/<int:cafe_id>", methods=["DELETE"])
def deletecafe(cafe_id):
    cafe = db.session.query(Cafe).get(cafe_id)#get cafe id
    my_api_key="TopSecretKey"
    api_key = request.args.get("api_key") #get new price 
    if api_key==my_api_key:
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully updated the price."})
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})



if __name__ == '__main__':
    app.run(debug=True)
