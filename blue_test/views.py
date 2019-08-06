from .extensions import db
from .models import Texts
from flask import Blueprint, jsonify, request

main = Blueprint('main', __name__)
@main.route('/add_text/<int:id>', methods = ['POST'])
def add_text():
    txt_data = request.get_json()
    new_txt = Texts(title=txt_data['title'], txt_content=txt_data['txt_content'])
    db.session(new_txt)
    db.session.commit()
    # 201 status code for create successfully
    return 'Done', 201
@main.route('/texts/', methods = ['GET'])
def texts():
    txt_list=Texts.query.all()
    texts=[]
    for txt in txt_list:
        texts.append({'title': txt.title, 'txt_content':txt.txt_content})
    return jsonify ({'texts':texts})
    