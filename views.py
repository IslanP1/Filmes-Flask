from flask import render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Usuario
from main import app
from flask_login import login_user

engine = create_engine('sqlite:///db.sqlite')
Base.metadata.bind = engine
sessaoDb = sessionmaker(bind=engine)
sessao = sessaoDb()

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password']
        
        user = sessao.query(Usuario).filter_by(email = email, password = password).first()
        sessao.close()
        
        if user:
            sessao.user_id = user.id
           
            return redirect(url_for('index'))
        
        else:
            return 'Email ou senha errados'
    
    return render_template('login.html')


@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        
        name = request.form.get('name')
        password = request.form.get('password')
        email = request.form.get('email')
        
        user = sessao.query(Usuario).filter_by(email=email).first()
        
        if user:
            return redirect(url_for('cadastro'))
        
        novo_usuario = Usuario(
            username=name, password=password, email=email)
        sessao.add(novo_usuario)
        sessao.commit()
        sessao.close()
        
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')
    
@app.route('/logout')
def logout():
    return 'Entrei no logout'
