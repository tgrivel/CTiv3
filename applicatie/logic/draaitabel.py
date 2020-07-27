from functools import reduce

from applicatie.logic.codelijst import Codelijst
from applicatie.logic.maak_matrix import pivot_table

WAARDE_KOLOM = 'bedrag'


class DraaiTabel:
    waarde_naam = WAARDE_KOLOM

    def __init__(self, naam: str, data, rij_naam: str, kolom_naam: str,
                 rij_codelijst: Codelijst, kolom_codelijst: Codelijst):
        self.naam = naam
        indices, self.tabel = pivot_table(data, aggregeer_kolommen=[rij_naam, kolom_naam],
                                          waarde_kolom=self.waarde_naam)
        self.rij_naam, self.kolom_naam = rij_naam, kolom_naam
        self.rijen, self.kolommen = indices

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
         relevante_labels = unieke_labels - {self.rij_naam, self.kolom_naam, rsub, ksub, WAARDE_KOLOM}

         # Verwijder verborgen labels
         relevante_labels = [label for label in relevante_labels if not label.startswith('_')]

         # Sort labels alphabetically but always put value last
         # TODO Waarom dit onderscheid?
         if ksub in unieke_labels:
             details = ([self.rij_naam] + [self.kolom_naam] + [rsub] + [ksub]
                        + sorted(relevante_labels, key=str.lower) + [WAARDE_KOLOM])
         else:
             details = ([self.rij_naam] + [self.kolom_naam] + [rsub]
                        + sorted(relevante_labels, key=str.lower) + [WAARDE_KOLOM])

         return details
