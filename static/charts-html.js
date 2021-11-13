// Jquery for handling the population of candlestick graphs

let history = $("#performance-history").data("history"); //grab coin history info from data in html page
let historyDataJson = JSON.parse(history.replace(/'/g, '"').replace(/-/g, '')); //replace all ' to create json form. then remove all dash from dates
let metaData = Object.values(historyDataJson)[0];//grab only the coin history meta data
let historyInfo = Object.values(historyDataJson)[1]; //grab only the coin history object
let sortedDates = sortDateKeys(historyInfo); //this is an array of sorted dates that are converted to integer
//function to create data points used in chart.js.
function createDataPoints(obj, dates) {
    let dataPoints = [];

    for (let date of dates) {
        let price = Object.values(obj[date]);
        let dateStr = date.toString();

        let year = parseInt(dateStr.slice(0, 4));
        let month = parseInt(dateStr.slice(4, 6)) - 1;
        let day = parseInt(dateStr.slice(6)) - 1;

        dataPoints.push({
            x: new Date(year, month, day),
            y: makeCandleSticks(price)
        });
    }

    return dataPoints;
}

//function to convert all dates in coin history object to Integer form and return only previous 30 days. 
function sortDateKeys(obj) {
    let dateKeys = Object.keys(obj);
    let dateArray = []

    for (let date of dateKeys) {
        dateArray.push(parseInt(date.replaceAll("-", "")))
    }
    return dateArray.sort((a, b) => b - a).slice(0, 59);
}

function makeCandleSticks(obj) {
    if (identifier == "stocks") {
        return [
            parseFloat(obj[0]),
            parseFloat(obj[1]),
            parseFloat(obj[2]),
            parseFloat(obj[4])
        ];
    } else {
        return [
            parseFloat(obj[0]),
            parseFloat(obj[2]),
            parseFloat(obj[4]),
            parseFloat(obj[6])
        ];
    };
};

//on document ready, populate the candlestick chart
$(document).ready(() => {
    $(".candleStickContainer").CanvasJSChart({
        zoomEnabled: true,
        exportEnabled: true,
        axisY: {
            includeZero: false,
            title: "Price",
            prefix: "$"
        },
        axisX: {
            interval: 2,
            valueFormatString: "DD-MMM-YY",
            labelAngle: -50
        },
        data: [
            {
                type: "candlestick",
                dataPoints: createDataPoints(historyInfo, sortedDates)
            }
        ]
    });
});


