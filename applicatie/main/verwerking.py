from applicatie.logic.codelijst import Codelijst
from applicatie.logic.controles import controle_met_defbestand
from applicatie.logic.draaitabel import DraaiTabel
from applicatie.logic.inlezen import ophalen_en_controleren_databestand, ophalen_bestand_van_web
from config.configurations import IV3_REPO_PATH, IV3_DEF_FILE, EXTERNE_CONTROLE


class Verwerking(object):
    def __init__(self, jsonbestand):
        # Initialiseren
        self.fouten = []
        self._codelijsten = {}
        self._grijze_cellen = {}

        # Draaitabellen
        self.draaitabellen = {}

        # Anders
        self.controle_resultaten = None
        self.metadata = None
        self.contact = None
        self.definitie_bestand = None
        self.sjabloon_meta = None

        # json data bestand ophalen en evt. fouten teruggeven
        if jsonbestand:
            self.data_bestand, self.fouten = ophalen_en_controleren_databestand(jsonbestand)
        else:
            self.data_bestand = None
            self.fouten.append("Geen json-bestand")

    def run(self, jsonbestand):
        """ Haal het JSON-bestand op en geef evt. foutmeldingen terug
        Indien geen fouten, laad de pagina met een overzicht van de data.
        """

        if not self.fouten:
            self.metadata = self.data_bestand['metadata']
            self.contact = self.data_bestand['contact']
            self._ophalen_definitiebestand()

        if not self.fouten:
            # Controle databestand met definitiebestand
            if EXTERNE_CONTROLE:
                print("regel 45 inside EXTERNE_DEF_BESTAND_CONTROLE if van verwerking.run()")
                self.fouten = OSF_connectie.geef_fouten(self, json_bestand, api_url)
            else:
                self.fouten = controle_met_defbestand(self.data_bestand, self.definitie_bestand)

        # TODO Aggregeren via externe API

        if not self.fouten:
            self.controle_resultaten = []

            # Zoek omschrijvingen bij de codes zodat we deze in de tabel kunnen tonen
            for naam, codelijst in self.definitie_bestand['codelijsten'].items():
                self._codelijsten[naam] = Codelijst(codelijst['codelijst'])

            # Zoek grijze cellen gedefinieerd in het definitiebestand.
            self._grijze_cellen['lasten'] = {}
            self._grijze_cellen['balans_lasten'] = {}
            self._grijze_cellen['baten'] = {}
            self._grijze_cellen['balans_baten'] = {}
            self._grijze_cellen['kengetallen'] = {}
            self._grijze_cellen['beleidsindicatoren'] = {}
            for naam, grijze_cellen in self.definitie_bestand['grijze_cellen'].items():
                self._grijze_cellen[naam] = grijze_cellen

            self._maken_draaitabellen(self._codelijsten, self._grijze_cellen, self.data_bestand['data'])

    def muteer(self, waarde_kant, mutatie):
        """Verwerk mutatie."""
        self.data_bestand['data'][waarde_kant].append(mutatie)

    def _ophalen_definitiebestand(self):
        # json definitie bestand ophalen van web
        # in de controles bij het inlezen is al bepaald dat dit bestaat
        overheidslaag = self.metadata['overheidslaag']
        boekjaar = self.metadata['boekjaar']
        bestandsnaam = IV3_DEF_FILE.format(overheidslaag, boekjaar)
        self.definitie_bestand, self.fouten = ophalen_bestand_van_web(IV3_REPO_PATH, bestandsnaam, 'definitiebestand')
        self.sjabloon_meta = self.definitie_bestand['metadata']

    def _maken_draaitabellen(self, codelijsten, grijze_cellen, data):
        """Maak alle draaitabellen."""

        self.draaitabellen['lasten'] = DraaiTabel(
            naam='lasten',
            data=data['lasten'],
            rij_naam='taakveld',
            kolom_naam='categorie',
            rij_codelijst=codelijsten['taakveld'],
            kolom_codelijst=codelijsten['categorie_lasten'],
            grijze_cellen=grijze_cellen['lasten'])

        self.draaitabellen['balans_lasten'] = DraaiTabel(
            naam='balans_lasten',
            data=data['balans_lasten'],
            rij_naam='balanscode',
            kolom_naam='categorie',
            rij_codelijst=codelijsten['balanscode'],
            kolom_codelijst=codelijsten['categorie_lasten'],
            grijze_cellen=grijze_cellen['balans_lasten'])

        self.draaitabellen['baten'] = DraaiTabel(
            naam='baten',
            data=data['baten'],
            rij_naam='taakveld',
            kolom_naam='categorie',
            rij_codelijst=codelijsten['taakveld'],
            kolom_codelijst=codelijsten['categorie_baten'],
            grijze_cellen=grijze_cellen['baten'])

        self.draaitabellen['balans_baten'] = DraaiTabel(
            naam='balans_baten',
            data=data['balans_baten'],
            rij_naam='balanscode',
            kolom_naam='categorie',
            rij_codelijst=codelijsten['balanscode'],
            kolom_codelijst=codelijsten['categorie_baten'],
            grijze_cellen=grijze_cellen['balans_baten'])

        self.draaitabellen['balans_standen'] = DraaiTabel(
            naam='balans_standen',
            data=data['balans_standen'],
            rij_naam='balanscode',
            kolom_naam='standper',
            rij_codelijst=codelijsten['balanscode'],
            kolom_codelijst=codelijsten['standper'])

        self.draaitabellen['kengetallen'] = DraaiTabel(
            naam='kengetallen',
            data=data.get('kengetallen', []),
            rij_naam='kengetal',
            kolom_naam='verslagperiode',
            rij_codelijst=codelijsten['kengetallen'],
            kolom_codelijst=codelijsten['verslagperiode'],
            waarde_naam='waarde',
            waarde_type='str',
            alles_weergeven=True,
            is_bewerkbaar=True,
            detail_weergave=False,
            grijze_cellen=grijze_cellen['kengetallen'])

        self.draaitabellen['beleidsindicatoren'] = DraaiTabel(
            naam='beleidsindicatoren',
            data=data.get('beleidsindicatoren', []),
            rij_naam='beleidsindicator',
            kolom_naam='verslagperiode',
            rij_codelijst=codelijsten['beleidsindicatoren'],
            kolom_codelijst=codelijsten['verslagperiode'],
            waarde_naam='waarde',
            waarde_type='str',
            alles_weergeven=True,
            is_bewerkbaar=True,
            detail_weergave=False,
            grijze_cellen=grijze_cellen['beleidsindicatoren'])
