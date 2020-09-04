from functools import reduce

from applicatie.logic.codelijst import Codelijst
from applicatie.logic.maak_matrix import pivot_table


class DraaiTabel:
    def __init__(self, naam: str, data, rij_naam: str, kolom_naam: str,
                 rij_codelijst: Codelijst, kolom_codelijst: Codelijst, waarde_naam='bedrag', waarde_type=float,
                 grijze_cellen=[], alles_weergeven=False, is_bewerkbaar=False, detail_weergave=True):
        self.naam = naam
        self.waarde_naam = waarde_naam
        self.is_bewerkbaar = is_bewerkbaar
        self.detail_weergave = detail_weergave
        self.grijze_cellen = grijze_cellen

        indices, self.tabel = pivot_table(data, aggregeer_kolommen=[rij_naam, kolom_naam],
                                          waarde_kolom=self.waarde_naam, waarde_type=waarde_type)

        if alles_weergeven:
            self.rijen = rij_codelijst.geef_terminals()
            self.kolommen = kolom_codelijst.geef_terminals()
        else:
            self.rijen, self.kolommen = indices

        self.rij_naam, self.kolom_naam = rij_naam, kolom_naam

        # Haal velden die met een underscore weg, die hebben een speciale betekenis
        self.rijen = sorted(self.rijen)
        self.kolommen = sorted([kolom for kolom in self.kolommen if not kolom.startswith('_')])
        self.data = data

        # Onthoud omschrijvingen
        self._rij_codelijst = rij_codelijst
        self._kolom_codelijst = kolom_codelijst

    def __getitem__(self, args):
        """Geef een specifieke waarde uit de draaitabel terug."""
        return self.tabel[args]

    def geef_rij_keuzes(self):
        """Geef keuzemogelijkheden voor rij bij een mutatie."""
        return self._rij_codelijst.geef_terminals()

    def geef_kolom_keuzes(self):
        """Geef keuzemogelijkheden voor kolom bij een mutatie."""
        return self._kolom_codelijst.geef_terminals()

    def geef_rij_omschrijving(self, code):
        """Geef een omschrijving bij een rij-code."""
        return self._rij_codelijst.geef_omschrijving(code)

    def geef_kolom_omschrijving(self, code):
        """Geef een omschrijving bij een kolom-code."""
        return self._kolom_codelijst.geef_omschrijving(code)

    def geef_detail_kolommen(self):
        unieke_labels = reduce(set.union, [rij.keys() for rij in self.data], set())
        rsub = 'sub_' + self.rij_naam
        ksub = 'sub_' + self.kolom_naam
        relevante_labels = unieke_labels - {self.rij_naam, self.kolom_naam, rsub, ksub, self.waarde_naam}

        det = 'details'
        labels = list()
        if det in relevante_labels:
            # details komt voor: details verwijderen en labels uit details toevoegen
            relevante_labels = relevante_labels - {det}
            for element in self.data:
                rij = dict(element)
                keys = [key for key in dict(rij[det]).keys()] if det in rij.keys() else []
                labels.append(keys)
        labels_uit_details = reduce(set.union, labels, set())

        oms = 'omschrijving'
        omschrijving = list()
        if oms in labels_uit_details:
            # omschrijving halen we eruit omdat we die aan het eind willen plaatsen
            labels_uit_details = labels_uit_details - {oms}
            omschrijving = [oms]

        relevante_labels.update(labels_uit_details)

        # Verwijder eventuele verborgen labels (deze beginnen met _ )
        relevante_labels = [label for label in relevante_labels if not label.startswith('_')]

        # Sort labels alphabetically but always put value last
        # TODO Waarom dit onderscheid?
        if ksub in unieke_labels:
            details = ([self.rij_naam] + [self.kolom_naam] + [rsub] + [ksub]
                       + sorted(relevante_labels, key=str.lower) + omschrijving + [self.waarde_naam])
        else:
            details = ([self.rij_naam] + [self.kolom_naam] + [rsub]
                       + sorted(relevante_labels, key=str.lower) + omschrijving + [self.waarde_naam])

        return details

    def is_grijze_cel(self, element):
        # If this is a grijze cel return true
        # if self.grijze_cellen:
        #     for categorie in self.grijze_cellen:
        #         for taakveld in self.grijze_cellen:
        #             # print(taakveld)


        return False
