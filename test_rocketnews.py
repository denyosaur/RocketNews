from app import app
from unittest import TestCase
from flask import session

##app.config['TESTING'] = True
##app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class RocketNewsTestCase(TestCase):
    def setUp(self):
        with app.test_client() as client:
            app.config['TESTING'] = True
            app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
            ##db.create_all()

    ##def tearDown(self):
        ##db.session.remove()
        ##db.drop_all()
        ##self.app_context.pop()

    def test_homepage_not_logged_in(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/login')
            
    def test_login_page(self):
        with app.test_client() as client:
            res = client.get('/login')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Login</h1>', html)
    
    def test_register(self): 
        with app.test_client() as client:
            res = client.post('/register', data={
                'username':'testinguser',
                'password':'testingpassword',
                'email':'test@email.com'
            }, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Login</h1>', html)
