let identifier = $("#identifier").data("identifier");
let symbol = $(".symbol").text()
let paginationCount = 1;

/** On Click for like button
 * handles click on like button (shape of moon). this adds the symbol of the coin to 
 * user's favorites
*/
$(document).on("click", ".like-button", (evt) => {
    $(evt.target).toggleClass("bi-moon-stars-fill bi-moon"); //toggles the class to fill/nofill
    let symbol = $(evt.target).parent().data("symbol"); //symbol is stored in data, instantiate data

    $(evt.target).closest(".followed").remove();//remove followed class
    addCoinToFavorite(symbol); //calls function to add or remove coin from favorite
})

/** functions for adding coin to favorite table
 * sends a POST request to backend api for adding or removing coin
*/
async function addCoinToFavorite(symbol) {
    const res = await axios.post(`/add/coin/${symbol}`);
    return res;
}

/** On key up in query send a search 
 * used for searching coins and returning search results as user searches
 */
$(".search-input-coins").keyup((evt) => {
    evt.preventDefault();
    let query = $(".search-input-coins").val().toUpperCase(); //change user's input to all uppercase and instantiate
    searchCoins(query); //call funtion to search the current query
    $('.query-list-coins').empty(); //as search updatede results are returned, empty the query list
})

/** function for search query
 * sends a GET request to backend api for search query
 */
async function searchCoins(query) {
    const res = await axios.get(`/api/coin-search/${query}`);
    addCoinQueryToHtml(res);
    return res;
}

/** function to add search query results to HTML
 * takes in return results form search and adds line items to HTML list
 */
function addCoinQueryToHtml(res) {
    let results = res.data.results;
    for (let coin of results) {
        $(".query-list-coins").append(`
        <li class="query-results">
            <a href="/coins/${coin.coin_symbol}">${coin.coin_symbol}</a>
            <a href="/coins/${coin.coin_symbol}">${coin.coin_name}</a>
        </li>
    `)
    }
}