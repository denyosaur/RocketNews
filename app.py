from flask import Flask, render_template, jsonify, g, session, redirect, flash
from time import sleep
from functions import Coins, News
from models import db, User, CoinFollowed, CoinsList, connect_db
from form import UserRegistration, UserProfile, LoginForm
from sqlalchemy.exc import IntegrityError

import os

from flask_debugtoolbar import DebugToolbarExtension
#########################################################################################################
app = Flask(__name__)

## HEROKU env
#app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///rocket_news')).replace("://", "ql://", 1)
## dev env
## app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///rocket_news'))
## RENDER ENV
## app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL'))
app.config['SQLALCHEMY_DATABASE_URI'] = (os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

CURR_USER_KEY = 'curr_user'
cmc_api_key = '2ea12a6d-136b-4f0b-893e-dc5a065a8c74'
cmc_api_key2 = '500230bd-97f1-4df6-8369-cef1446e0cb3'

#########################################################################################################
coins = Coins()
news = News()
coinlist = CoinsList()
user= User()

#########################################################################################################
######     app.routes      ##############################################################################
#########################################################################################################

@app.before_request
def add_user_to_g():
    '''If user is logged into a valid account, add their account g
    else, leave it blank.'''
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def login_user(user):
    '''If user logs in, update session to include their id'''
    session[CURR_USER_KEY] = user.id

def logout_user():
    '''if user logs out, update session to remove their id in session'''
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

#########################################################################################################

@app.route('/')
def homepage():
    '''if user is correctly logged in, redirect them to /homepage
    else redirect them to the login page'''
    if g.user:
        username = g.user.username
        return redirect('/homepage')
    else:
        return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''GET and POST route for registering a new account
    if user is logged in, redirect them to the homepage if they try to access this link
    if the registration form is valid, create new user
    if username is invalid, flash a message'''
    if g.user:
        return redirect('/homepage')
    
    register_form = UserRegistration()
    if register_form.validate_on_submit():
        try:
            new_user = user.register(username=register_form.username.data, 
                                         password=register_form.password.data, 
                                         email=register_form.email.data)
            db.session.commit()

            login_user(new_user)
            return redirect('/homepage')
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('register.html', form=register_form)

    return render_template('register.html', form=register_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''GET and POST request for logging in.
    use validate_on_submit to capture the user's input and authenticate.
    if user is invalid, return user back to login page.'''
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.authenticate(login_form.username.data, login_form.password.data)
        
        if user:
            login_user(user)
            return redirect("/homepage")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=login_form)

@app.route('/logout')
def logout():
    '''log out the user by calling logout_user() function which removes user id from session'''
    logout_user()
    return redirect('/')

#########################################################################################################

@app.route('/homepage')
def logged_in_homepage():
    '''homepage route for logged in users. If not logged in, redirect to login page.
    this page shows any stocks and coins they follow and search bars for coins and stocks.
    passes list of followed coins and stocks to the jinja template'''

    if not g.user:
        return redirect('/login')

    user_info = g.user
    user_coins = g.user.coins
    followed_coins_symbol = coins.symbols_string(user_coins)
    followed_coins = coins.explore_coin_info(followed_coins_symbol)

    return render_template('users-homepage.html', user=user_info, followed_coins=followed_coins) #, followed_stocks=followed_stocks_info)

@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def view_user_info(user_id):
    '''users info page
    User can edit their username, email, and currency of'''
    if not g.user:
        return redirect("/")
    
    form = UserProfile(obj=g.user)

    if form.validate_on_submit():
        authenticate = user.authenticate(g.user.username, form.password.data)
        if authenticate:
            g.user.username = form.username.data
            g.user.email = form.email.data
            g.user.currency = form.currency.data

            db.session.add(g.user)
            db.session.commit()
            return redirect(f'/user/{g.user.id}')
        flash('Invalid Password', 'danger')

    user_info = User.query.get_or_404(user_id)
    return render_template('users-info.html', form=form)

@app.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def update_user_info():
    '''page to edit a user's info and also shows their info'''
    form_info = UserProfile(obj=g.user)

    if form_info.validate_on_submit():
        password = form_info.password.data
        if User.authenticate(g.user.password, password):
            g.user.username = form_info.username.data
            g.user.email = form_info.email.data
            g.user.currency = form_info.currency.data
            db.session.add(g.user)
            db.session.commit()
            return redirect(f'/user/{g.user.id}')
    return redirect('user-edit.html', obj=form_info)

#########################################################################################################
######    RocketNews JSON API    ########################################################################
#########################################################################################################

