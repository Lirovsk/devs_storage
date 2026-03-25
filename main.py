# Main file for flask_DIO

# This is the main file for the project created using the file manager.

import json

from flask import Flask, request

from DBworks import (create_hability, create_user, delete_user,
                     search_hability_by_name, search_user_by_email,
                     search_user_by_name, delete_hability, update_user, update_user_email)


app = Flask(__name__)


@app.route('/insert_user/', methods=['POST'])
def Insert_user():
    dados = request.data
    print(dados)
    dados = json.loads(dados)

    response = create_user(dados)

    return response


@app.route('/search_user_by_name/<string:name>', methods=['GET'])
def Search_user(name):
    response = search_user_by_name(name)
    return response


@app.route('/search_user_by_email/<string:email>', methods=['GET'])
def Search_by_email(email):
    response = search_user_by_email(email)
    return response


@app.route('/delete_user/<string:email>', methods=['DELETE'])
def Delete_user(email):
    response = delete_user(email)
    return response


@app.route('/update_user/<string:email>', methods=['GET', 'PUT'])
def Update_user(email):
    if request.method == 'GET':
        response = search_user_by_email(email)
        return response
    
    elif request.method == 'PUT':
        dados = request.data
        dados = json.loads(dados)

        response = update_user(user_email=email, user_name=dados.get('name'), user_age=dados.get('age'))

        return response
    
    
@app.route('/update_user_email/<string:email>', methods=['PUT'])
def Update_user_email(email):
        
        dados = request.data
        dados = json.loads(dados)

        response = update_user_email(user_email=email, new_email=dados.get('new_email'))

        return response


@app.route('/create_hability/', methods=['POST'])
def Create_hability():
    dados = request.data
    dados = json.loads(dados)

    response = create_hability(hability_name=dados['hability_name'], hability_level=dados['hability_level'], user_email=dados['user_email'], hability_description=dados.get('hability_description', None))

    return response


@app.route('/search_hability_by_name/<string:hability_name>/<string:user_email>', methods=['GET'])
def Search_hability_by_name(hability_name, user_email):
    response = search_hability_by_name(hability_name, user_email)
    return response


@app.route('/delete_hability/<string:hability_name>/<string:user_email>', methods=['DELETE'])
def Delete_hability(hability_name, user_email):
    response = delete_hability(hability_name, user_email)
    return response


if __name__ == '__main__':
    app.run(debug=True)
