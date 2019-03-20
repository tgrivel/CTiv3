from applicatie.logic.maak_matrix import pivot_table


class DraaiTabel:
   def __init__(self, data, rij_naam, kolom_naam):
       self._data = data
       indices, self.tabel = pivot_table(data, aggregeer_kolommen=[rij_naam, kolom_naam],
                                         waarde_kolom='bedrag')
       self.rij_naam, self.kolom_naam = rij_naam, kolom_naam
       self.rijen, self.kolommen = indices

       self.rijen = sorted(self.rijen)
       self.kolommen = sorted(self.kolommen)

   def __getitem__(self, args):
       """Geef een specifieke waarde uit de draaitabel terug."""
       return self.tabel[args]

