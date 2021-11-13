"""methods for coin app."""
from requests import Session

from models import db, CoinsList
# from models import db, StocksList, CoinsList
from datetime import datetime
import datetime
import requests

session = Session()

class Coins():
    def __init__(self):
        self.cmc_api_key = '2ea12a6d-136b-4f0b-893e-dc5a065a8c74'
        self.cmc_api_key2 = '500230bd-97f1-4df6-8369-cef1446e0cb3'
        self.av_api_key = '2M6OIS2G7ADE4Y43'

        self.av_url = 'https://www.alphavantage.co/query?'
        self.cmc_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency'
        self.coinlist = CoinsList()

    def coin_mapping(self):
        '''get coin name, coin symbol, and CMC specific coin ID from the CMC api key
        this is used to update the database with all the coins'''
        coin_map_url = f'{self.cmc_url}/map'
        params ={
            'sort':'cmc_rank'
            }
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": self.cmc_api_key
            }

        res = requests.get(coin_map_url, headers=headers, params=params).json()
        coin_map = res.get("data")
        return coin_map

    def push_coin_to_db(self, data):
        '''push the results of coin_mapping() to our tracker DB. Check whether the coin exists
        this updates the CoinList table'''
        cmc_id = data.get("id")
        coin_symbol = data.get("symbol")
        coin_name = data.get("name")

        exists = CoinsList.query.get(cmc_id) is not None

        if exists:
            return
        else:
            coin_info = CoinsList(
                id=cmc_id, 
                coin_symbol=coin_symbol, 
                coin_name=coin_name
                )
            db.session.add(coin_info)
            return
    
    def explore_all_coin_list(self, start, count): 
        '''API request to get a list of coins that are sorted by market cap
        this function is used for the explore coins page and for the price point history table'''
        explore_coin_url = f'{self.cmc_url}/listings/latest'
        params = {
            'start':start,
            'limit': count,
            'sort': 'market_cap'
            }
        headers = {
            'Accepts':'application/json',
            'X-CMC_PRO_API_KEY': self.cmc_api_key
            }

        res = requests.get(explore_coin_url, headers=headers, params=params).json()
        coins_data = res.get("data")
        return coins_data

    def explore_coin_info(self, symbol):
        '''function to request coin info from CMC API 
        this returns coin name, and other coin price info'''
        coin_url = f'{self.cmc_url}/quotes/latest'
        params = {
            'symbol': symbol,
            'convert': 'USD'
            }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.cmc_api_key2
            }

        res = requests.get(coin_url, headers=headers, params=params).json()
        coin_data = res.get("data")
        return coin_data
    
    def explore_coin_history(self, symbol):
        '''function to request past seven day coin info from AV API '''
        av_url =  f'{self.av_url}/listings/latest'
        params = {
            'function': 'DIGITAL_CURRENCY_DAILY',
            'symbol': symbol,
            'market': 'USD',
            'apikey': self.av_api_key
            }

        res = requests.get(av_url, params=params).json()
        return res

    def symbols_string(self, obj):
        '''take in an object of coins that user follows and return an array of only the symbols
        this is used to pass along list of followed coins from front end to back end'''
        string = ""

        for info in obj:
            string+=info.coin_symbol
            string+=","

        return string[:(len(string)-1)]

    def coin_query_serialize(self, obj):
        '''serialize coin information into JSON format'''
        serialized = []
        for query in obj:
            serialized.append({
                'coin_symbol':query.coin_symbol,
                'coin_name':query.coin_name
            })
        return serialized

# class Stocks():
#     def __init__(self):
#         self.av_apikey = '2M6OIS2G7ADE4Y43'
#         self.polygon_apikey = 'rmdZyMBXEpepgMrKJzY4So_ds9zoioMx'
#         self.polygon_apikey2 = 'Tl5PAvzoLu3eIpCuAftOakqViaxV_kEu'
#         self.polygon_apikey3 = 'VONeHzDUSptWoQjpi94nAT6dsLekfLVq'

