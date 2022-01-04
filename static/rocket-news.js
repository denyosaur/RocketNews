/** helpers to handle infinite scrolling for News Articles 
 * OOP class of helpers used to make GET request and add onto the current news HTML list
 */
class NewsListHelpers {
    constructor () {
        this.symbol = $(".symbol").text();
        this.paginationCount = 1; //variable for pagination, used for sending requests to external news API
        this.ajaxLock = false; //variable to instantiate boolean used to pull information while true
    }

    /** On Click for like button
     * handles click on like button (shape of moon). this adds the symbol of the coin to 
     * user's favorites
    */
    async addCoinToFavorite() {
        const res = await axios.post(`/add/coin/${this.symbol}`);
        return res;
    }

    /** functions to get articles
     * function to call internal API (which then calls external API) gets news articles using symbol and pagination
     * then call addArticlesToHtml
    */
    async getCoinArticles() {
        const res = await axios.get(`/api/coin-news/${this.symbol}/${this.paginationCount}`);
        this.addArticlesToHtml(res);
        this.ajaxLock = false;
        this.paginationCount += 1; //increase pagination count for external GET request
    }

    /** functions to add new articles to HTML
     * for each new article, add news information to HTML 
    */
    addArticlesToHtml(res) {
        let article_info = res.data.articles; //instantiate articles to article_info
        for (let article of article_info) {
            $(".article-section").append(`
            <div class="card">
            <div class="card-body">
                <div class="article-image-title">
                    <div class="article-image">
                        <a href="${article.url}">
                            <img src="${article.image}" alt="article-image"
                                onerror="this.src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkWfbGNKZyGwrxymaoronVG972LJ0Nd3OspQ&usqp=CAU';">
                        </a>
                    </div>
                    <div class="article-title text-decoration-none">
                        <a href="${article.url}">
                            <h4>${article.title}</h4>
                        </a>
                    </div>
                </div>
                <div class="article-info">
                    <div class="article-source text-decoration-none">
                        <a href="${article.url}">${article.source}</a>
                    </div>
                    <div class="article-author">
                        <span>Created By: ${article.source}</span>
                    </div>
                    <div class="article-description">
                        <span>${article.description}</span>
                    </div>
                </div>
            </div>
        </div>
        `)
        }
    }
};

let NewsHelpers = new NewsListHelpers();

/** Event Handler to add more articles to list
 * On scroll, if ajaxCoinsLock is false, call getCoinArticles and add additional articles
 */
 $(window).scroll((evt) => {
    evt.preventDefault()

    if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10) {
        if (NewsHelpers.ajaxLock === true) {
            NewsHelpers.ajaxLock = false;
        } else {
            NewsHelpers.ajaxLock = true; //set ajaxCoinsLock to true
            NewsHelpers.getCoinArticles(); //function to call more articles
        }
    }
});

/** On Click event handler for like button
 * handles click on like button (shape of moon). this adds the symbol of the coin to 
 * user's favorites
*/
$(document).on("click", ".like-button", (evt) => {
    $(evt.target).toggleClass("bi-moon-stars-fill bi-moon");

    let coinSymbol = $(evt.target).parent().data("symbol");

    NewsHelpers.addCoinToFavorite(coinSymbol);
});
