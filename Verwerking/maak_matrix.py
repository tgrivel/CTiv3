# import things
from flask_table import Table, Col


# Get some objects
data = {
    'category1': {
        'titles': ['t1', 't2', 't3'],
        'dates': ['d1', 'd2', 'd3']
    },
    'category2': {
        'titles': ['t4', 't5', 't6'],
        'dates': ['d4', 'd5', 'd6']
    }
}

newdata = zip(
    zip(*(x['titles'] for x in data.values())),
    zip(*(x['dates'] for x in data.values())))
