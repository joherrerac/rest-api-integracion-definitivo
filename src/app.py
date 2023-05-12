from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://joherrerac:<cotito2001j>@cluster0.dn5pzce.mongodb.net/?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_products():
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    categoria = request.json['categoria']
    precio = request.json['precio']
    stock = request.json['stock']
    
    if nombre and descripcion and categoria and precio and stock:
        id = mongo.db.products.insert(
            {'nombre': nombre, 'descripcion': descripcion, 'categoria': categoria, 'precio': precio, 'stock': stock}
        )
        response = {
            'id': str(id),
            'nombre': nombre,
            'descripcion': descripcion,
            'categoria': categoria,
            'precio': precio,
            'stock': stock
        }
        return response
    else:
        return not_found()

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({"_id": ObjectId(id)})
    response = json_util(user)
    
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({"_id": ObjectId(id)})
    response = jsonify({"message": 'User' + id + 'was deleted succefully'})
    
    return response

@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    categoria = request.json['categoria']
    precio = request.json['precio']
    stock = request.json['stock']
    if nombre and descripcion and categoria and precio and stock:
        mongo.db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'nombre': nombre, 'descripcion': descripcion, 'categoria': categoria, 'precio': precio, 'stock': stock}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
        return not_found()


@app.errorhandler(404)

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource not found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)