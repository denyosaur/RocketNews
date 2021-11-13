$("input").keyup((evt) => {
    evt.preventDefault();
    let query = $("input").val().toUpperCase();
    getSearchResults(query)
})

async function getSearchResults(query) {
    const res = await axios.get(`/api/stock-search/${query}`);
    addQueryToHtml(res)
    return res
}

function addQueryToHtml(res) {
    let results = res.data.results;
    for (let stock of results) {
        $(".query-list").append(`
        <li class="query">
            <div>
                <span class="text-left"><a href="/stocks/${stock.stock_symbol}">${stock.stock_symbol} -
                    </a></span>
                <span class="text-right"><a
                        href="/stocks/${stock.stock_symbol}">${stock.company_name}</a></span>
            </div>
        </li>
    `)
    }
}