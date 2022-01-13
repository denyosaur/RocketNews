from app import app, db
from unittest import TestCase
from flask import session
from form import UserRegistration, UserProfile, LoginForm

##app.config['TESTING'] = True
##app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class RocketNewsTestCase(TestCase):
    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # def test_homepage_not_logged_in(self):
    #     with app.test_client() as client:
    #         res = client.get('/')
    #         html = res.get_data(as_text=True)

    #         self.assertEqual(res.status_code, 302)
    #         self.assertEqual(res.location, 'http://localhost/login')
            
    # def test_login_page(self):
    #     with app.test_client() as client:
    #         res = client.get('/login')
    #         html = res.get_data(as_text=True)

    #         self.assertEqual(res.status_code, 200)
    #         self.assertIn('<h1>Login</h1>', html)
    
    # def test_register_page(self):
    #     with app.test_client() as client:
    #         res = client.get('/register')
    #         html = res.get_data(as_text=True)

    #         self.assertEqual(res.status_code, 200)
    #         self.assertIn('<h1>Register</h1>', html)

    # def test_expects_to_instantiate_new_form(self):
    #     with app.test_request_context('/register'):
    #         form = UserRegistration()
    #     self.assertIsInstance(form, UserRegistration)


    def test_expects_to_register_user(self):
        app.config['WTF_CSRF_ENABLED'] = False

        user_data = {
                'username':'testuser4', 
                'password':'testpass', 
                'email':'test4@email.com'
                }
        res = self.client.post(
            '/register',
            data = user_data)
        self.assertEqual(res.status_code, 302)

    def test_expects_new_register_to_redirect(self):
        app.config['WTF_CSRF_ENABLED'] = False

        user_data = {
                'username':'testuser4', 
                'password':'testpass', 
                'email':'test4@email.com'
                }
        res = self.client.post(
            '/register',
            data = user_data,
            follow_redirects=True)
        html = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('<div class="coins-query-searchbar">', html)
