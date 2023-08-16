from unittest import TestCase

import datetime
from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users."""

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_full_name(self):
        """Tests for the full name of user."""
        user = User(first_name="Olga", last_name="Quaranta")
        db.session.add(user)
        db.session.commit()

        self.assertEquals(user.full_name, "Olga Quaranta")
        
    def test_timestamp(self):
        """Tests for timestamp of post."""
        user = User(first_name="Olga", last_name="Quaranta")
        db.session.add(user)
        db.session.commit()
        
        post = Post(title="TestPost", content="Bla bla", user_id=user.id)
        db.session.add(post)
        db.session.commit()
        
        now = datetime.datetime.utcnow()
        timestamp = now.strftime('%b %-d %Y, %H:%M %p')
        
        self.assertEquals(post.timestamp, timestamp)
