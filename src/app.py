from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://joherrerac:<cotito2001j>@cluster0.dn5pzce.mongodb.net/?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    categoria = request.json['categoria']
    precio = request.json['precio']
    stock = request.json['stock']
    
    if nombre and descripcion and categoria and precio and stock:
        id = mongo.db.users.insert(
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
        return "received"
    

if __name__ == "__main__":
    app.run(debug=True)