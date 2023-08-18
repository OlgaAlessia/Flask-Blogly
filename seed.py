"""Seed file to make data for User db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add users
alan = User(first_name='Alan', last_name='Alda')
joel = User(first_name='Joel', last_name='Burton', image_url='https://pbs.twimg.com/profile_images/1217917608/IMG_3419_400x400.jpg')
jane = User(first_name='Jane', last_name='Smith')


# Add new objects to session, so they'll persist
db.session.add_all([alan, joel, jane])

# Commit
db.session.commit()


# Add posts
p1 = Post(title='First Post!', content='Oh, hai', user_id=2)
p2 = Post(title='Yet Another Post', content='', user_id=2)
p3 = Post(title='Flask is Awesome', content='Tell me something I don\'t know ', user_id=2)

# Add tags
t1 = Tag(name='Fun')
t2 = Tag(name='Even More')
t3 = Tag(name='Bloop')

db.session.add_all([p1, p2, p3, t1, t2, t3])
db.session.commit()

pt1 = PostTag(post_id = p1.id, tag_id = t1.id)
pt2 = PostTag(post_id = p1.id, tag_id = t2.id)
pt3 = PostTag(post_id = p1.id, tag_id = t3.id)
pt4 = PostTag(post_id = p2.id, tag_id = t1.id)

db.session.add_all([pt1, pt2, pt3, pt4])
db.session.commit()