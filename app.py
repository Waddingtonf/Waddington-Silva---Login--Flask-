from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from flask_login import LoginManager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yqamigryqnjmxl:180ee9d8de24aa592779826530b513d37efcee9a776c19e6cd1035ad06de17d7@ec2-44-205-41-76.compute-1.amazonaws.com:5432/dfminucost016v'
app.config['SECRET_KEY'] = 'wK050885'
login_manager = LoginManager(app)
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

@app.route('/')
def home():
    return render_template('home.html')

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']

        user = User(name, email, pwd)
        db.session.add(user)
        db.session.commit()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(pwd):
            return redirect(url_for('login'))        

        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # port = int(os.getenv('PORT'), '5000')
    #host='0.0.0.0', port = port,
    app.run(debug=True)