from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from bson.json_util import dumps
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://qvxjnoc.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(uri, server_api=ServerApi('1'))

mongo = PyMongo(app)

@app.route('/products', methods=['POST'])
def create_product():
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    categoria = request.json['categoria']
    precio = request.json['precio']
    stock = request.json['stock']
    
    if nombre and descripcion and categoria and precio and stock:
        products = mongo.db.products
        product_data = {
            'nombre': nombre,
            'descripcion': descripcion,
            'categoria': categoria,
            'precio': precio,
            'stock': stock
        }
        result = products.insert_one(product_data)
        product_id = str(result.inserted_id)
        product_data['_id'] = product_id
        return jsonify(product_data)
    else:
        return not_found()

@app.route('/products', methods=['GET'])
def get_products():
    products = mongo.db.products.find()
    response = dumps(products)
    return response

@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = mongo.db.products.find_one({"_id": ObjectId(id)})
    if product:
        response = dumps(product)
        return response
    else:
        return not_found()

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    result = mongo.db.products.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return jsonify({"message": f"Product {id} was deleted successfully"})
    else:
        return not_found()

@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    categoria = request.json['categoria']
    precio = request.json['precio']
    stock = request.json['stock']
    if nombre and descripcion and categoria and precio and stock:
        products = mongo.db.products
        product_data = {
            'nombre': nombre,
            'descripcion': descripcion,
            'categoria': categoria,
            'precio': precio,
            'stock': stock
        }
        result = products.update_one(
            {'_id': ObjectId(id)},
            {'$set': product_data}
        )
        if result.modified_count == 1:
            return jsonify({'message': f"Product {id} updated successfully"})
        else:
            return not_found()
    else:
        return not_found()

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