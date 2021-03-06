from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__) 
#BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root@localhost:3306/productos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

CORS(app)

db = SQLAlchemy(app)

#Convertir objetos ORM en Json
ma = Marshmallow(app)

class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float)

    def __init__(self,nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio



class ProductSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','cantidad','precio')

product_schema=ProductSchema()
products_schema=ProductSchema(many=True)


#from products import products

@app.route('/ping')
def ping():
    return jsonify({"message":"pong"})

#Obtener productos
@app.route('/products')
def getProducts():
    all_products = Productos.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

#Obtener solo un producto
@app.route('/products/<id>')
def getProduct(id):
    product = Productos.query.get(id)
    return product_schema.jsonify(product)
    # product_found=[product for product in products if product['name']==product_name]
    # if (len(product_found)>0):
    #     return jsonify({"product": product_found[0]})
    # else:

#Agregar Producto
@app.route('/products',methods=['POST'])
def addProduct():
    name = request.json['name']
    quantity = request.json['quantity']
    price = request.json['price']
    new_product = Productos(name, quantity,price)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)
    # new_product={
    #     "name":request.json['name'],
    #     "price": request.json['price'],
    #     "quantity": request.json['quantity']
    # }
    # products.append(new_product)
     
#Actualizar productos
@app.route('/products/<id>',methods=['PUT'])
def editProduct(id):
    product = Productos.query.get(id)
    product.cantidad = request.json['quantity']
    db.session.commit()
    return product_schema.jsonify(product)
    # product_found=[product for product in products if product['name']==product_name]
    # if len(product_found) > 0:
    #     product_found[0]['name']=request.json['name']
    #     product_found[0]['price']=request.json['price']
    #     product_found[0]['quantity']=request.json['quantity']
    #     return jsonify({'message':'succesfully',"product":product_found})

#Eliminar un producto
@app.route('/products/<id>',methods=['DELETE'])
def deleteProduct(id):
    product = Productos.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)
    # product_found=[product for product in products if product['name']==product_name]
    # if len(product_found) > 0:
    #     products.remove(product_found[0])

if __name__=='__main__':
    app.run(debug=True, port=4000) 