@app.route('/add/coin/<symbol>', methods=['POST'])
def add_followed_coin(symbol):
    '''App route for adding coins to a user's coin follow list
    if the coin is already on the followed list, remove it from the list
    this route returns a JSON confirming creation or deletion of the followed coin.
    if user is not logged in, redirect to /login page'''
    if not g.user:
        return redirect('/login')

    coin = CoinsList.query.filter_by(coin_symbol=symbol).first()
    followed_coin = CoinFollowed.query.filter_by(coin_cmc_id=coin.id).first()

    if followed_coin:
        CoinFollowed.query.filter_by(coin_cmc_id=coin.id).delete()
        db.session.commit()
        return (jsonify(info={
            'Message':'Successfully Deleted'
            }), 204)
    else:
        new_coin_followed = CoinFollowed.follow_coin(g.user.id, coin.id)
        db.session.commit()
        print(new_coin_followed)
        return (jsonify(info={
            'Message':'Successfully Added'
            }), 204)

@app.route('/coins/scroll/<int:page>')
def get_more_coins(page):
    '''app route for exploring all coins
    this route will call API from CMC and return the top 15 coins by market cap to be used in Jinja template

    pass to jinja template the top coins by market cap and a list of coins that the user followed (this is for marking coins as followed)
    if user is logged in, this route will also show which coins are being followed'''
    coin_list = coins.explore_all_coin_list(page, 15)
    followed_coins = g.user.coins
    followed_coins_symbol = coins.symbols_string(followed_coins)
    return jsonify(data=coin_list, followed=followed_coins_symbol)

@app.route('/api/coin-search/<input>')
def search_coin_db_similar(input):
    '''this route is used to search for coins in the database.
    route is used for search bar to find coins according to the users text inputs'''
    queried = coinlist.query.filter_by(coin_symbol=input).limit(10).all()
    query_obj = coins.coin_query_serialize(queried)
    print(query_obj)
    return jsonify(results=query_obj)

@app.route('/api/update-coin-list', methods=['GET', 'POST'])
def api_coin_list():
    '''NOT USABLE BY USERS - for back end updating DB only
    this route updates the coins database.
    pulls information from CMC which returns JSON. update the database with the JSON file'''
    coin_map = coins.coin_mapping()
    for coin in coin_map:
        coin_info = coins.push_coin_to_db(coin)
    
    db.session.commit()
    return render_template('index.html')

@app.route('/api/coin-news/<coin_symbol>/<int:count>', methods=['GET'])
def newsapi_articles(coin_symbol, count):
    '''app route for getting articles from News API. these articles are used for infinite scrolling
    - NewsAPI doesn't allow infinite scrolling to pull directly through Jquery, so back end api was required to pull. 
    - serialize the news articles into JSON format'''
    coin_info = coins.explore_coin_info(coin_symbol).get(coin_symbol)

    news_articles = news.get_coin_articles(coin_info, count).get("articles")

    serialized_articles = [news.serialize_articles(art) for art in news_articles]

    return jsonify(articles=serialized_articles)

#########################################################################################################
#########################################################################################################
#########################################################################################################

@app.route('/coins')
def coin_list():
    '''app route for exploring all coins
    if user is logged in, this route will also show which coins are being followed by markeitng them with different icon'''
    coin_list = coins.explore_all_coin_list(1, 25)

    if g.user:
        followed_ids = CoinFollowed.query.with_entities(CoinFollowed.coin_cmc_id).filter_by(user_id=g.user.id).all()
        followed_ids_list = [item[0] for item in followed_ids]
        return render_template('coin-list.html', coins=coin_list, followed=followed_ids_list)

    return render_template('coin-list.html', coins=coin_list)

@app.route('/coins/<coin_symbol>')
def coin_info(coin_symbol):
    '''app route for viewing a specific coins information, previous daily info, and news
    - coin_info - grab coin information
    - coin_history - get previous 60day performance for coin
    - if user is logged in, pass in information on which coins were followed
    '''
    coin_info = coins.explore_coin_info(coin_symbol).get(coin_symbol)
    coin_history = coins.explore_coin_history(coin_symbol)

    news_articles = news.get_coin_articles(coin_info, 1).get("articles")

    if g.user:
        followed_ids = CoinFollowed.query.with_entities(CoinFollowed.coin_cmc_id).filter_by(user_id=g.user.id).all()
        followed_ids_list = [item[0] for item in followed_ids]
        return render_template('coin-info.html', coin=coin_info, coin_history=coin_history, news_articles=news_articles, followed=followed_ids_list)

    return render_template('coin-info.html', coin=coin_info, coin_history=jsonify(coin_history), news_articles=news_articles)

#########################################################################################################
###   Error Handling   ##################################################################################
#########################################################################################################

@app.errorhandler(404)
def page_not_found(error):
    return render_template('ErrorPage/page_not_found.html'), 404

@app.errorhandler(500)
def page_not_found(error):
    return render_template('ErrorPage/page_not_found.html'), 500