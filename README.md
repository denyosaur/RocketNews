Rocket News: https://rocketnews.herokuapp.com/

Rocket News is used to track stocks and crypto currencies. A user can view specific stocks/coins to get a high level overview of performance and the most up to date news articles.

Features:
    - Homepage:
        - Ability to follow stocks and coins: Following coins will allow users to have faster access to view the details of their equity. These will be shown on the homepage.
        - Homepage also has two search bars to search through the database for specific equity. 
    - Equity info page:
        - The information page of the equity shows the high level overview of the equity. Daily price performance is shown here.
        - Previous 60 day daily perofrmance is also shown here through a a candlestick graph.
        - Stocks: Additional details about the company is shown on this page as well. Information includes company details, company description (what they do) and a list of similar companies.
        - News articles of the equity is also shown below using infinite scrolling. The articles will be the most popular articles of the previous two weeks.
    - Coins list page: This page offers a list of all the coins sorted by market cap.
    -Stock list page: This page has a search bar to search through the database for specific stocks.
    - User Account page:
        - This page gives the user the ability to change their username and email.

Userflow:
    - User will first register their account with username, email, and password.
    - The user will be automatically logged in and see the homepage.
        - The homepage will have two search bars, one for coins, the other for stocks. These are used to specifically search for their equity of interest.
        - The homepage also gives access to a url that will take user to a full list of coins or a page to search for stocks.
    - The user can follow equity through the coins list or the specific equity page.


APIs:
- Coin APIs:
    - coin API: https://coinmarketcap.com/api/documentation/v1/
    - coin and stock API: https://polygon.io/docs/getting-started 
- Stocks API:
    - AlphaVantage: https://www.alphavantage.co/documentation/ 
    - polygon.io: https://polygon.io/docs/getting-started - Some of the features of this API is broken and I found out too late. The stocks part still works, but I had to implement many work arounds to get everything to work. Unfortunately, AlphaVantage also uses polygon.io as a reference for many of their API routes.
- News APIs
    - google news api: https://newsapi.org/docs
    - bing news api: https://rapidapi.com/microsoft-azure-org-microsoft-cognitive-services/api/bing-news-search1?endpoint=apiendpoint_9c82a06e-fbb7-414d-b945-fce253310bba
    - bloomberg api: https://rapidapi.com/apidojo/api/bloomberg-market-and-financial-news

Tech Stack:

    - Front-End
        - Javascript
        - Jquery v3.6.0 and Axios
        - Bootstrap v5.0
        - Canvas.JS


    - Back-End
        - Python 
        - bcrypt v3.2.0
        - Flask 1.1.2
        - Flask WTF v0.14.2
        - SQLAlchemy v2.5.1
        - Jinja v2.11.3

