from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key" # serve para proteção da conexão
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # serve para acessar o banco de dados

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
# view login
login_manager.login_view = 'login'

# Session <- conexão ativa

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Rota para realizar o Login
@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        # Login
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password: # checagem do usuário e senha, se são válidos
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message":"Autenticação realizada com sucesso"}), 200
    
    return jsonify({"message":"Credenciais inválidas"}), 400

# Rota para realizar o Logoff
@app.route('/logout', methods=['GET'])
@login_required # Protege a rota de usuários não autenticados
def logout():
    logout_user()
    return jsonify({"message":"Logout realizado com sucesso"}),200

# Rota para realizar a Criação de usuários
@app.route('/user', methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message":"Usuário cadastrado com sucesso"}), 200
    
    return jsonify({"message":"Dados inválidas"}), 400

# Rota para realizar a Leitura do usuário
@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)
    
    if user:
        return {"username":user.username}
    
    return jsonify({"message":"Usuário não encontrado"}), 404

# Rota para realizar a Alteração de usuário
@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)
    
    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()
        
        return jsonify({"message":f"Usuário {id_user} atualizado com sucesso"})
    
    return jsonify({"message":"Usuário não encontrado"}), 404

# Rota para Deletar o usuário
@app.route('/user/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)
    
    if id_user == current_user.id:
        return jsonify({"message":"Deleção não permitida"}), 403
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify ({"message":f"Usuário {id_user} deletado com sucesso"})
    
    return jsonify({"message":"Usuário não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)