import json
from collections import OrderedDict
#from Verwerking.maak_matrix import ItemTable
from flask_table import Table, Col

# Declare your table
class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')


class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description


def ophalen_file(bestand):
    print (bestand.filename)
    newfile = bestand.read()
    try:
        data = json.loads(newfile.decode('utf-8'), object_pairs_hook=OrderedDict)
        print('verwerken als utf8')
    except:
        data = json.loads(newfile.decode('cp1251'), object_pairs_hook=OrderedDict)
        print('verwerken als cp1251')
    verwerken(data)

    items = [Item('Name1', 'Description1'),
             Item('Name2', 'Description2'),
             Item('Name3', 'Description3')]
    table = ItemTable(items)
    print (table.__html__())

    # newfiel = bestand.read()
    # data = json.load(newfiel, object_pairs_hook=OrderedDict)
    # verwerken(data)

    #
    # with open(newfiel) as bron:
    #     data = json.load(bron, object_pairs_hook=OrderedDict)
    #     verwerken(data)

def verwerken(data):
    aantal = 0
    for row in data:
        aantal += 1
    print('totaal ' + str(aantal) + ' ingelezen')

