from datetime import datetime

from statistics import mode

from flask import Flask, jsonify, request

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tipo_medicion = {'sensor' : 'HC-SR04', 'variable' : 'Distancia', 'unidades' : 'Centimetros'}

moda = [0]

mediciones = [
    {'fecha': "2019-08-23 00:20:50", **tipo_medicion, 'valor': 24},
    {'fecha': '2019-08-23 04:53:30', **tipo_medicion, 'valor': 23},
    {'fecha': '2019-08-23 10:32:13', **tipo_medicion, 'valor': 12},
    {'fecha': '2019-08-23 17:24:10', **tipo_medicion, 'valor': 50},
    {'fecha': '2019-08-23 21:21:21', **tipo_medicion, 'valor': 43},
    {'fecha': '2019-08-24 01:58:27', **tipo_medicion, 'valor': 24},
    {'fecha': '2019-08-25 08:54:35', **tipo_medicion, 'valor': 9}
]

@app.route('/')
def get():
    return jsonify(**tipo_medicion)

@app.route('/mediciones', methods = ['GET'])
def getAll():
    return jsonify(mediciones)

@app.route('/mediciones/moda', methods = ['GET'])
def getModa():
    for medicion in mediciones:
        moda.append(medicion['valor'])
    return jsonify(mode(moda))

@app.route('/mediciones', methods=['POST'])
def postOne():
    now = datetime.now()
    body = request.json
    body['fecha'] = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    mediciones.append({**body, **tipo_medicion})
    return jsonify(mediciones)

@app.route('/mediciones/<string:fecha>', methods=['DELETE'])
def deleteOne(fecha):
    x = False
    for medicion in mediciones:
        if (fecha in medicion['fecha']):
            x = True
            mediciones.remove(medicion)
    return 'Eliminado' if x else 'No Encontrado'

@app.route('/mediciones/<string:fecha>', methods=['PUT'])
def putOne(fecha):
    body = request.json
    x = False
    for medicion in mediciones:
        if(fecha in medicion['fecha']):
            x = True
            medicion['valor'] = body['valor']
    return 'Modificado' if x else 'No Encontrado'

app.run(port = 5000, debug = True)
