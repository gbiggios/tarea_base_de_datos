from flask import Flask, render_template, request, Response, jsonify, redirect, url_for, flash, session
from functions import Restaurante
from database import Restaurante
from pedidos import Pedidos
from datetime import date
import pymongo


app = Flask(__name__)

restaurante=Restaurante()
db = restaurante.dbConnection()
app.secret_key = 'tu_clave_secreta_única_y_segura'

@app.route("/")
def index():
    pedidos_recibidos = restaurante.mycol.find()
    return render_template('index.html', products=pedidos_recibidos)

# Métodos Añadir
@app.route('/pedidos', methods=['POST'])
def addProduct():
    # Carga el ID desde el archivo
    with open('contador.txt', 'r') as file:
        _id = int(file.read())
    
    fecha = str(date.today())
    cliente = request.form['cliente']
    platos = request.form['platos'].split(',')
    total = request.form['total']

    if fecha and cliente and platos and total:
        # Crea una instancia de Pedidos con el ID cargado
        pedidos_instance = Pedidos(_id, fecha, cliente, platos, total)
        products = db['pedidos']
        products.insert_one(pedidos_instance.toDBCollection())

        # Incrementa el contador y guárdalo en el archivo
        _id += 1
        with open('contador.txt', 'w') as file:
            file.write(str(_id))
        
        flash('Pedido agregado correctamente', 'success')
        return redirect(url_for('index'))




def notFound(error=None):
    message = {
        'mensaje': 'No encontrado ' + str(request.url),  # Convertir el número a cadena
        'status': '404 not found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

@app.route('/delete', methods=['POST'])
def delete():
    nombre_cliente = request.form['cliente']
    products = db['pedidos']
    result = products.delete_many({'cliente': nombre_cliente})

    if result.deleted_count > 0:
        flash(f'Se eliminaron {result.deleted_count} pedidos del cliente {nombre_cliente}.', 'success')
    else:
        flash(f'No se encontraron pedidos para el cliente {nombre_cliente}.', 'info')
    
    return redirect(url_for('index'))

@app.route('/buscar_pedido', methods=['POST'])
def buscar_pedido():
    products = db['pedidos']
    pedido_id = request.form['id']
    
    try:
        # Intentar convertir el ID a ObjectId
        filtro = {'_id':(pedido_id)}
    except Exception as e:
        # Si falla la conversión, retornar error
        return render_template('index.html', error="ID inválido")

    pedido = products.find_one(filtro)
    
    if pedido:
        return render_template('index.html', pedido=pedido)
    else:
        return render_template('index.html', error="Pedido no encontrado")

@app.route('/edit', methods=['POST'])
def edit():
    products = db['pedidos']
    pedido_id = request.form['id']
    nuevo_total = request.form['total']

    try:
        # Intentar convertir el ID a ObjectId
        filtro = {'_id':pedido_id}
    except Exception as e:
        # Si falla la conversión, retornar error
        return render_template('index.html', error="ID inválido")

    if pedido_id and nuevo_total:
        actualizacion = {'$set': {'total': nuevo_total}}
        result = products.update_one(filtro, actualizacion)
        
        if result.matched_count > 0:
            return redirect(url_for('index'))
        else:
            return render_template('index.html', error="No se pudo actualizar el pedido.")
    else:
        return notFound()
    
def notFound(error=None):
    message = {
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True, port=4000)
