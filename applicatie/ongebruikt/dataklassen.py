# nog niet bekend of deze nodig zijn

class GrijzeCellen(object):
    def __init__(self, rek_kant,taakv,cat):
        self.rek_kant = rek_kant
        self.taakv = taakv
        self.cat = cat

class DataLastenBaten(object):
    def __init__(self,taakv,cat,bedr,extra_data: dict):
        self.taakv = taakv
        self.cat = cat
        self.bedr = bedr
        self.extra_data = extra_data  # type: dict

class DataBalans(object):
    def __init__(self,balanscode,stand,bedr):
        self.balanscode = balanscode
        self.stand = stand
        self.bedr = bedr

class iv3codesCategorien(object):
    def __init__(self,cat_kant,cat_code,cat_omschr):
        self.cat_kant = cat_kant
        self.cat_code = cat_code
        self.cat_omschr = cat_omschr

class iv3beleidsterreinen(object):
    def __init__(self,belter_codes,belter_omschr,belter_children: list):
        self.belter_codes = belter_codes
        self.belter_omschr = belter_omschr
        self.belter_children = belter_children # type: list

class iv3balanscodes(object):
    def __init__(self,bal_code,bal_omschr,bal_children:list):
        self.bal_code = bal_code
        self.bal_omschr = bal_omschr
        self.bal_children = bal_children # type: list

# hieronder staan enkele probeersels.
# indien deze gebruikt gaan worden, graag verplaatsen naar boven deze opmerking



class LayoutLastenBaten(object):
    def __init__(self,rijnr, rij,rijniv,kolnr, kol,kolniv,bedr):
        self.rijnr = rijnr          # tbv volgorde in scherm, rijnummering
        self.rij = rij              # taakvelden en balansposten
        self.rijniv = rijniv        # diepte, subtotalen en totalen
        self.kolnr = kolnr          # kolomnummer
        self.kol = kol              # categorien
        self.kolniv = kolniv        # diepte


class DataLastenBaten(object):
    def __init__(self,code_combi,bedr):
        self.code_combi = code_combi
        self.bedr = bedr


class TotalenLastenBaten(object):
    def __init__(self,code_combi,bedr):
        self.code_combi = code_combi
        self.bedr = bedr


class PaginaDefinities(object):
    def __init__(self,rekeningkant, kolomgroep, rijgroep):
        self.rekeningkant = rekeningkant
        self.kolomgroep = kolomgroep
        self.rijgroep = rijgroep