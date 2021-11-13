let scrollCount = 26;
let ajaxCoinsLock = false;
//below methods handle the infinite scrolling.
$(window).scroll((evt) => {
    evt.preventDefault()
    if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10) {
        if (ajaxCoinsLock == true) {
            return
        } else {
            ajaxCoinsLock = true;
            getMoreCoins(scrollCount);
            scrollCount += 10;
        }
    }
});

async function getMoreCoins(pageCount) {
    const res = await axios.get(`/coins/scroll/${pageCount}`);
    let newCoins = res.data.data;
    let followed = res.data.followed;
    addCoinsToHtml(newCoins, followed)
    ajaxCoinsLock = false;
}

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
