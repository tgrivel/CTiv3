
function initialiseer_form_controls_bulkcorrecties() {

    let form_bulk = $("#Form_bulkcorrecties");
    if (form_bulk.length){
        //alert("Form gevonden");

        let bulkcorrecties = form_bulk.find("div[id^='bulkcorr_']");

        $.each(bulkcorrecties, function(key, corr) {

            // voeg events toe aan form-controls:
            // change(): type, rij_soort, kolom_soort
            // click():  reset

            $(this).find("#type").change(function() {
                form_control_changed_type($(corr)); });

            $(this).find("#rij_soort").change(function() {
                form_control_changed_rij($(corr)); });

            $(this).find("#kolom_soort").change(function() {
                form_control_changed_kol($(corr)); });

            // button: click event
            $(this).find("#reset").click(function() {
                form_control_reset_row($(corr)); });
       });
    }
};


function knop_werkt_niet() {

    alert("Deze knop werkt nog niet.");
};

function formulier_bulkcorrecties_leegmaken() {

    let form_bulk = $("#Form_bulkcorrecties");
    if (form_bulk.length){

        let bulkcorrecties = form_bulk.find("div[id^='bulkcorr_']");

        $.each(bulkcorrecties, function(key, corr) {

            form_control_reset_row($(corr));
        });
    }
};

function form_control_changed_type(corr) {

    alert("Gewijzigd: " + corr.attr("id"));

    let type_selected = corr.find("#type").children("option:selected").val();

    let rij_selected = corr.find("#rij_soort").children("option:selected").val();

    let kol_selected = corr.find("#kolom_soort").children("option:selected").val();

    alert("Geselecteerd: " + type_selected + " ; " + rij_selected + " ; " + kol_selected);

};

function form_control_changed_rij(corr) {

    alert("Rij - Gewijzigd: " + corr.attr("id"));
};


function form_control_changed_kol(corr) {

    alert("Kolom - Gewijzigd: " + corr.attr("id"));
};


function form_control_reset_row(corr) {
    // code voor de reset knop per correctieregel

    // alert("Regel: " + corr.attr("id"));

    // reset selectie van type
    let x = corr.find("#type").closest("select");
    x.val(x.data("default-value"));

    // reset selectie van rij_soort
    x = corr.find("#rij_soort").closest("select");
    x.val(x.data("default-value"));

    // reset selectie van rij_code
    x = corr.find("#rij_code").closest("select");
    x.val(x.data("default-value"));

    // reset selectie van kolom_soort
    x = corr.find("#kolom_soort").closest("select");
    x.val(x.data("default-value"));

    // reset selectie van kolom_code
    x = corr.find("#kolom_code").closest("select");
    x.val(x.data("default-value"));

    // reset bedrag
    x = corr.find("#bedrag");
    x.val("0");

    // reset opmerking
    x = corr.find("#opmerking");
    x.val("Bulkcorrectie Ocido");

    // reset check (hidden)
    x = corr.find("#check");
    x.val(false);
};
