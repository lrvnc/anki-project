import os
from selenium.webdriver import Firefox
import time
import pandas as pd
import csv

def write_csv(card_backside, card_frontside, translations, csv_fileName):
    d = {'front': card_frontside, 'back': card_backside, 'translation': translations}
    df = pd.DataFrame(data=d)

    doc = open('anki-cards/' + str(csv_fileName), 'w')
    doc.write(df.to_csv(header=False, index=False))
    doc.close()

csv_file = input('CSV file with desired words: ')
csv_fileName = input('CSV file name output: ')

# Create display variable
os.environ["DISPLAY"] = ":0"

inicio = time.time()

# Create display variable
os.environ["DISPLAY"] = ":0"

driver = Firefox()
driver.get("https://conjugacao.reverso.net/conjugacao-frances.html")

# Lists
with open(csv_file, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

words = []
for i in range(len(data)):
    words.append(str(data[i][0]).capitalize())

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

    # Formating le futur proche
    card_frontside.append('Futur proche: ' + word)
    card_backside.append('Je vais ' + word.lower() + ', Tu vas ' + word.lower() + ', Il/elle va ' + word.lower() + ', Nous allons ' + word.lower() + ', Vous allez ' + word.lower() + ', Ils/elles vont ' + word.lower())
    translations.append(translation.capitalize())

    # Formating le passé récent
    card_frontside.append('Passé récent: ' + word)
    card_backside.append('Je viens de ' + word.lower() + ', Tu viens de ' + word.lower() + ', Il/elle vient de ' + word.lower() + ', Nous venons de ' + word.lower() + ', Vous venez de ' + word.lower() + ', Ils/elles viennent de ' + word.lower())
    translations.append('Acabei de ' + translation)
    
    write_csv(card_backside, card_frontside, translations, csv_fileName)
    tac = time.time()
    print(word.capitalize() + ': conjugado! (' + str(tac-tic) + 's)')

driver.quit()

fim = time.time()

print('')
print('Tempo total de execução: ' + str(fim-inicio) + 's')