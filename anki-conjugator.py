import os
from selenium.webdriver import Firefox
import time
import pandas as pd

def write_csv(card_backside, card_frontside, translations):
    d = {'front': card_frontside, 'back': card_backside, 'translation': translations}
    df = pd.DataFrame(data=d)

    doc = open('verbs_csv', 'w')
    doc.write(df.to_csv(header=False, index=False))
    doc.close()

inicio = time.time()

# Create display variable
os.environ["DISPLAY"] = ":0"

driver = Firefox()
driver.get("https://conjugacao.reverso.net/conjugacao-frances.html")

# List of desired words
words = ['être', 'avoir', 'entendre', 'sentir', 'voir', 'marcher', 'écouter', 'chanter', 'montrer', 'parler', \
    'regarder', 'voler', 'fermer', 'ouvrir', 'sortir', 'entrer', 'briller', 'donner', 'finir', 'faire', 'commencer', \
        'tomber', 'jouer', 'blanchir', 'fleurir', 'grandir', 'grossir', 'jaunir', 'rougir', 'coûter', 'mesurer', 'peser', \
            'représenter', 'attendre', 'habiter', 'monter', 'sonner', 'dire', 'épouser', 'mettre', 'prendre', 'visiter', \
                'aller', 'venir', 'apporter', 'ajouter', 'arriver', 'coucher', 'passer', 'remercier', 'boire', 'servir', \
                    'déjeuner', 'manger', 'préparer']

print('Pesquisando ' + str(len(words)) + ' verbos\n')

# Lists to save the verbs
card_frontside = []
card_backside = []
translations = []
back = ''

# Loop through desired words
for word in words:

    tic = time.time()

    # Search the word
    search_box = driver.find_element_by_name('ctl00$txtVerb')
    search_box.send_keys(word)

    conjugate = driver.find_element_by_id('lbConjugate')
    conjugate.click()

    # Scrap le présent, le futur and le passé composé
    present = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[1]/div[2]/div').text.split()
    futur = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[1]/div[4]/div').text.split()
    passe_compose = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[3]/div[2]/div').text.split()

    # Scrap the translation
    translation = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[1]/div/div[3]/p').text

    # Formating le présent
    card_frontside.append(present[0] + ': ' + word) #Setting the front of the card

    if len(present)!=13:
        back = present[1].capitalize() + ', '
        for i in range(2,len(present),2): #Setting the back of the card
            back += present[i].capitalize() + ' ' + present[i+1] + ', '

    else:
        for i in range(1,len(present),2): #Setting the back of the card
            back += present[i].capitalize() + ' ' + present[i+1] + ', '

    card_backside.append(back[0:len(back)-2])
    translations.append(translation.capitalize())
    back = ''

    # Formating le futur
    card_frontside.append(futur[0] + ': ' + word) #Setting the front of the card

    if len(futur)!=13:
        back = futur[1].capitalize() + ', '
        for i in range(2,len(futur),2): #Setting the back of the card
            back += futur[i].capitalize() + ' ' + futur[i+1] + ', '
    else:
        for i in range(1,len(futur),2): #Setting the back of the card
            back += futur[i].capitalize() + ' ' + futur[i+1] + ', '


    card_backside.append(back[0:len(back)-2])
    translations.append(translation.capitalize())
    back = ''

    # Formating le passé composé
    if passe_compose[2]=="j'ai":
        card_frontside.append(passe_compose[0] + ' ' + passe_compose[1] + ' (avec avoir): ' + word)
        back = passe_compose[2].capitalize() + ' ' + passe_compose[3] + ', '
        for i in range(4,19,3): #Setting the back of the card
            back += passe_compose[i].capitalize() + ' ' + passe_compose[i+1] + ' ' + passe_compose[i+2] + ', '
        card_backside.append(back[0:len(back)-2])
        translations.append(translation.capitalize())
        back = ''

    if passe_compose[2]=="je":
        card_frontside.append(passe_compose[0] + ' ' + passe_compose[1] + ' (avec être): ' + word)
        for i in range(2,len(passe_compose),3): #Setting the back of the card
            back += passe_compose[i].capitalize() + ' ' + passe_compose[i+1] + ' ' + passe_compose[i+2] + ', '
        card_backside.append(back[0:len(back)-2])
        translations.append(translation.capitalize())
        back = ''

    if passe_compose[2]=="j'ai" and len(passe_compose)!=19:
        card_frontside.append(passe_compose[0] + ' ' + passe_compose[1] + ' (avec être): ' + word)
        for i in range(19,len(passe_compose),3): #Setting the back of the card
            back += passe_compose[i].capitalize() + ' ' + passe_compose[i+1] + ' ' + passe_compose[i+2] + ', '
        card_backside.append(back[0:len(back)-2])
        translations.append(translation.capitalize())
        back = ''
    
    write_csv(card_backside, card_frontside, translations)
    tac = time.time()
    print(word.capitalize() + ': conjugado! (' + str(tac-tic) + 's)')

driver.quit()

fim = time.time()

print('')
print('Tempo total de execução: ' + str(fim-inicio) + 's')
