//functions helpers to handle infinite scrolling for news articles

let symbol = $(".symbol").text(); //variable to hold the coin's symbol of the current page
let paginationCount = 1; //variable for pagination, used for sending requests to external news API
let ajaxLock = false; //variable to instantiate boolean used to pull information while true

/** On Click for like button
 * handles click on like button (shape of moon). this adds the symbol of the coin to 
 * user's favorites
*/
$(document).on("click", ".like-button", (evt) => {
    $(evt.target).toggleClass("bi-moon-stars-fill bi-moon");

    let symbol = $(evt.target).parent().data("symbol");

    addCoinToFavorite(symbol);
});

/** functions for adding coin to favorite table
 * sends a POST request to backend api for adding or removing coin
*/
async function addCoinToFavorite(symbol) {
    const res = await axios.post(`/add/coin/${symbol}`);
    return res;
};

/** functions to handle infinite scrolling for news
 * On scroll down, if ajaxLock is false, increase paginagtion count
 * then get additional articles using coin symbol and pagination
*/
$(window).scroll((evt) => {
    evt.preventDefault()
    if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10) {
        if (ajaxLock === true) {
            ajaxLock = false;
            return
        } else {
            ajaxLock = true; //set ajaxCoinsLock to true
            paginationCount += 1; //increase pagination count for external GET request

            getCoinArticles(symbol, paginationCount); //function to call more articles
        }
    }
});

/** functions to get articles
 * function to call internal API (which then calls external API) gets news articles using symbol and pagination
 * then call addArticlesToHtml
*/
async function getCoinArticles(symbol, count) {
    const res = await axios.get(`/api/coin-news/${symbol}/${count}`);
    addArticlesToHtml(res);
    ajaxLock = false;
};

/** functions to add new articles to HTML
 * for each new article, add news information to HTML 
*/
function addArticlesToHtml(res) {
    article_info = res.data.articles; //instantiate articles to article_info
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
    `);
    };
};
