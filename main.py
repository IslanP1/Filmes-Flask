from flask import Flask
from sqlalchemy import create_engine
from models import Base

app = Flask(__name__)

app.config['SECRET_KEY'] = 'flaskFilmes'

engine = create_engine('sqlite:///db.sqlite')
Base.metadata.create_all(bind=engine)

from views import *

if __name__ == '__main__':
    app.run(debug=True)