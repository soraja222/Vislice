import bottle
import model

SKRIVNOST = 'moja skrivnost'

vislice = model.Vislice(model.DATOTEKA_S_STANJEM)

@bottle.get('/') # / pomeni korensko mapo na strežniku
def index():
    return bottle.template('index.tpl')

@bottle.post('/nova-igra/')
def nova_igra():
    id_igre = vislice.nova_igra()
    bottle.response.set_cookie('idigre', 'idigre{}'.format(id_igre), path='/', secret=SKRIVNOST) # nastavili smo piškotek, 7 pomeni da mamo pousot dostop do cookija
    bottle.redirect('/igra/')

@bottle.get('/igra/')
def pokazi_igro():
    id_igre = int(bottle.request.get_cookie('idigre', secret=SKRIVNOST).split('e')[1]) #hočmo dobit številko k je pr idigre, zato razdelimo to pr e in uzamemo samo število, to je split in [1] 
    igra, stanje = vislice.igre[id_igre]
    return bottle.template('igra.tpl', igra=igra, stanje=stanje)

@bottle.post('/igra/')
def ugibaj():
    id_igre = int(bottle.request.get_cookie('idigre', secret=SKRIVNOST).split('e')[1])
    crka = bottle.request.forms.getunicode('crka')
    vislice.ugibaj(id_igre, crka)
    bottle.redirect('/igra/')

@bottle.get('/img/<picture>') # v <> smo poimenoval vse slike skp s picture
def serve_pictures(picture):
    return bottle.static_file(picture, root='img')

bottle.run(reloader=True, debug=True)