

import hashlib
from http import client
from pickle import TRUE
from turtle import update
from flask import Flask,jsonify,request
import pymongo
import flask_mongoengine
from pymongo import MongoClient
import json
from bson import json_util
from flask_cors import CORS, cross_origin




#cluster = MongoClient("mongodb+srv://mamadou:passer@cluster0.vdd6f.mongodb.net/test")
cluster = MongoClient("mongodb+srv://mamadou:passer@cluster0.vdd6f.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["hopital"]
collection = db["patient"]



#collection.insert_one({"nom":"kamado","prenom":"TAngiro","date_naissance":"24/10/1799"})
#collection.find_one()

app = Flask(__name__)
cors =CORS(app)
app.config['CORS_Headers']= 'Content-Type'

@app.route('/get', methods=['GET'])
def get_patients():
    all_patients= list(collection.find({}))
    return json.dumps(all_patients,default=json_util.default)


@app.route('/get/<nom>', methods=['GET'])
@cross_origin()
def get_one_patient(nom):
    patient= list(collection.find({'nom':nom}))
    return json.dumps(patient,default=json_util.default)


@app.route('/add', methods=['POST'])
def add_client():
    new_patient = request.get_json()
    nom = new_patient['nom']
    prenom = new_patient['prenom']
    numero_patient = new_patient['numero_patient']
    sexe = new_patient['sexe']
    date_naissance = new_patient['date_naissance']
    lieu_naissance = new_patient['lieu_naissance']
    nom_du_pere = new_patient['nom_du_pere']
    nom_de_la_mere = new_patient['nom_de_la_mere']
    address = new_patient['address']
    nat = new_patient['Nationalité']


    exist = collection.find_one({'numero_patient':numero_patient})
 
    if exist:
        return jsonify({'msg': 'patient already exists'})
    else:
            collection.insert_one({'nom':nom,'prenom':prenom,'numero_patient':numero_patient,
            'sexe':sexe,'date_naissance':date_naissance, 'lieu_naissance':lieu_naissance,'nom_du_pere':nom_du_pere,
            'nom_de_la_mere':nom_de_la_mere,'address':address,'natNationalité':nat}) 
            return jsonify({'msg': 'patient created successfully'})


@app.route('/delete/<nom>', methods=['DELETE'])
def delete_patient(nom):
    exist = collection.find_one({'nom':nom})
    if exist:
        collection.delete_one({'nom':nom})
        return jsonify({'msg': 'patient deleted successfully'})
    else:
        return jsonify({'msg': 'patient n\'existe pas !!'})



@app.route('/update/<nom>', methods=['PUT'])
def update_patient(nom):
    new_patient = request.get_json()
    exist = collection.find_one({'nom':nom})
    new_nom = new_patient['nom']
    new_prenom = new_patient['prenom']
    new_numero_patient = new_patient['numero_patient']
    new_sexe = new_patient['sexe']
    new_date_naissance = new_patient['date_naissance']
    new_lieu_naissance = new_patient['lieu_naissance']
    new_nom_du_pere = new_patient['nom_du_pere']
    new_nom_de_la_mere = new_patient['nom_de_la_mere']
    new_address = new_patient['address']
    new_nat = new_patient['Nationalité']

    exist = collection.find_one({'numero_patient':new_numero_patient})  
    if  exist:
        collection.update_one({'nom':nom},{"$set":{'nom':new_nom,'prenom':new_prenom,'numero_patient':new_numero_patient,
            'sexe':new_sexe,'date_naissance':new_date_naissance, 'lieu_naissance':new_lieu_naissance,'nom_du_pere':new_nom_du_pere,
            'nom_de_la_mere':new_nom_de_la_mere,'address':new_address,'natNationalité':new_nat}})
        return jsonify({'msg': 'Information updated successfully'})
        #return get_one_patient(new_nom)
    else:
        return jsonify({'msg': 'patient n\'existe pas !!'})






if __name__ == '__main__':
    app.debug = True
    app.run() 
