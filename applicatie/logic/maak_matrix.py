


def pivot_table(data, aggregeer_kolommen, waarde_kolom):
    """Aggregeer kolom value_col over args.

    @param aggregeer_kolommen De kolommen waarover geaggregeerd moet worden
    @param waarde_kolom De kolom waarvan de waarde moet worden opgeslagen
    """

    index = [set() for _ in aggregeer_kolommen]
    table = {}

    for row in data:
        key = tuple(row[kolom] for kolom in aggregeer_kolommen)

        # Update indices
        for i, k in enumerate(key):
            index[i].add(k)

        # Update tabel
        table[key] = table.get(key, 0) + row[waarde_kolom]

    return index, table
