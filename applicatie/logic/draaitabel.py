from functools import reduce
from typing import Iterable, Tuple

from applicatie.logic.maak_matrix import pivot_table

WAARDE_KOLOM = 'bedrag'


class DraaiTabel:
   def __init__(self, data, rij_naam, kolom_naam):
       indices, self.tabel = pivot_table(data, aggregeer_kolommen=[rij_naam, kolom_naam],
                                         waarde_kolom=WAARDE_KOLOM)
       self.rij_naam, self.kolom_naam = rij_naam, kolom_naam
       self.rijen, self.kolommen = indices

       self.rijen = sorted(self.rijen)
       self.kolommen = sorted(self.kolommen)
       self.data = data

   def __getitem__(self, args):
       """Geef een specifieke waarde uit de draaitabel terug."""
       return self.tabel[args]

   def geef_detail_kolommen(self):
       unieke_labels = reduce(set.union, [rij.keys() for rij in self.data], set())
       relevante_labels = unieke_labels - {self.rij_naam, self.kolom_naam, WAARDE_KOLOM}

       # Sort labels alphabetically but always put value last
       return sorted(relevante_labels, key=str.lower) + [WAARDE_KOLOM]
