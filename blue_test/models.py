# import db from base folder, see dot
from .extensions import db 

class Texts(db.Model):
    # primary key 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    txt_content = db.Column(db.String(1000))
    
