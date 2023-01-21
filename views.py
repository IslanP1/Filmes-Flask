from flask import render_template, request, redirect, url_for, session
from sqlalchemy.orm import sessionmaker
from models import Base, Usuario
from main import app, engine
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import requests
import json

Base.metadata.bind = engine
sessaoDb = sessionmaker(bind=engine)

login_manage = LoginManager()
login_manage.init_app(app)


class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        
    def get_id(self):
        return self.id
    

@login_manage.user_loader
def load_user(user_id):
    sessaoLoad = sessaoDb()
    user = sessaoLoad.query(Usuario).filter_by(id=user_id).first()
    sessaoLoad.close()

    if user:
        return User(user.id, user.username, user.email)
    
    return None


@app.route('/')
def index():
    if current_user.is_authenticated:
        filmes = filmesPopulares()
        return render_template('base.html', user_name=current_user.name, filmes=filmes)
    else:
        return 'Cadastra-se ou faça login'

def filmesPopulares():
    chave_api = ""
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={chave_api}&language=pt-br"
    response = requests.get(url)
    return response.json()



   
    


@app.route('/login', methods=['POST', 'GET'])
def login():
    
    if current_user.is_authenticated:
        logout_user()
        
    if request.method == 'POST':
        sessaoLogin = sessaoDb()
        email= request.form['email']
        password = request.form['password']
        
        user = sessaoLogin.query(Usuario).filter_by(email = email, password = password).first()
        
        sessaoLogin.close()
        if user:
            user_obj = User(user.id, user.username, user.email)
            login_user(user_obj)
            return redirect(url_for('index'))
        else:
            return 'Email ou senha errados'

    return render_template('login.html')


@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        sessaoCadastro = sessaoDb()
        
        name = request.form.get('name')
        password = request.form.get('password')
        email = request.form.get('email')
        
        user = sessaoCadastro.query(Usuario).filter_by(email=email).first()
        
        if user:
            return redirect(url_for('cadastro'))
        
        novo_usuario = Usuario(
            username=name, password=password, email=email)
        sessaoCadastro.add(novo_usuario)
        sessaoCadastro.commit()
        sessaoCadastro.close()
        
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')
    
    
@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect('/login')
    else:
        @login_required
        def deslogar():
            logout_user()
        deslogar()
    return 'user deslogado'