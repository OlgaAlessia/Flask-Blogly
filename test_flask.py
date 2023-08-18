from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

DEFAULT_IMAGE_URL='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRI6evl-nRSxEm9Yl3WDpM5qmHAcQMZlLOXtMp7x6o&s'


# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()
        Post.query.delete()
        Tag.query.delete()
        
        user = User(first_name="TestFirstName", last_name="TestLastName")
        db.session.add(user)
        db.session.commit()
        
        post = Post(title="Test Title Post", content="Test Content Post", user_id=user.id)
        tag = Tag(name="TestTag")
                
        db.session.add_all([ post, tag ])
        db.session.commit()
        
        self.user = user
        self.post = post
        self.tag = tag
        
        
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstName', html)

    def test_show_user(self):
        with app.test_client() as client:
            
            resp = client.get(f"/users/{self.user.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstName TestLastName', html)
            self.assertIn(f'<button formmethod="GET" formaction="/users/{self.user.id}/edit" class="btn btn-primary"> Edit </button>', html)
            
    def test_create_user(self):
        with app.test_client() as client:
            d = {"first_name": "Name", "last_name": "Cognome", "image_url": "www.google.com"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Name Cognome", html)
     
    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name":"John", "last_name": "TestLastName", "image-url":"www.qualcosa.com"}
            resp = client.post(f'/users/{self.user.id}/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text = True)
            self.assertIn("John TestLastName", html)
            self.assertEqual(resp.status_code, 200)
            
    def test_delete(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user.id}/delete')
            user = User.query.get(self.user.id)

            self.assertFalse(user)
            
#################################################################################################################            
            
    def test_show_post(self):
        with app.test_client() as client:
            
            resp = client.get(f"/posts/{self.post.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Title Post</h1>', html)
            self.assertIn(f'<button formmethod="GET" formaction="/posts/{self.post.id}/edit" class="btn btn-primary"> Edit </button>', html)
            
    def test_create_post(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user.id}/posts/new", 
                    data={'title': 'NewTestTitle', 'pContent': 'NewTestContent'}, follow_redirects=True)
            html = resp.get_data(as_text = True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("NewTestTitle", html)
            
     
    def test_edit_post(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post.id}/edit', 
                    data={'title': 'FirstTestPost', 'pContent': 'First Post Test Content'}, follow_redirects=True)
            
            html = resp.get_data(as_text = True)
            
            self.assertIn("FirstTestPost", html)
            self.assertIn(f'<a href="/posts/{self.post.id}">FirstTestPost</a>', html)
            self.assertEqual(resp.status_code, 200)
            
    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post.id}/delete')
            post = Post.query.get(self.post.id)

            self.assertFalse(post)
            
            
            
#################################################################################################################            
            
    def test_list_tag(self):
        with app.test_client() as client:
            resp = client.get("/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestTag', html)
            
    def test_show_tag(self):
        with app.test_client() as client:
            
            resp = client.get(f"/tags/{self.tag.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestTag</h1>', html)
            self.assertIn('<h4 class="my-3">No post with this tag</h4>', html)
           
    def test_show_tag2(self):
        with app.test_client() as client:
            
            post = self.post
            tag_id = [self.tag.id, ]
            post.tags = Tag.query.filter(Tag.id.in_(tag_id)).all()
            
            db.session.add(post)
            db.session.commit()
            
            resp = client.get(f"/tags/{self.tag.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestTag</h1>', html)
            self.assertIn(f'<li><a href="/posts/{post.id}">{post.title}</a></li>', html)
             
            
    def test_create_tag(self):
        with app.test_client() as client:
            resp = client.post("/tags/new", 
                    data={'name': 'NewTestTag'}, follow_redirects=True)
            html = resp.get_data(as_text = True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("A new tag was create", html)
    
    
    def test_create_tag2(self):
        with app.test_client() as client:
            
            resp = client.post("/tags/new", 
                    data={'name': 'NewTestTag2', 'posts': f'{self.post.id}' }, follow_redirects=True)
            html = resp.get_data(as_text = True)
            
            tag = Tag.query.filter_by(name='NewTestTag2').one()
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<a href="/tags/{tag.id}">{tag.name}</a>', html)
            
            
    def test_edit_tag(self):
        with app.test_client() as client:
            resp = client.post(f'/tags/{self.tag.id}/edit', 
                    data={'name': 'EditTag'}, follow_redirects=True)
            
            html = resp.get_data(as_text = True)
            
            self.assertIn("EditTag", html)
            self.assertEqual(resp.status_code, 200)
    
    def test_edit_tag2(self):
        with app.test_client() as client:
            
            new_post = Post(title="Test Title Tag", content="Test Content Post w/tag", user_id=self.user.id)
            db.session.add(new_post)
            db.session.commit()
            
            
            resp = client.post(f'/tags/{self.tag.id}/edit',
                    data={'name': 'NewTestTag3', 'posts': f'{new_post.id}' }, follow_redirects=True)
            
            html = resp.get_data(as_text = True)
            
            self.assertIn("NewTestTag3", html)
            self.assertIn(f'<a href="/posts/{new_post.id}">Test Title Tag</a>', html)
            self.assertEqual(resp.status_code, 200)
            
    def test_delete_tag(self):
        with app.test_client() as client:
            resp = client.post(f'/tags/{self.tag.id}/delete')
            tag = Tag.query.get(self.tag.id)

            self.assertFalse(tag)