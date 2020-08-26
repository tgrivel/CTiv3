
function knop_werkt_niet() {

    alert("Deze knop werkt nog niet.");
};

function formulier_bulkcorrecties_leegmaken() {

    document.getElementById("Form_bulkcorrecties").reset();
};

function form_control_changed_type(corr) {

    alert("Gewijzigd: " + corr.attr("id"));

    let type_selected = corr.find("#type").children("option:selected").val();

    let rij_selected = corr.find("#rij_soort").children("option:selected").val();

    let kol_selected = corr.find("#kolom_soort").children("option:selected").val();

    alert("Geselecteerd: " + type_selected + " ; " + rij_selected + " ; " + kol_selected);

    // reset selectie van rij_soort
    let x = corr.find("#rij_soort").closest("select");
    x.val(x.data("default-value"));

    // reset selectie van kolom_soort
    x = corr.find("#kolom_soort").closest("select");
    x.val(x.data("default-value"));

    // reset selectie van bedrag
    x = corr.find("#bedrag");
    x.val("0");

    // reset selectie van bedrag
    x = corr.find("#opmerking");
    x.val("Bulkcorrectie Ocido");

};

function form_control_changed_rij(corr) {

    alert("Rij - Gewijzigd: " + corr.attr("id"));
};


function form_control_changed_kol(corr) {

    alert("Kolom - Gewijzigd: " + corr.attr("id"));
};
