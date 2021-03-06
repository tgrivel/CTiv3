const IS_TUSSENTOTAAL = '_is_tussentotaal';

function download_data(filename, meta, contact) {

    var data = {};
    var tabellen = $('table.pvtTable.draaitabel');
    for (var i = 0; i < tabellen.length; i++) {
        var tabel = $(tabellen[i]);
        var tabel_naam = tabel.attr('naam');
        const tabel_data = geef_data_uit_pivottabel(tabel)
        data[tabel_naam] = data_opschonen(tabel_data);
    }

    var json_bestand = {
        'metadata': meta,
        'contact': contact,
        'data': data
    };

    // Generate download link
    var text = JSON.stringify(json_bestand, null, 2);

    // Zorg dat downloads altijd eindigen op '.aangepast.json'
    var toevoeging = '.iv3_aangepast'
    var filename_new = (filename.replace('.json', "")
                                .replace(toevoeging, "")
                                .concat(toevoeging)
                                .concat('.json'));
    download(filename_new, text);
}

function download(filename, text) {
    // Code overgenomen van mikemaccana (sic)
    // https://stackoverflow.com/questions/3665115
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

function data_opschonen(data) {
    // Verwijder aggregaten uit de data
    return data.filter(record => record[IS_TUSSENTOTAAL] === undefined)
}

function geef_data_uit_pivottabel(tabel) {
    // Haal data op die in een tabel staat op en zet om naar json
    //
    // Dit kan op twee manieren:
    // Niet bewerkbare tabellen:
    // - Hier willen we de oorspronkelijke niet-geaggregeerde data teruggeven
    // Bewerkbare tabellen:
    // - Hier willen we de vulling weten van de tabel zoals je hem op het scherm ziet

    const bewerkbaar = tabel.attr("contenteditable").toLowerCase() == "true"

    if (!bewerkbaar) {
        return JSON.parse(tabel.attr("data"))
    } else {
        const rij_naam = tabel.attr("rij_naam")
        const kolom_naam = tabel.attr("kolom_naam")
        const cellen = tabel.find('tbody').find('td')

        let records = Array()

        for (i = 0; i < cellen.length; i++) {
            const row = $(cellen[i])
            const rij_waarde = row.attr(rij_naam)
            const kolom_waarde = row.attr(kolom_naam)
            const waarde = row.text().trim()

            // Sla lege cellen over
            if (waarde.trim() !== "") {
                let record = {}
                record[kolom_naam] = kolom_waarde
                record[rij_naam] = rij_waarde
                record["waarde"] = waarde
                records.push(record)
            }
        }

        return records
    }
}
