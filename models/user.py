from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    # id(int), username(text), password(text)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True) # nullable: não deixar o campo estar vazio(True: aceita estar vazio/False: não aceita), unique: não aceita os usuário com o mesmo nome
    password = db.Column(db.String(80), nullable=False)