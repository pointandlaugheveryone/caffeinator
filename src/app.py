from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import DATABASE_URI
from models import Base
from flask import Flask, render_template, request, redirect, url_for, session
from models import Session, Drink   
# from kupi import fetch_drinks


app = Flask(__name__)

# database connection
engine = create_engine(DATABASE_URI)
session = scoped_session(sessionmaker(bind=engine))

# closes db session
@app.teardown_appcontext
def remove_session(exception=None):
    Session.remove()


@app.route('/')
def get_drinks():
    drinks = session.query(Drink).filter_by(discount=True).all()
    return render_template('home.html', drinks=drinks)

@app.route('/zero')
def get_zero_drinks():
    zero_drinks = session.query(Drink).filter_by(is_zero=True, discount=True).all()
    return render_template('zero.html', drinks=zero_drinks)

@app.route('/about')
def about_page():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
