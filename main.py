import os
from flask import Flask, render_template as rt, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash as gph, check_password_hash as cph

app = Flask(__name__)
app.config['SECRET_KEY'] = '05c31152d33d28330bfd6cdfb5ee36e2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
        
    return rt('index.html')

@app.route('/login')
def login():
    return rt('login.html')

@app.route('/signin', methods=['POST'])
def signin():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return redirect('/login')
    if not cph(user.password, password):
        return redirect('/login')

    session['user_id'] = user.id
    return redirect('/')

@app.route('/register')
def register():
    return rt('register.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.fliter_by(email=email).first()
    if user:
        return redirect('/register')
    new_user = User (
        name=name,
        email=email,
        password=gph(password, method='sha256')
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect('/login')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
    return redirect('/')
    
if __name__ == '__main__':
    db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)