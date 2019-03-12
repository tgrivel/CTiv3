from applicatie.logic.maak_matrix import pivot_table


class DraaiTabel:
   def __init__(self, data, aggregeer_kolommen):
       self._data = data
       self.aggregeer_kolommen = aggregeer_kolommen
       indices, self.tabel = pivot_table(data, aggregeer_kolommen=aggregeer_kolommen,
                                         waarde_kolom='bedrag')
       self.rijen, self.kolommen = indices

   def __getitem__(self, args):
       """Geef een specifieke waarde uit de draaitabel terug."""
       return self.tabel[args]

