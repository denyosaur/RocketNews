let scrollCount = 26; // variable to hold the amount of coins to currently show
let ajaxCoinsLock = false; //variable to instantiate boolean used to pull information while true

//below methods handle the infinite scrolling.


/** Function to add more coins to list
 * On scroll, if ajaxCoinsLock is false, call getMoreCoins and add 10 coins
 */
$(window).scroll((evt) => {
    evt.preventDefault()
    if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10) {
        if (ajaxCoinsLock === true) {
            ajaxCoinsLock = false;
            return
        } else {
            ajaxCoinsLock = true; //set ajaxCoinsLock to true
            getMoreCoins(scrollCount); //function to call getMoreCoins
            scrollCount += 10; //add 10 to the variable count
        }
    }
});

/** Function for getting more coins
 * make a GET request to backend API to get info of more coins
 */
async function getMoreCoins(pageCount) {
    const res = await axios.get(`/coins/scroll/${pageCount}`); //back end API GET request
    let newCoins = res.data.data; //holds new coins results
    let followed = res.data.followed; //holds information on which coins are followed by user
    addCoinsToHtml(newCoins, followed); //function to add coin results to HTML
    ajaxCoinsLock = false; //set ajaxCoinsLock to false
}

/** Function to add coins resuls to HTML
 * pass in coins results and followed
 * create TR for new coin information. using followed, update the new TRs to reflect whether user follows it
 */
function addCoinsToHtml(newCoins, followed) {
    let button = `<i class="like-button bi bi-moon"></i>`;
    for (let newCoin of newCoins) {
        if (followed.includes(newCoin.symbol)) {
            button = `<i class="like-button bi bi-moon-stars-fill"></i>`
        } else {
            button = `<i class="like-button bi bi-moon"></i>`;
        }

        $(".table-body").append(`
        <tr class="coins-row">
            <td data-symbol="${newCoin.symbol}">
                ${button}
            </td>
            <th scope="row"><a href="/coins/${newCoin.symbol}">${newCoin.symbol}</a></th>
            <td class="name"><a href="/coins/{{coin.symbol}}">${newCoin.name}</a></td>
            <td class="dollars">${newCoin.quote.USD.price}</td>
            <td class="percent">${newCoin.quote.USD.percent_change_24h}</td >
            <td class="dollars">${newCoin.quote.USD.market_cap}</td>
            <td class="dollars">${newCoin.quote.USD.volume_24h}</td>
        </tr >
        `)
    }
}
