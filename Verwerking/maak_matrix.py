# import things
from flask_table import Table, Col
from Verwerking.inlezen import verwerken


# Get some objects
#data = {'date':[u'2012-06-28', u'2012-06-29', u'2012-06-30'], 'users': [405, 368, 119]}

header = {'kolkop':['1.0', '3.1','6.1','7.0']}

data = {'regels':[['tv 1.0','','12','','123'],
        ['tv 1.1','3','2','1','0'],
        ['tv 2.0','','43','',''],
        ['tv 6.6','4','','','13']]
        }


# data = {
#     'category1': {
#         'titles': ['t1', 't2', 't3'],
#         'dates': ['d1', 'd2', 'd3']
#     },
#     'category2': {
#         'titles': ['t4', 't5', 't6'],
#         'dates': ['d4', 'd5', 'd6']
#     }
# }

# newdata = zip(
#     zip(*(x['titles'] for x in data.values())),
#     zip(*(x['dates'] for x in data.values())))
