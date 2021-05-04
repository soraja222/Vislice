STEVILO_DOVOLJENIH_NAPAK = 10
PRAVILNA_CRKA, PONOVLJENA_CRKA, NAPACNA_CRKA = '+', 'o', '-'
ZMAGA, PORAZ = 'w', 'x'

class Igra:

    def __init__(self, geslo, crke=[]):
        self.geslo = geslo
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

    def zamaga(self):
        return not self.poraz() and len(set(self.pravilne_crke())) == len(set(self.geslo)) #set smo dodal, da se črke nikjer niso ponavljale

    def pravilni_del_gesla(self):
        pravilni = ''
        for crka in self.geslo.upper(): #uganjene črke bomo napisal v velikih črkah
            if crka in self.crke:
                pravilni += crka
            else:
                pravilni += '_'
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
            

with open('besede.txt', encoding="utf-8") as f:
    bazen_besed = f.read().split() #.split() deli po praznih znakih(white space), pri nas je to presledek, .read() pa da v niz celo datoteko

import random

def nova_igra():
    geslo = random.choice(bazen_besed)
    return Igra(geslo)