console.log('begin')
console.log(data)
console.log('end')

var sumOverSum = $.pivotUtilities.aggregators["Sum over Sum"]

$("#overzicht").pivotUI(
    data['waarden'], // .filter(function(cell) {return cell.rekeningkant == "lasten"}),
    {
        rows: ['taakveld'],
        cols: ['categorie'],
        vals: ['bedrag'],
        // aggregator: [sumOverSum],
        showUI: false,
        // renderers: $.pivotUtilities.d3_renderers
    }
);


// d3.select("#detail")
// 	.selectAll('th')
// 	.data(Object.keys(dida['waarden'][0]))
// 	.enter()
// 	.append('th').text(function(x) {return x})
//
// 	//.data([1, 2, 3, 4, 4])
// d3.select('#detail')
// 	.selectAll("tr")
// 	//.data(dida['waarden'].map(function(x) {return x.bedrag}))
// 	.data(dida['waarden'])
// 	.enter()
// 	.append("tr")
// 	.selectAll('td')
//         .data(function(waarde) {return Object.values(waarde)})
// 	.enter()
// 	.append('td')
// 	.text(function(value) {return (value)});

// d3.select('#overzicht').text("overzicht")

