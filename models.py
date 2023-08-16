"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE_URL='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRI6evl-nRSxEm9Yl3WDpM5qmHAcQMZlLOXtMp7x6o&s'


db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    
    db.app = app
    db.init_app(app)
    
    
    
class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String, nullable=True, default=DEFAULT_IMAGE_URL)
    
    # SQLA will populate it with data from the post table automatically!
    # These settings are appropriate for related objects which only exist as long 
    # as they are attached to their parent, and are otherwise deleted.
    posts = db.relationship('Post', backref='user', passive_deletes=True) 
        
    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"
    
    @property
    def full_name(self):
        """return the full name of the user"""
        return f"{self.first_name} {self.last_name}"
    
    
class Post(db.Model):
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        """Show info about user."""
        
        p = self
        return f"<Post {p.id} {p.title} {p.content} {p.created_at} >"
    
    @property
    def timestamp(self):
        """Showing the time in a easy way
            May 1 2015, 10:30 AM """
        
        return self.created_at.strftime("%b %-d %Y, %H:%M %p")