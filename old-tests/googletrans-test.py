from googletrans import Translator
import googletrans
import time

translator = Translator(service_urls=['translate.google.com.br'])

words = ['être', 'avoir', 'entendre', 'sentir', 'voir', 'marcher', 'écouter', 'chanter', 'montrer', 'parler', \
    'regarder', 'voler', 'fermer', 'ouvrir', 'sortir', 'entrer', 'briller', 'donner', 'finir', 'faire', 'commencer', \
        'tomber', 'jouer', 'blanchir', 'fleurir', 'grandir', 'grossir', 'jaunir', 'rougir', 'coûter', 'mesurer', 'peser', \
            'représenter', 'attendre', 'habiter', 'monter', 'sonner', 'dire', 'épouser', 'mettre', 'prendre', 'visiter', \
                'aller', 'venir', 'apporter', 'ajouter', 'arriver', 'coucher', 'passer', 'remercier', 'boire', 'servir', \
                    'déjeuner', 'manger', 'préparer']


translator = Translator()


for word in words:
    tic = time.time()
    print(translator.translate(word, src='fr', dest='pt').text)
    tac = time.time()
    print(tac-tic)

#print(googletrans.LANGUAGES)