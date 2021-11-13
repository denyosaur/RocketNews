let identifier = $("#identifier").data("identifier");
let symbol = $(".symbol").text()
let paginationCount = 1;

$(document).on("click", ".like-button", (evt) => {
    $(evt.target).toggleClass("bi-moon-stars-fill bi-moon");

    let symbol = $(evt.target).parent().data("symbol")

    if (identifier == "stocks") {
        addStockToFavorite(symbol);
    } else if (identifier == "coins") {
        addCoinToFavorite(symbol);
    }
})

//functions for adding coin or stocks to favorite table
async function addStockToFavorite(symbol) {
    const res = await axios.post(`/add/stock/${symbol}`);
    return res;
}
async function addCoinToFavorite(symbol) {
    const res = await axios.post(`/add/coin/${symbol}`);
    return res;
}

// Jquery for handling the population of candlestick graphs

let ajaxLock = false;

//below methods handle the infinite scrolling.
$(window).scroll((evt) => {
    evt.preventDefault()
    if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10) {
        if (ajaxLock == true) {
            return
        } else {
            ajaxLock = true;
            paginationCount += 1;
            if (identifier == "stocks") {
                getStockArticles(symbol, paginationCount);
            } else {
                getCoinArticles(symbol, paginationCount)
            }
        }
    }
});

//get news articles through axios 
async function getCoinArticles(symbol, count) {
    const res = await axios.get(`/api/coin-news/${symbol}/${count}`);
    addArticlesToHtml(res);
    ajaxLock = false;
}

async function getStockArticles(symbol, count) {
    const res = await axios.get(`/api/stock-news/${symbol}/${count}`);
    addArticlesToHtml(res);
    ajaxLock = false;
}

function addArticlesToHtml(res) {
    article_info = res.data.articles
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