#         self.av_url = 'https://www.alphavantage.co/query?'
#         self.polygon_url = 'https://api.polygon.io'

#     def stock_mapping(self, page):
#         '''get Stock, Stock name, and CMC specific coin ID from the CMC api key'''
#         polygon_map_url = f'{self.polygon_url}/v2/reference/tickers'
#         params ={
#             'page':page,
#             'active':'true',
#             'sort':'ticker',
#             'type':'cs',
#             'perpage':'50',
#             'apiKey':self.polygon_apikey
#             }
#         res = requests.get(polygon_map_url, params=params).json()
#         tickers = res.get('tickers')
#         return tickers

#     def push_stock_to_db(self, data):
#         '''push the stock map to our DB. this updates the StockList table'''
#         ticker = data.get("ticker")
#         company_name = data.get("name")
#         country = data.get("locale")

#         exists = StocksList.query.filter_by(stock_symbol=ticker).first() is not None

#         if exists:
#             return
#         else:
#             stock_info = StocksList(
#                 stock_symbol=ticker, 
#                 company_name=company_name,
#                 country=country
#                 )
#             db.session.add(stock_info)
#             return
    
#     def explore_stock_info(self, symbol):
#         '''function to request stock info from Polygon API 
#         this returns ticker information for specific stock'''
#         date = self.get_valid_date()
#         ticker_details_url = f'{self.polygon_url}/v2/aggs/ticker/{symbol}/range/1/minute/{date[1]}/{date[0]}?'
#         params = {
#             'apikey':self.polygon_apikey3,
#             'unadjusted':'true',
#             'sort':'asc',
#             'limit':'1',
#         }
#         res = requests.get(ticker_details_url, params=params).json()
#         if 'results' not in res:
#             return {'results':[{
#                 'T': symbol,
#                 'v': 'N/A',
#                 'vw': 'N/A',
#                 'o': 'N/A',
#                 'c': 'N/A',
#                 'h': 'N/A',
#                 'l': 'N/A',
#                 't': 'N/A'
#             }]}
#         return res

#     def followed_stock_info(self, followed):
#         '''this is used to parse through and return info that users are following
#         if no stocks are followed, return an empty json form'''
#         followed_stocks_info = []
#         all_info = self.all_stock_info().get('results')
#         for followed_stock in followed:
#             stock_grouped = [stock for stock in all_info if stock['T'] == followed_stock.stock_id]
#             if len(stock_grouped) == 0:
#                 followed_stocks_info.append({
#                     'T':followed_stock.stock_id,
#                     'c':'N/A',
#                     'h':'N/A',
#                     'l':'N/A',
#                     'v':'N/A'
#                 })
#             else :
#                 followed_stocks_info.append(stock_grouped[0])
#         return followed_stocks_info

#     def all_stock_info(self):
#         '''this function gets JSON file from polygon.io
#         Get the daily open, high, low, and close (OHLC) for the entire stocks/equities markets
#         this is used to parse through and return info that users are following'''
#         date = self.get_valid_date()

#         url = f'{self.polygon_url}/v2/aggs/grouped/locale/us/market/stocks/{date[0]}?'
#         params = {
#             'unadjusted':'true',
#             'apiKey':self.polygon_apikey2
#         }

#         res = requests.get(url, params=params).json()
#         return res

