
const FORMULIER_BULK = "Form_bulkcorrecties";

function initialiseer_form_controls_bulkcorrecties() {

    let form_bulk = $("#" + FORMULIER_BULK);

    if (!form_bulk.length){

        alert("Formulier bulkcorrecties niet gevonden.");

    } else {

        let bulkcorrecties = form_bulk.find("div[id^='bulkcorr_']");

        $.each(bulkcorrecties, function(key, corr) {

            // voeg events toe:
            // change() voor form_controls Type
            // click() voor button Reset

            $(this).find("#type").change(function() {
                form_control_changed_type($(corr)); });

            $(this).find("#reset").click(function() {
                form_control_reset_row($(corr)); });
       });
    }
};


function bulkcorrecties_verwerken() {

    let tekst = "Weet u zeker dat u de ingevoerde correcties wilt verwerken?\r\n"
    tekst = tekst + "Zo ja,  klik op OK\r\n"
    tekst = tekst + "Zo nee, klik op Annuleren (Cancel)"


    if (confirm(tekst)) {
        // Save it!
        console.log('Status: ' + DEBUG_STATUS);
    } else {
        // Do nothing!
    }
};


function formulier_bulkcorrecties_leegmaken() {

    let form_bulk = $("#" + FORMULIER_BULK);

    if (form_bulk.length){

        let bulkcorrecties = form_bulk.find("div[id^='bulkcorr_']");

        $.each(bulkcorrecties, function(key, corr) {
            // reset de correctieregel
            form_control_reset_row($(corr));
        });
    }
};


function form_control_changed_type(corr) {
    /* form_control Type is gewijzigd
       overige form-controls updaten */

    // voor debugging:
    // alert("Gewijzigde correctieregel: " + corr.attr("id"));

    // geselecteerde waarde voor type
    let type_selected = corr.find("#type").children("option:selected").val();

    // update selectie opties voor form_controls
    form_control_update_options($(corr), "rij_soort", type_selected, true);
    form_control_update_options($(corr), "rij_code", type_selected, false);
    form_control_update_options($(corr), "kolom_soort", type_selected, true);
    form_control_update_options($(corr), "kolom_code", type_selected, false);

};

function form_control_update_options(corr, kolom, type_selected, select) {
    /* update of delete de opties voor een form_control */

    let form_bulk = $("#" + FORMULIER_BULK);

    let arr_options;

    arr_options = [];
    if (type_selected != "") {
        // haal string met opties op
        let str_options = form_bulk.find("#" + kolom + "_opties").val().replace(/'/g, '"');
        // omzetten naar array met opties
        arr_options = $.parseJSON(str_options)[type_selected];
    }

    // opties updaten voor form_control
    let form_control = corr.find("#" + kolom);

    // oude opties verwijderen
    form_control.find("option").each(function() {
        if (this.value){
            $(this).remove();
        } else {
            $(this).prop('selected', 'selected');
        }
    });

    // nieuwe opties toevoegen uit array
    form_control_select = form_control.closest("select");
    for (i = 0; i < arr_options.length; i++) {
        let opt = arr_options[i];
        let el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        // eerste element van de array selecteren
        if (select && i == 0) {
            el.setAttribute("selected", "selected");
        }
        form_control_select.append(el);
    }

    // voor debugging:
    // let selected = form_control.children("option:selected").val();
    // console.log("selected option: " + selected);

};


function form_control_reset_row(corr) {
    /* reset de correctieregel */

    // verwijder alle opties voor de form_controls
    form_control_update_options($(corr), "rij_soort", "", false);
    form_control_update_options($(corr), "rij_code", "", false);
    form_control_update_options($(corr), "kolom_soort", "", false);
    form_control_update_options($(corr), "kolom_code", "", false);

    // reset waarde van type
    let x = corr.find("#type").closest("select");
    x.val(x.data("default-value"));

    // reset waarde van rij_soort
    x = corr.find("#rij_soort").closest("select");
    x.val(x.data("default-value"));

    // reset waarde van rij_code
    x = corr.find("#rij_code").closest("select");
    x.val(x.data("default-value"));

    // reset waarde van kolom_soort
    x = corr.find("#kolom_soort").closest("select");
    x.val(x.data("default-value"));

    // reset waarde van kolom_code
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
