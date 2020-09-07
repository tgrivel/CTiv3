
const FORMULIER_BULK = "Form_bulkcorrecties";

function initialiseer_form_controls_bulkcorrecties() {

    let form_bulk = $("#" + FORMULIER_BULK);

    if (!form_bulk.length){

        alert("Formulier " + FORMULIER_BULK + " niet gevonden.");

    } else {

        let bulkcorrecties = form_bulk.find("div[id^='bulkcorr_']");

        $.each(bulkcorrecties, function(key, corr) {

            // change() event toevoegen aan form control 'Type'
            // zie https://api.jquery.com/change/
            $(this).find("#type").change(function() {
                form_control_type_gewijzigd($(corr)); });

            // click() event toevoegen aan button 'Reset'
            // zie https://api.jquery.com/click/
            $(this).find("#reset").click(function() {
                form_control_reset_rij($(corr)); });
       });
    }
};


function bulkcorrecties_verwerken() {

    let tekst = "Weet u zeker dat u de ingevoerde correcties wilt verwerken?\r\n"
    tekst = tekst + "Zo ja,  klik op OK\r\n"
    tekst = tekst + "Zo nee, klik op Annuleren (Cancel)"

    if (confirm(tekst)) {
        console.log('Debug status: ' + DEBUG_STATUS);
    }
};


function formulier_bulkcorrecties_leegmaken() {

    let form_bulk = $("#" + FORMULIER_BULK);

    if (form_bulk.length){

        let bulkcorrecties = form_bulk.find("div[id^='bulkcorr_']");

        $.each(bulkcorrecties, function(key, corr) {
            // reset de correctieregel
            form_control_reset_rij($(corr));
        });
    }
};


function form_control_type_gewijzigd(corr) {
    /* form_control Type is gewijzigd
       overige form-controls updaten */

    if (DEBUG_STATUS){
        console.log("Gewijzigde correctieregel: " + corr.attr("id"));
    }

    // geselecteerde waarde voor type
    let type_geselecteerd = corr.find("#type").children("option:selected").val();

    // update selectie opties voor form_controls van een correctieregel
    form_control_update_opties($(corr), "rij_soort", type_geselecteerd, true);
    form_control_update_opties($(corr), "rij_code", type_geselecteerd, false);
    form_control_update_opties($(corr), "kolom_soort", type_geselecteerd, true);
    form_control_update_opties($(corr), "kolom_code", type_geselecteerd, false);

};


function form_control_update_opties(corr, kolom, type_geselecteerd, select) {
    /* update de selectie opties voor een form control */

    let form_bulk = $("#" + FORMULIER_BULK);

    let arr_opties;
    arr_opties = [];

    if (type_geselecteerd != "") {
        // haal string met opties op
        let str_opties = form_bulk.find("#" + kolom + "_opties").val().replace(/'/g, '"');
        // omzetten naar een array met opties
        arr_opties = $.parseJSON(str_opties)[type_geselecteerd];
    }

    // selecteer de form control
    let form_control = corr.find("#" + kolom);

    // oude selectie opties verwijderen
    form_control.find("option").each(function() {
        if (this.value){
            $(this).remove();
        } else {
            $(this).prop('selected', 'selected');
        }
    });

    // nieuwe opties toevoegen uit array
    let form_control_select = form_control.closest("select");
    for (i = 0; i < arr_opties.length; i++) {
        let opt = arr_opties[i];
        let el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        // eerste element van de array selecteren
        if (select && i == 0) {
            el.setAttribute("selected", "selected");
        }
        form_control_select.append(el);
    }

    if (DEBUG_STATUS){
        let selected = form_control.children("option:selected").val();
        console.log("Geselecteerde optie: " + selected);
    }

};


function form_control_reset_rij(corr) {
    /* reset een correctieregel */

    // verwijder selectie opties voor de form_controls
    form_control_update_opties($(corr), "rij_soort", "", false);
    form_control_update_opties($(corr), "rij_code", "", false);
    form_control_update_opties($(corr), "kolom_soort", "", false);
    form_control_update_opties($(corr), "kolom_code", "", false);

    // reset alle kolommen naar default waardes
    arr = ["type", "rij_soort", "rij_code", "kolom_soort", "kolom_code"]
    for (i = 0; i < arr.length; i++) {
        let foo = corr.find("#" + arr[i]).closest("select");
        foo.val(foo.data("default-value"));
    }

    let foo;

    foo = corr.find("#bedrag");
    foo.val("0");

    foo = corr.find("#opmerking");
    foo.val("Bulkcorrectie Ocido");

    foo = corr.find("#check");
    foo.val(false);
};
