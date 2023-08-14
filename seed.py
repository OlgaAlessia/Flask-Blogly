"""Seed file to make data for User db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
alan = User(first_name='Alan', last_name='Alda')
joel = User(first_name='Joel', last_name='Burton', image_url='https://pbs.twimg.com/profile_images/1217917608/IMG_3419_400x400.jpg')
jane = User(first_name='Jane', last_name='Smith')


# Add new objects to session, so they'll persist
db.session.add(alan)
db.session.add(joel)
db.session.add(jane)

# Commit
db.session.commit()