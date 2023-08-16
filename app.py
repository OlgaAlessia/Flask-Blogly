"""Blogly application."""

from flask import Flask, render_template,  redirect, request, flash
from models import db, connect_db, User, Post

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


# app name
@app.errorhandler(404)
  
# inbuilt function which takes error as parameter
def not_found(e):
  
  return render_template("404.html")


@app.route('/')
def home_page():
    posts = Post.query.order_by(Post.created_at).limit(5)
    return render_template('post/recent_posts.html', posts=posts)

############################    USER    ############################

@app.route('/users')
def list():
    """Shows list of all users."""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user/list.html', users=users)


@app.route('/users/new')
def add_user():
    """Show an add form for users."""
    return render_template('user/add.html')

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
    return render_template('user/detail_page.html', user=user)


@app.route('/users/<int:user_id>/edit')
def get_edit_user(user_id):
    """Show the edit page for a user."""
    
    user = User.query.get_or_404(user_id)
    return render_template('user/edit.html', user=user)


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

############################    POST    ############################

@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """Show form to add a post for that user."""
    
    user = User.query.get_or_404(user_id)
    return render_template('post/add_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """Adding a new post."""
    
    title = request.form["title"]
    pContent = request.form["pContent"]

    post = Post(title=title, content=pContent, user_id=user_id)
    
    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post."""
    
    post = Post.query.get_or_404(post_id)
    return render_template('post/show_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    """Edit the post."""
    
    post = Post.query.get_or_404(post_id)
    
    if request.method == 'POST':
        
        title = request.form["title"]
        pContent = request.form["pContent"]
        
        if post.title != title:
            post.title = title 

        if post.content != pContent:
            post.content = pContent
            
        db.session.commit()
        flash(f"The post '{post.title}' was edited.")
        
        return redirect(f'/users/{post.user_id}')
    else:
        
        return render_template('post/edit_post.html', post=post)


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete the user"""
    
    post = Post.query.get_or_404(post_id)
    
    #user_id = post.user_id
    
    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/users/{post.user_id}')
