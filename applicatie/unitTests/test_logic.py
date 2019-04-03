from unittest import TestCase


class MaakMatrix(TestCase):

    _KOLOMMEN = ['Land', 'Bedrijf', 'Jaar', 'Omzet']

    _PRE_DATA = [['Denemarken', 'Q8', 2018, 776790.9255494669],
                 ['Nederland', 'Q8', 2015, 768910.9557386474],
                 ['Denemarken', 'BP', 2015, 379117.29816911824],
                 ['Nederland', 'Esso', 2016, 32934.924861288906],
                 ['Duitsland', 'Esso', 2017, 860230.5873922401],
                 ['Duitsland', 'Esso', 2016, 617863.5309096542],
                 ['Denemarken', 'Shell', 2018, 644011.7355527324],
                 ['Denemarken', 'Shell', 2017, 328534.24034264236],
                 ['Denemarken', 'BP', 2015, 651831.8261813337],
                 ['Nederland', 'Q8', 2017, 490090.3426783866],
                 ['Duitsland', 'Esso', 2015, 258218.14179539605],
                 ['Duitsland', 'Shell', 2016, 413170.38352001924],
                 ['Denemarken', 'BP', 2018, 435816.76818360627],
                 ['Duitsland', 'Shell', 2015, 795357.6380468213],
                 ['Nederland', 'Esso', 2018, 908931.8633676557],
                 ['Duitsland', 'Q8', 2015, 662335.0578824308],
                 ['Duitsland', 'Shell', 2017, 868656.4880121602],
                 ['Duitsland', 'Esso', 2017, 131550.96737900862],
                 ['Denemarken', 'Esso', 2017, 467549.0322160846],
                 ['Duitsland', 'Q8', 2015, 619703.1685107129],
                 ['Duitsland', 'Esso', 2015, 434254.04782141553],
                 ['Nederland', 'Q8', 2017, 98799.89988018801],
                 ['Denemarken', 'Esso', 2018, 469282.0119387381],
                 ['Duitsland', 'BP', 2017, 484080.55867874366],
                 ['Nederland', 'BP', 2015, 927046.0526701929],
                 ['Nederland', 'Q8', 2017, 689992.6179071222],
                 ['Duitsland', 'BP', 2018, 759542.0892718703],
                 ['Denemarken', 'Q8', 2015, 36549.40439668042],
                 ['Nederland', 'Shell', 2015, 268477.66687856213],
                 ['Nederland', 'BP', 2015, 403872.66536009137],
                 ['Duitsland', 'Esso', 2017, 716673.3082165094],
                 ['Duitsland', 'BP', 2018, 886116.3596413484],
                 ['Nederland', 'Shell', 2016, 182475.5611290688],
                 ['Duitsland', 'Q8', 2017, 371412.72892899],
                 ['Nederland', 'Esso', 2016, 99772.74615732534],
                 ['Denemarken', 'BP', 2018, 673946.4978682523],
                 ['Denemarken', 'Shell', 2018, 954144.5681983181],
                 ['Denemarken', 'Q8', 2018, 789939.6295789226],
                 ['Duitsland', 'BP', 2015, 460271.70101547596],
                 ['Nederland', 'Esso', 2017, 665947.1387589467],
                 ['Denemarken', 'BP', 2016, 282625.3778096207],
                 ['Nederland', 'BP', 2018, 737259.3290336671],
                 ['Denemarken', 'Shell', 2016, 58240.815426989226],
                 ['Denemarken', 'Q8', 2018, 166104.31977948782],
                 ['Duitsland', 'BP', 2017, 784998.7496879863],
                 ['Denemarken', 'Q8', 2017, 368202.7185702247],
                 ['Duitsland', 'BP', 2018, 1549.6422996220672],
                 ['Nederland', 'Esso', 2015, 283334.8541963584],
                 ['Nederland', 'Esso', 2018, 101697.92576460501],
                 ['Duitsland', 'BP', 2017, 331529.7793876557],
                 ['Nederland', 'Q8', 2015, 42330.43117143809],
                 ['Duitsland', 'Esso', 2015, 290175.45204931684],
                 ['Duitsland', 'Q8', 2017, 671428.8796454167],
                 ['Denemarken', 'Q8', 2016, 212650.1703679793],
                 ['Duitsland', 'Esso', 2015, 619284.6044688036],
                 ['Denemarken', 'BP', 2015, 566161.5494625472],
                 ['Duitsland', 'Esso', 2016, 5893.455981561769],
                 ['Nederland', 'Q8', 2015, 135182.41871728664],
                 ['Nederland', 'Shell', 2017, 958847.0372519607],
                 ['Denemarken', 'Esso', 2015, 763453.8659732142],
                 ['Duitsland', 'Q8', 2018, 413339.44467571046],
                 ['Nederland', 'Shell', 2017, 744263.8094484147],
                 ['Nederland', 'Shell', 2016, 545387.6338108644],
                 ['Nederland', 'Q8', 2018, 779904.2830532115],
                 ['Nederland', 'Esso', 2015, 903873.3130502425],
                 ['Denemarken', 'BP', 2018, 73059.71753161578],
                 ['Nederland', 'Shell', 2017, 581162.7838720737],
                 ['Nederland', 'Esso', 2016, 678374.9610337258],
                 ['Denemarken', 'Q8', 2016, 989103.6822720476],
                 ['Nederland', 'Esso', 2015, 165998.4873845196],
                 ['Duitsland', 'Esso', 2017, 229220.18827880576],
                 ['Duitsland', 'Q8', 2017, 292167.9046049814],
                 ['Denemarken', 'Q8', 2015, 397063.92575578886],
                 ['Nederland', 'Esso', 2016, 523131.9765461942],
                 ['Denemarken', 'BP', 2015, 843990.781721409],
                 ['Duitsland', 'Q8', 2017, 668981.6025185145],
                 ['Duitsland', 'BP', 2016, 450172.3970786814],
                 ['Nederland', 'BP', 2018, 642163.9306334845],
                 ['Nederland', 'Esso', 2017, 726736.508805806],
                 ['Nederland', 'BP', 2016, 29728.413625634275]]

    def testPivotTable_01(self):
        from applicatie.logic.maak_matrix import pivot_table


        data                = [dict(zip(self._KOLOMMEN, rij)) for rij in self._PRE_DATA]
        aggregeer_kolommen  = ['Land']
        waarde_kolom        = 'Omzet'

        _, result           = pivot_table(data, aggregeer_kolommen, waarde_kolom)

        exp_result          = {('Denemarken',): 11328170.862846822,
                               ('Duitsland',): 14098178.857699854,
                               ('Nederland',): 14116630.532786965}


        self.assertDictEqual(result, exp_result)
