function vul_detail(element, rij_naam, kolom_naam) {

    // Collect necessary data
    var element = $(element);
    var tabel = element.closest('table');
    var data = JSON.parse(tabel.attr('data'));
    var kolommen = JSON.parse(tabel.attr('detail_kolommen'))

    var rij_naam = tabel.attr('rij_naam');
    var kolom_naam = tabel.attr('kolom_naam');
    var rij_waarde = element.attr(rij_naam);
    var kolom_waarde = element.attr(kolom_naam);

    var sel = data.filter(rij => rij[rij_naam] == rij_waarde
                          && rij[kolom_naam] == kolom_waarde);

    // Delete the existing data and recreate table
    // I know this is not "reactive programming" but it's convenient for now
    d3.select('#Detail')
       .select('thead')
           .select('tr')
               .selectAll("th")
                   .remove();

   d3.select('#Detail')
       .select('tbody')
           .selectAll("tr")
               .remove();

   d3.select("#Detail")
       .select('thead')
           .select('tr')
               .selectAll('th')
                   .data(kolommen)
                   .enter()
               .append('th')
                   .classed("pvtTable pvtColLabel", true)
                   .text(head => head)

    d3.select('#Detail')
        .selectAll('tbody')
            .selectAll("tr")
                .data(sel)
                .enter()
            .append("tr")
                .selectAll("td")
                    .data(rij => kolommen.map(kolom => rij[kolom] || '-'))
                    .enter()
                .append("td")
                    .classed('pvtVal', true)
                    .text(value => value);

}