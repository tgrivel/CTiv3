function vul_detail(element, rij_naam, kolom_naam) {

    $("#Detail").show(100);

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

    // Highlight choice
    tabel.find('td').removeClass("selected");
    element.addClass("selected");

    var rij_naam_kort = rij_naam.split(":")[0];
    var rij_waarde_kort = rij_waarde.split(" ")[0];
    var header_text = 'Details voor cel:' + '\xa0 \xa0';
    header_text = header_text + '[ ' + rij_naam_kort + ': ' + rij_waarde_kort + '\xa0\xa0 | \xa0\xa0';
    header_text = header_text + kolom_naam + ': ' + kolom_waarde + ' ]';
    d3.select('#DetailScherm').selectAll("p").text(header_text);

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

function toevoegen_mutatie(el) {
    /**
    Make sure that what is entered as a mutation is entered correctly
    */
    var form = $(el).closest('form.muteerknoppen');
    var form_groups = form.find('.form-group');

    // Make dict out of entered input fields
    var mutatie_velden = {};
    for(var i=0; i < form_groups.length; i++) {
        var form_group = $(form_groups[i]);
        var variabele = form_group.attr('naam');
        var invoer_veld = form_group.find('.mutatie-invoer');
        var value = invoer_veld.val();

        if (variabele !== undefined ) {
            mutatie_velden[variabele] = value;
        }
    }

    // Clear losse input velden
    form.find('input').val(0);

    // Mark mutation as created by us
    mutatie_velden['opmerking'] = "Mutatie toegevoegd met CTiv3.";
    mutatie_velden['ctiv_mutatie'] = 1;

    console.log('Mutatie toevoegen met waarden', mutatie_velden);

    // Update data-attribuut in html tabel
    var tabblad = $(el).closest('.tabcontent');
    var pivotTabel = $($(tabblad).find('table.pvtTable'));
    var data = JSON.parse(pivotTabel.attr('data'));
    console.log(data);
    data.push(mutatie_velden);
    pivotTabel.attr('data', JSON.stringify(data));

    // TODO Update waarden in pivot table
    // Hiervoor heb ik informatie nodig over de hierarchie van rijen en kolommen
    // Extra probleem: Er kunnen ook kolommen en rijen bij komen

}
