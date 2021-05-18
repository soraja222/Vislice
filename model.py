import random
import json

STEVILO_DOVOLJENIH_NAPAK = 9
PRAVILNA_CRKA, PONOVLJENA_CRKA, NAPACNA_CRKA = '+', 'o', '-'
ZMAGA, PORAZ = 'w', 'x'
ZACETEK = 'Z'

DATOTEKA_S_STANJEM = 'stanje.json'
DATOTEKA_Z_BESEDAMI ='besede.txt'
class Igra:

    def __init__(self, geslo, crke=None):
        self.geslo = geslo
        if crke is None:
            self.crke = []
        else:
            self.crke = crke
    
    def napacne_crke(self):
        napacne = []
        for c in self.crke:
            if c.upper() not in self.geslo.upper():
                napacne.append(c)
        return napacne
    
    def pravilne_crke(self):
        pravilne = []
        for c in self.crke:
            if c.upper() in self.geslo.upper():
                pravilne.append(c)
        return pravilne

    def stevilo_napak(self):
        return len(self.napacne_crke())

    def poraz(self):
        return self.stevilo_napak() > STEVILO_DOVOLJENIH_NAPAK

    def zmaga(self):
        return not self.poraz() and len(set(self.pravilne_crke())) == len(set(self.geslo)) #set smo dodal, da se črke nikjer niso ponavljale

    def pravilni_del_gesla(self):
        pravilni = ''
        for crka in self.geslo.upper(): #uganjene črke bomo napisal v velikih črkah
            if crka in self.crke:
                pravilni += crka + ' '
            else:
                pravilni += '_ '
        return pravilni

    def nepravilni_ugibi(self):
        return ' '.join(self.napacne_crke())

    def ugibaj(self, crka):
        crka = crka.upper()
        if crka in self.crke:
            return PONOVLJENA_CRKA
        elif crka in self.geslo.upper():
            self.crke.append(crka)
            if self.zmaga():
                return ZMAGA
            else:
                return PRAVILNA_CRKA
        else:
            self.crke.append(crka)
            if self.poraz():
                return PORAZ
            else:
                return NAPACNA_CRKA
            

with open(DATOTEKA_Z_BESEDAMI, encoding="utf-8") as f:
    bazen_besed = f.read().split() #.split() deli po praznih znakih(white space), pri nas je to presledek, .read() pa da v niz celo datoteko

import random

def nova_igra():
    geslo = random.choice(bazen_besed)
    return Igra(geslo)

class Vislice:

    def __init__(self, datoteka_s_stanjem):
        self.igre = {}
        self.datoteka_s_stanjem = datoteka_s_stanjem

    def prost_id_igre(self):
        if len(self.igre) == 0:
            return 0
        else:
            return max(self.igre.keys()) + 1

    def nova_igra(self):
        self.nalozi_igre_iz_datoteke()
        id_igre = self.prost_id_igre()
        igra = nova_igra()
        self.igre[id_igre] = (igra, ZACETEK)
        self.zapisi_igre_v_datoteko()
        return id_igre

    def ugibaj(self, id_igre, crka):
        self.nalozi_igre_iz_datoteke()
        igra, _ = self.igre[id_igre] # _ predstavlja stanje, ki ga ne rabmo ker ga takoj po ugibu spremenimo, zato namesto stanje napišemo _
        stanje = igra.ugibaj(crka)
        self.igre[id_igre] = (igra, stanje)
        self.zapisi_igre_v_datoteko()

    def nalozi_igre_iz_datoteke(self):
        with open(self.datoteka_s_stanjem, encoding='utf-8') as f:
            igre = json.load(f)
            self.igre = {int(id_igre): (Igra(geslo,crke), stanje) for id_igre, (geslo, crke, stanje) in igre.items()}

    def zapisi_igre_v_datoteko(self):
        with open(self.datoteka_s_stanjem, 'w', encoding='utf-8') as f:
            igre = {id_igre: (igra.geslo, igra.crke, stanje) for id_igre, (igra, stanje) in self.igre.items()}
            json.dump(igre, f)
        