#     def get_valid_date(self):
#         '''returns valid date format and weekdays that can be sent to polygon. 
#         - Polygon will return an error for stocks if any weekend dates are sent.
#         returned dates are in a list. 
#         - If today's date is a weekend, the list will contain Friday's date and Thursday's date
#         - [0] is current date, [1] is previous date
#         valid date format: "YYYY-MM-DD"'''
#         date = datetime.datetime.now()
#         today_no = date.weekday()
#         if today_no == 6:
#             valid_day = date - datetime.timedelta(2)
#             previous_day = valid_day - datetime.timedelta(1)
#             return [valid_day.strftime("%Y-%m-%d"), previous_day.strftime("%Y-%m-%d")]
#         elif today_no == 5:
#             valid_day = date - datetime.timedelta(1)
#             previous_day = valid_day - datetime.timedelta(1)
#             return [valid_day.strftime("%Y-%m-%d"), previous_day.strftime("%Y-%m-%d")]
#         else: 
#             previous_day = date - datetime.timedelta(1)
#             return [date.strftime("%Y-%m-%d"), previous_day.strftime("%Y-%m-%d")]
    
#     def explore_company_info(self, symbol):
#         '''function to request company info from Polygon API 
#         this returns company information for specific stock'''
#         company_details_url = f'{self.polygon_url}/v1/meta/symbols/{symbol}/company?&apiKey={self.polygon_apikey3}'
        
#         res = requests.get(company_details_url).json()
#         return res

#     def explore_stock_history(self, symbol):
#         '''function to request past seven day stock info from AV API '''
#         params = {
#             'function':'TIME_SERIES_DAILY_ADJUSTED',
#             'symbol': symbol,
#             'outputsize':'compact',
#             'datatype':'json',
#             'apikey': self.av_apikey
#             }

#         res = requests.get(self.av_url, params=params).json()
#         return res

#     def stock_query_serialize(self, obj):
#         '''returns a JSON format list of followed stocks'''
#         serialized = []
#         for query in obj:
#             serialized.append({
#                 'stock_symbol':query.stock_symbol,
#                 'company_name':query.company_name
#             })
#         return serialized

class News():
    def __init__(self):
        self.newsapi_api = 'eb15841b2cb44f50bc9102dc9b3fb60a'
        self.newsapi_api2 = '99a3f82f070a4e848b6bb98b724179b0'
        self.polygon_apikey3 = 'VONeHzDUSptWoQjpi94nAT6dsLekfLVq'

        self.newsapi_counter = 0
 
        self.newsapi_url = 'https://newsapi.org/v2/everything'
        self.polygon_url = 'https://api.polygon.io'

        self.date = datetime.datetime.now().strftime('%m-%d-%Y')
        self.previous_week = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%m-%d-%y")

    def get_coin_articles(self, info_obj, count):
        '''get news articles for specific coins
        The counter is used to use either the first or second API. this is to not be blocked by the site'''
        params = self.news_params(info_obj, count)
        
        res = requests.get(self.newsapi_url, params=params).json()

        if self.newsapi_counter == 0:
            self.newsapi_counter += 1
        else:
            self.newsapi_counter -= 1

        return res

    # def get_stock_articles(self, symbol, page):
    #     '''get news articles from polygon.io. the stock symbol and the page required is passed along'''
    #     poly_article_url = f'{self.polygon_url}/v1/meta/symbols/{symbol}/news'
    #     params = {
    #         'perpage':10,
    #         'page':page,
    #         'apiKey':self.polygon_apikey3
    #     }
        
    #     res = requests.get(poly_article_url, params=params).json()

    #     return res

    def news_params(self, obj, count):
        '''creates the news parameters for the NewsAPI'''
        if self.newsapi_counter == 0:
            self.newsapi_counter += 1
            apikey = self.newsapi_api
        else:
            self.newsapi_counter -= 1
            apikey = self.newsapi_api2

        name = obj["name"]
        symbol = obj["symbol"]
        return {
            "q": name,
            "q": symbol,
            "language": "en",
            "sortBy":"popularity",
            "pageSize":"10",
            "apiKey":self.newsapi_api,
            "page":count
            }
    
    def serialize_articles(self, article):
        return {
            'source': article["source"]["name"],
            'author': article["author"],
            'title': article["title"],
            'description': article["description"],
            'url': article["url"],
            'image':article["urlToImage"]
        }