"""Blogly application."""

from flask import Flask, render_template,  redirect, request
from models import db, connect_db, User

DEFAULT_IMAGE_URL='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRI6evl-nRSxEm9Yl3WDpM5qmHAcQMZlLOXtMp7x6o&s'


app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "key"

#toolbar = DebugToolbarExtension(app)

#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
#db.create_all()

@app.route('/')
def home_page():
    return redirect('/users')


@app.route('/users')
def list():
    """Shows list of all users."""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def add_user():
    """Show an add form for users."""
    return render_template('add.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Adding a new user."""
    
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_URL = request.form.get("image_URL")
    
    image_URL = image_URL if image_URL else DEFAULT_IMAGE_URL

    user = User(first_name=first_name, last_name=last_name, image_url=image_URL)
    
    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show information about the given user."""
    
    user = User.query.get_or_404(user_id)
    return render_template('detail_page.html', user=user)


@app.route('/users/<int:user_id>/edit')
def get_edit_user(user_id):
    """Show the edit page for a user."""
    
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Process the edit form."""
    
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_URL = request.form.get("image_URL")
    
    #image_URL = image_URL if image_URL else None
    
    user = User.query.get_or_404(user_id)
    
    if user.first_name != first_name:
        user.first_name = first_name 

    if user.last_name != last_name:
        user.last_name = last_name
    
    if user.image_url != image_URL:  #if '' defaut = None     image_URL = image_URL if image_URL else DEFAULT_IMAGE_URL
        user.image_url = DEFAULT_IMAGE_URL if image_URL == '' else image_URL  
    
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete the user"""
    
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')