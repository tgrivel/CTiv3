from functools import reduce
from typing import Iterable, Tuple

from applicatie.logic.maak_matrix import pivot_table

WAARDE_KOLOM = 'bedrag'


class DraaiTabel:
   def __init__(self, data, rij_naam, kolom_naam, rij_omschrijvingen, kolom_omschrijvingen):
       indices, self.tabel = pivot_table(data, aggregeer_kolommen=[rij_naam, kolom_naam],
                                         waarde_kolom=WAARDE_KOLOM)
       self.rij_naam, self.kolom_naam = rij_naam, kolom_naam
       self.rijen, self.kolommen = indices

       self.rijen = sorted(self.rijen)
       self.kolommen = sorted(self.kolommen)
       self.data = data

       # Onthoud omschrijvingen
       self.rij_omschrijvingen = rij_omschrijvingen
       self.kolom_omschrijvingen = kolom_omschrijvingen

   def __getitem__(self, args):
       """Geef een specifieke waarde uit de draaitabel terug."""
       return self.tabel[args]

   def geef_detail_kolommen(self):
        unieke_labels = reduce(set.union, [rij.keys() for rij in self.data], set())
        rsub = 'sub_' + self.rij_naam
        ksub = 'sub_' + self.kolom_naam
        relevante_labels = unieke_labels - {self.rij_naam, self.kolom_naam, rsub, ksub, WAARDE_KOLOM}

        # Sort labels alphabetically but always put value last
        # TODO Waarom dit onderscheid?
        if ksub in unieke_labels:
            details = ([self.rij_naam] + [self.kolom_naam] + [rsub] + [ksub]
                       + sorted(relevante_labels, key=str.lower) + [WAARDE_KOLOM])
        else:
            details = ([self.rij_naam] + [self.kolom_naam] + [rsub]
                       + sorted(relevante_labels, key=str.lower) + [WAARDE_KOLOM])

        return details
