from flask import Flask, request, jsonify
from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
import os
import uuid


app = Flask(__name__)
app.config.from_object(__name__)
CORS(app,resources={r"/*": {"origins": "*"}})


# Basic Route

@app.route('/', methods=['GET'])
def greeting():
    return "Hello, World!"


@app.route('/shark', methods=['GET'])
def shark():
    return "Shark"

GAMES = [

    {   'id': uuid.uuid4().hex,
        'title':'2k21',
        'genre':'sports',
        'played': True,
    },
    {   'id': uuid.uuid4().hex,
        'title':'Evil Within',
        'genre':'horror',
        'played': False,
    },
    {   'id': uuid.uuid4().hex,
        'title':'the last of us',
        'genre':'survival',
        'played': True,
    },
    {  'id': uuid.uuid4().hex,
        'title':'days gone',
        'genre':'horror/survival',
        'played': False,
    },
    {   'id': uuid.uuid4().hex,
        'title':'mario',
        'genre':'retro',
        'played': True,
    }

]

@app.route('/games', methods=['GET', 'POST'])
def all_games():
    response_object = {'status':'success'}
    if request.method == "POST":
        post_data = request.get_json()
        GAMES.append({
            'id' : uuid.uuid4().hex,
            'title': post_data.get('title'),
            'genre': post_data.get('genre'),
            'played': post_data.get('played')})
        response_object['message'] =  'Game Added!'
    else:
        response_object['games'] = GAMES
    return jsonify(response_object)

@app.route('/games/<game_id>', methods =['PUT', 'DELETE'])
def single_game(game_id):
    response_object = {'status':'success'}
    if request.method == "PUT":
        post_data = request.get_json()
        remove_game(game_id)
        GAMES.append({
            'id' : uuid.uuid4().hex,
            'title': post_data.get('title'),
            'genre': post_data.get('genre'),
            'played': post_data.get('played')
        })
        response_object['message'] =  'Game Updated!'
    if request.method == "DELETE":
        remove_game(game_id)
        response_object['message'] = 'Game removed!'    
    return jsonify(response_object)


# Removing the game to update / delete
def remove_game(game_id):
    for game in GAMES:
        if game['id'] == game_id:
            GAMES.remove(game)
            return True
    return False

if __name__ == '__main__':
    app.run(debug=True)