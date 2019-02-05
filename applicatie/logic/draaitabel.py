from applicatie.logic.maak_matrix import pivot_table


class DraaiTabel:
   def __init__(self, data):
       self._data = data
       indices, self.tabel = pivot_table(data, aggregeer_kolommen=['taakveld', 'categorie'],
                                         waarde_kolom='bedrag')
       self.rijen, self.kolommen = indices

   def __getitem__(self, args):
       print("args = {!r}".format(args))
       return self.tabel[args]

