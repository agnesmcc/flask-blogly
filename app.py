"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.debug = True
app.secret_key = 'secret'
toolbar = DebugToolbarExtension(app)

app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
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
    user = db.session.get(User, user_id)
    return render_template('show_user.html', user=user, posts=user.posts)

@app.route('/users/<user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == "GET":
        user = db.session.get(User, user_id)
        return render_template('edit_user.html', user=user)
    else:
        print('new user being created')
        first_name = request.form.get('first-name', '')
        last_name = request.form.get('last-name', '')
        image_url = request.form.get('image-url', '')
        print(first_name, last_name, image_url)
        user = db.session.get(User, user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.image_url = image_url
        db.session.add(user)
        db.session.commit()
        return redirect('/users')

@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = db.session.get(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<user_id>/posts/new', methods=['GET', 'POST'])
def new_post(user_id):
    user = db.session.get(User, user_id)
    if request.method == "GET":
        return render_template('create_post.html', user=user)
    else:
        print('new post being created')
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        print(title, content)
        new_post = Post(title=title, content=content, user_id=user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(f'/users/{user.id}')

@app.route('/posts/<post_id>')
def get_post(post_id):
    post = db.session.get(Post, post_id)
    return render_template('show_post.html', post=post, user=post.user)

@app.route('/posts/<post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = db.session.get(Post, post_id)
    if request.method == "GET":
        return render_template('edit_post.html', post=post)
    else:
        print('post being edited')
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        print(title, content)
        post.title = title
        post.content = content
        db.session.add(post)
        db.session.commit()
        return redirect(f'/posts/{post.id}')

@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')