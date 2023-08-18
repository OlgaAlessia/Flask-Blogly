"""Blogly application."""

from flask import Flask, render_template,  redirect, request, flash
from models import *

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
    
    flash(f"A new user was create.")
        
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
    
    flash(f"The user '{user.full_name}' was edited.")
    
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete the user"""
    
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f"The user '{user.full_name}' was delete.")
        
    return redirect('/users')

############################    POST    ############################

@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """Show form to add a post for that user."""
    
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('post/add_post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """Adding a new post."""
    
    title = request.form["title"]
    pContent = request.form["pContent"]
    tags_id = [int(id) for id in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tags_id)).all()
    
    post = Post(title=title, content=pContent, user_id=user_id, tags=tags)
    
    db.session.add(post)
    db.session.commit()
    
    flash(f"A new post was create.")
    
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
            
        #getlist("tags") 
        list_id_tag = [int(num) for num in request.form.getlist("tags")]
        post.tags = Tag.query.filter(Tag.id.in_(list_id_tag)).all()
        
        db.session.add(post)
        db.session.commit()
        flash(f"The post '{post.title}' was edited.")
        
        return redirect(f'/users/{post.user_id}')
    else:
        
        tags = Tag.query.all()
        
        return render_template('post/edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete the podt"""
    
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    
    flash(f"The post '{post.title}' was delete.")
    
    return redirect(f'/users/{post.user_id}')

############################    TAG    ############################

@app.route('/tags')
def list_tag():
    """Shows list of all users."""

    tags = Tag.query.all()
    return render_template('tag/list_tag.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag/show_tag.html', tag=tag)


@app.route('/tags/new', methods=['GET', 'POST'])
def add_tag():
    """ GET: Shows a form to add a new tag. 
        POST: Adding a new tag. """
    
    if request.method == 'POST':
        name = request.form["name"]
        list_id_post = [int(num) for num in request.form.getlist("posts")]

        posts = Post.query.filter(Post.id.in_(list_id_post)).all()
        
        tag = Tag(name=name,posts=posts)
        
        db.session.add(tag)
        db.session.commit()
        
        flash(f"A new tag was create.")
    
        return redirect(f'/tags')
    else:
        
        posts = Post.query.all()
        return render_template('tag/add_tag.html', posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    """Edit the tag."""
    
    tag = Tag.query.get_or_404(tag_id)
    
    if request.method == 'POST':
        
        name = request.form["name"]

        if tag.name != name:
            tag.name = name 
            
        list_id_post = [int(num) for num in request.form.getlist("posts")]
        tag.posts = Post.query.filter(Post.id.in_(list_id_post)).all()

        db.session.add(tag)
        db.session.commit()
        flash(f"The tag '{tag.name}' was edited.")
        
        return redirect(f'/tags/{tag.id}')
    else:
        
        posts = Post.query.all()
        
        return render_template('tag/edit_tag.html', tag=tag, posts=posts)
    
    
@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete the tag"""
    
    tag = Tag.query.get_or_404(tag_id)
    
    db.session.delete(tag)
    db.session.commit()
    
    flash(f"The tag '{tag.name}' was delete.")
    
    return redirect(f'/tags')