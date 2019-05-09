function download_data(filename, meta, contact) {

    // TODO Dit is een beginnetje, maar bevat nu nog alleen de data (alles op een hoop)
    var data = {};

    var tabellen = $('table.pvtTable.draaitabel');
    for (var i = 0; i < tabellen.length; i++) {
        var tabel = $(tabellen[i]);
        var tabel_naam = tabel.attr('naam');
        var tabel_data = JSON.parse(tabel.attr('data'));

        // This is like extend in Python (Javascript is weird!)
        // According to https://jsperf.com/concat-array-in-place it's very fast
        // Array.prototype.push.apply(data, tabel_data);
        data[tabel_naam] = tabel_data;
    }

    // Haal globale variabele op
    // var meta = window.meta;
    // var contact = window.contact;
    // var filename = window.filename;

    // FIXME Deze variabelen doorgeven aan deze functie lukt mij niet
    // var meta = 'lukt niet om meta op te halen'
    // var contact = 'lukt niet om contact op te halen'

    json_bestand = {
        'metadata': meta,
        'contact': contact,
        'data': data
    }

    // Generate download link
    var text = JSON.stringify(json_bestand, null, 2);
    download('data.json', text);
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