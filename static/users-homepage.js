let identifier = $("#identifier").data("identifier");
let symbol = $(".symbol").text()
let paginationCount = 1;

$(document).on("click", ".like-button", (evt) => {
    $(evt.target).toggleClass("bi-moon-stars-fill bi-moon");
    let symbol = $(evt.target).parent().data("symbol");
    // let type = $(evt.target).parent().data("type");

    $(evt.target).closest(".followed").remove();
    addCoinToFavorite(symbol);

    // if (type == "stocks") {
    //     addStockToFavorite(symbol);
    // } else if (type == "coins") {
    //     addCoinToFavorite(symbol);
    // }
})


// async function addStockToFavorite(symbol) {
//     const res = await axios.post(`/add/stock/${symbol}`);
//     return res;
// }

//functions for adding coin to favorite table
async function addCoinToFavorite(symbol) {
    const res = await axios.post(`/add/coin/${symbol}`);
    return res;
}

$(".search-input-coins").keyup((evt) => {
    evt.preventDefault();
    let query = $(".search-input-coins").val().toUpperCase();
    searchCoins(query);
    $('.query-list-coins').empty();
})

async function searchCoins(query) {
    const res = await axios.get(`/api/coin-search/${query}`);
    addCoinQueryToHtml(res);
    return res;
}

//function to add returned query from database. for coins search bar
function addCoinQueryToHtml(res) {
    let results = res.data.results;
    for (let coin of results) {
        $(".query-list-coins").append(`
        <li class="query-results">
                <span class="text-left">
                    <a href="/coins/${coin.coin_symbol}">
                        ${coin.coin_symbol}
                    </a>
                </span>
                <span class="text-right">
                    <a href="/coins/${coin.coin_symbol}">
                        ${coin.coin_name}
                    </a>
                </span>
        </li>
    `)
    }
}

// $(".search-input-stocks").keyup((evt) => {
//     evt.preventDefault();
//     let query = $(".search-input-stocks").val().toUpperCase();
//     searchStocks(query);
//     $('.query-list-stocks').empty();
// })

// async function searchStocks(query) {
//     const res = await axios.get(`/api/stock-search/${query}`);
//     console.log(res);
//     addStockQueryToHtml(res);
//     return res;
// }

// //function to add returned query from database. for stocks search bar
// function addStockQueryToHtml(res) {
//     let results = res.data.results;
//     for (let stock of results) {
//         $(".query-list-stocks").append(`
//         <li class="query-stocks">
//                 <span class="text-left"><a href="/stocks/${stock.stock_symbol}">${stock.stock_symbol}
//                     </a></span>
//                 <span class="text-right"><a
//                         href="/stocks/${stock.stock_symbol}">${stock.company_name}</a></span>
//         </li>
//     `);
//     };
// }