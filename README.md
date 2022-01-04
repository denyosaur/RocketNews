**Rocket News** 
=====================================

Rocket News is used to track crypto currency prices and performances. A user can view specific coins to get a high level overview of performance and the most up to date news articles.
https://rocketnews.herokuapp.com/

**Features**
---------------
The purpose of this project was to implement a full stack web app. The front end was designed with mobile first in mind, then larger screen sizes. This web app is a practice in utilizing various external web APIs as well as the creation and utilization of internal APIs. 

**Features**
---------------
- Homepage:
    - Ability to follow coins: Following coins will allow users to have faster access to view the details of their equity. These will be shown on the homepage.
    - Homepage also has two search bars to search through the database for specific equity. 
- Equity info page:
    - The information page of the equity shows the high level overview of the equity. Daily price performance is shown here.
    - Previous 60 day daily perofrmance is also shown here through a a candlestick graph.
    - Stocks: Additional details about the company is shown on this page as well. Information includes company details, company description (what they do) and a list of similar companies.
    - News articles of the equity is also shown below using infinite scrolling. The articles will be the most popular articles of the previous two weeks.
- Coins list page: This page offers a list of all the coins sorted by market cap.
- User Account page:
    - This page gives the user the ability to change their username and email.

**Userflow**
---------------
- Users without logins will be able to view a list of all the coins. 
    - This list initially shows 25 results but will add additional coins through use of infinite scrolling.
    - If a user is logged in, they will be able to favorite their coins.
- Users will first register their account with username, email, and password.
- The user will be automatically logged in and see the homepage.
    - The homepage will have a search bar for looking up coins. As the user types, the search bar will auto update results.
- Clicking on specific coins will lead users to a page with additional details on the coins performance.
    - This page also includes new articles that are related to the coin.


**APIs**
---------------
- Coin APIs:
    - coin API: https://coinmarketcap.com/api/documentation/v1/
    - coin API: https://polygon.io/docs/getting-started 
- News APIs
    - Google News API: https://newsapi.org/docs
    - Bing News API: https://rapidapi.com/microsoft-azure-org-microsoft-cognitive-services/api/bing-news-search1?endpoint=apiendpoint_9c82a06e-fbb7-414d-b945-fce253310bba
    - Bloomberg API: https://rapidapi.com/apidojo/api/bloomberg-market-and-financial-news

**Tech Stack**
---------------

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

