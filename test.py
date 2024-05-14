from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class FlaskTests(TestCase):

    def setUp(self):
        User.query.delete()

        user = User(first_name="Bob", last_name="Smith", image_url="http://cat.jpeg")
        db.session.add(user)
        db.session.commit()
        post = Post(title="a post", content="good content", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.user = user
        self.post = post
        self.fullname = user.first_name + ' ' + user.last_name

    def tearDown(self):
        db.session.rollback()

    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.fullname, html)

    def test_get_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.fullname, html)

    def test_new_user(self):
        with app.test_client() as client:
            d = {"first-name": "Tim", "last-name": "Malcom", "image-url": "cats"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Tim Malcom", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first-name": "Billy", "last-name": "Smith", "image-url": "cats"}
            resp = client.post(f"/users/{self.user.id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Bob Smith", html)
            self.assertIn("Billy Smith", html)

    def test_get_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("good content", html)

    def test_new_post(self):
        with app.test_client() as client:
            d = {"title": "new post", "content": "new content"}
            resp = client.post(f"/users/{self.user.id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.fullname, html)

    def test_edit_post(self):
        with app.test_client() as client:
            d = {"title": "updated post", "content": "updated content"}
            resp = client.post(f"/posts/{self.post.id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("updated post", html)
            self.assertIn("updated content", html)