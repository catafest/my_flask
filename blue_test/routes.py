from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify({'result' : 'You are in main page!'}) 
