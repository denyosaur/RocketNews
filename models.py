"""SQLAlchemy models for crypto tracker."""
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    '''table of user's info'''
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    currency = db.Column(db.Text, nullable=True, default='USD')

    coins = db.relationship('CoinsList', secondary='coin_followed', backref='users')
    # stocks = db.relationship('StocksList', secondary='stock_followed', backref='user')

    def __repr__(self):
        return f'user_info #{self.id}: {self.username}, {self.email}'

    @classmethod
    def register(cls, username, email, password):
        '''sign up for user'''
        hashed_pw = bcrypt.generate_password_hash(password).decode('UTF-8')

        new_user = User(username=username, password=hashed_pw, email=email)
        db.session.add(new_user)
        return new_user
    
    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False

class CoinFollowed(db.Model):
    '''table of crypto currencies that users followed'''
    __tablename__='coin_followed'
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('user_info.id'), 
                        primary_key=True)
    coin_cmc_id = db.Column(db.Integer, 
                            db.ForeignKey('coin_list.id'), 
                            primary_key=True)
    favorited = db.Column(db.Boolean)

    @classmethod
    def follow_coin(cls, user_id, coin_id):
        new_coin = CoinFollowed(user_id=user_id, coin_cmc_id=coin_id)
        db.session.add(new_coin)
        return new_coin

# class StockFollowed(db.Model):
#     '''table of stocks that users followed'''
#     __tablename__='stock_followed'
#     user_id = db.Column(db.Integer, 
#                         db.ForeignKey('user_info.id'), 
#                         primary_key=True)
#     stock_id = db.Column(db.Text, 
#                         db.ForeignKey('stock_list.stock_symbol'), 
#                         primary_key=True)
#     favorited = db.Column(db.Boolean)

#     @classmethod
#     def follow_stock(cls, user_id, stock_id):
#         new_stock = StockFollowed(user_id=user_id, stock_id=stock_id)
#         db.session.add(new_stock)
#         return new_stock

# class StocksList(db.Model):
#     '''list of all the stocks'''
#     __tablename__='stock_list'
#     stock_symbol = db.Column(db.Text, unique=True, nullable = False, primary_key=True)
#     company_name = db.Column(db.Text, nullable = False)
#     company_industry = db.Column(db.Text)
#     sector = db.Column(db.Text)
#     country = db.Column(db.Text)

class CoinsList(db.Model):
    '''list of all the crypto currencys'''
    __tablename__='coin_list'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    coin_symbol = db.Column(db.Text)
    coin_name = db.Column(db.Text)

class CurrencyList(db.Model):
    '''list of all traditional currencies that are supported'''
    __tablename__='traditional_currencies'
    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.Text)
    currency_name = db.Column(db.Text)
    
def connect_db(app):
    '''connect DB to flask app'''
    db.app = app
    db.init_app(app)