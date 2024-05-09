"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.debug = True
app.secret_key = 'secret'
toolbar = DebugToolbarExtension(app)

app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
# db.create_all()

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == "GET":
        return render_template('create_user.html')
    else:
        print('new user being created')
        first_name = request.form.get('first-name', '')
        last_name = request.form.get('last-name', '')
        image_url = request.form.get('image-url', '')
        print(first_name, last_name, image_url)
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/users')

@app.route('/users/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    return render_template('show_user.html', user=user)

@app.route('/users/<user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == "GET":
        user = User.query.get(user_id)
        return render_template('edit_user.html', user=user)
    else:
        print('new user being created')
        first_name = request.form.get('first-name', '')
        last_name = request.form.get('last-name', '')
        image_url = request.form.get('image-url', '')
        print(first_name, last_name, image_url)
        user = User.query.get(user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.image_url = image_url
        db.session.add(user)
        db.session.commit()
        return redirect('/users')

@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')