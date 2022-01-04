/** helpers to handle infinite scrolling for coins 
 * OOP class of helpers used to make GET request and add onto the current coins HTML list
 */

class CoinListHelpers {
    constructor () {
        this.scrollCount = 26; // variable to hold the amount of coins to currently show
        this.ajaxCoinsLock = false; //variable to instantiate boolean used to pull information while true
    }

    /** Function for getting more coins
     * make a GET request to backend API to get info of more coins
     */
    async getMoreCoins() {
        const res = await axios.get(`/coins/scroll/${this.scrollCount}`); //back end API GET request
        let newCoins = res.data.data; //holds new coins results
        let followed = new Set(res.data.followed.split(",")); //holds information on which coins are followed by user
        this.addCoinsToHtml(newCoins, followed); //function to add coin results to HTML
        this.ajaxCoinsLock = false; //set ajaxCoinsLock to false
    }

    /** functions for adding coin to favorite table
    * sends a POST request to backend api for adding or removing coin
    */
    async addCoinToFavorite(symbol) {
        const res = await axios.post(`/add/coin/${symbol}`);
        return res;
    }

    /** Function to add coins resuls to HTML
     * pass in coins results and followed
     * create TR for new coin information. using followed, update the new TRs to reflect whether user follows it
     */
    addCoinsToHtml(newCoins, followed) {
        if (newCoins) {
            for (let newCoin of newCoins) {
                const buttonStatus = followed.has(newCoin.symbol) ? `bi-moon-stars-fill` : `bi-moon`;
                const button = `<i class="like-button bi ${buttonStatus}"></i>`;

                const newCoinPrice = this.currencyFormatter(newCoin.quote.USD.price);
                const newCoinMarketCap = this.currencyFormatter(newCoin.quote.USD.market_cap);
                const newCoinVolume = this.currencyFormatter(newCoin.quote.USD.market_cap);
                const newCoinPercent = newCoin.quote.USD.percent_change_24h.toFixed(2);

                $(".CoinsTable-tbody").append(`
                <tr class="CoinsTable-row">
                    <th headers="CoinsTable-header2" class="CoinsTable-Row-Header" scope="row">
                        <div class="CoinsTable-like-button" data-symbol=${newCoin.symbol}>
                            ${button}
                        </div>
                        <a href="/coins/${newCoin.symbol}">
                            <div class="CoinsTable-name">
                                <div class="CoinsTable-name-name">${newCoin.name}</div> 
                                <div class="CoinsTable-name-symbol">${newCoin.symbol}</div>
                            </div>
                        </a>
                    </th>
                    <td headers="CoinsTable-header3" class="CoinsTable-Row-price">
                        <div class="CoinsTable-text">${newCoinPrice}</div>
                    </td>
                    <td headers="CoinsTable-header4">
                        <div class="CoinsTable-text">${newCoinPercent}%</div>
                    </td>
                    <td headers="CoinsTable-header5">
                        <div class="CoinsTable-text">${newCoinMarketCap}</div>
                    </td>
                    <td headers="CoinsTable-header6">
                        <div class="CoinsTable-text">${newCoinVolume}</div>
                    </td>
                </tr>
                `)
            }
        }
    }

    currencyFormatter (amount) {
        let formatter = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',     
        });
        return formatter.format(amount); 
    }
};

let CoinsHelpers = new CoinListHelpers();

/** Event Handler to add more coins to list
 * On scroll, if ajaxCoinsLock is false, call getMoreCoins and add 10 coins
 */
 $(".CoinsTable").scroll((evt) => {
    evt.preventDefault();
    const coinsTable = document.querySelector(".CoinsTable");

    if ($(".CoinsTable").scrollTop() + coinsTable.clientHeight >= coinsTable.scrollHeight - 50) {
        if (CoinsHelpers.ajaxCoinsLock === true) {
            CoinsHelpers.ajaxCoinsLock = false;
            //return;
        } else {
            CoinsHelpers.ajaxCoinsLock = true; //set ajaxCoinsLock to true
            CoinsHelpers.getMoreCoins(); //function to call getMoreCoins
            CoinsHelpers.scrollCount += 10; //add 10 to the variable count
        };
    };
});

/** On Click event handler for like button
 * handles click on like button (shape of moon). this adds the symbol of the coin to 
 * user's favorites
*/
$(document).on("click", ".like-button", (evt) => {
    $(evt.target).toggleClass("bi-moon-stars-fill bi-moon");
    
    let coinSymbol = $(evt.target).parent().data("symbol");
    CoinsHelpers.addCoinToFavorite(coinSymbol);
});