import os
from selenium.webdriver import Firefox
import time
import csv

def write_csv(card_frontside, card_backside, translation, csv_output_filename):
    doc = open('anki-cards/' + str(csv_output_filename), 'a')
    doc.write(card_frontside + ', "' + card_backside + '", ' + translation + '\n')
    doc.close()

def present_indicatif(driver, word, csv_output_filename):
    # Scraping
    present = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[1]/div[2]/div').text.split()
    translation = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[1]/div/div[3]/p').text.capitalize()

    # Formatting
    card_frontside = present[0] + ': ' + word # Setting card frontside
    
    if len(present)!=13:
        back = present[1].capitalize() + ', '
        for i in range(2,len(present),2): # Setting card backside
            back += present[i].capitalize() + ' ' + present[i+1] + ', '

    else:
        back = ''
        for i in range(1,len(present),2): # Setting card backside
            back += present[i].capitalize() + ' ' + present[i+1] + ', '

    card_backside = back[0:len(back)-2]
    write_csv(card_frontside, card_backside, translation, csv_output_filename)

def passe_compose(driver, word, csv_output_filename):
    # Scraping
    passe_compose = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[3]/div[2]/div').text.split()
    translation = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[1]/div/div[3]/p').text.capitalize()

    # Formatting
    if passe_compose[2]=="j'ai":
        card_frontside = passe_compose[0] + ' ' + passe_compose[1] + ' (avec avoir): ' + word # Setting card frontside
        back = passe_compose[2].capitalize() + ' ' + passe_compose[3] + ', '
        for i in range(4,19,3): # Setting card backside
            back += passe_compose[i].capitalize() + ' ' + passe_compose[i+1] + ' ' + passe_compose[i+2] + ', '
        card_backside = back[0:len(back)-2]
        write_csv(card_frontside, card_backside, translation, csv_output_filename)

    if passe_compose[2]=="je":
        card_frontside = passe_compose[0] + ' ' + passe_compose[1] + ' (avec être): ' + word
        back = ''
        for i in range(2,len(passe_compose),3): # Setting card backside
            back += passe_compose[i].capitalize() + ' ' + passe_compose[i+1] + ' ' + passe_compose[i+2] + ', '
        card_backside = back[0:len(back)-2]
        write_csv(card_frontside, card_backside, translation, csv_output_filename)

    if passe_compose[2]=="j'ai" and len(passe_compose)!=19:
        card_frontside = passe_compose[0] + ' ' + passe_compose[1] + ' (avec être): ' + word
        back = ''
        for i in range(19,len(passe_compose),3): # Setting card backside
            back += passe_compose[i].capitalize() + ' ' + passe_compose[i+1] + ' ' + passe_compose[i+2] + ', '
        card_backside = back[0:len(back)-2]
        write_csv(card_frontside, card_backside, translation, csv_output_filename)

def futur_indicatif(driver, word, csv_output_filename):
    # Scraping
    futur = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[1]/div[4]/div').text.split()
    translation = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[1]/div/div[3]/p').text.capitalize()

    # Formatting
    card_frontside = futur[0] + ': ' + word #Setting card frontside

    if len(futur)!=13:
        back = futur[1].capitalize() + ', '
        for i in range(2,len(futur),2): # Setting card backside
            back += futur[i].capitalize() + ' ' + futur[i+1] + ', '
    else:
        back = ''
        for i in range(1,len(futur),2): # Setting card backside
            back += futur[i].capitalize() + ' ' + futur[i+1] + ', '

    card_backside = back[0:len(back)-2]
    write_csv(card_frontside, card_backside, translation, csv_output_filename)

def futur_proche(driver, word, csv_output_filename):
    # Scraping
    translation = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[1]/div/div[3]/p').text.capitalize()

    # Formating
    card_frontside = 'Futur proche: ' + word
    card_backside = 'Je vais ' + word.lower() + ', Tu vas ' + word.lower() + ', Il/elle va ' + word.lower() + ', Nous allons ' + word.lower() + ', Vous allez ' + word.lower() + ', Ils/elles vont ' + word.lower()
    
    write_csv(card_frontside, card_backside, translation, csv_output_filename)

def passe_recent(driver, word, csv_output_filename):
    # Scraping
    translation = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[1]/div/div[3]/p').text.capitalize()

    # Formating
    card_frontside = 'Passé récent: ' + word
    card_backside = 'Je viens de ' + word.lower() + ', Tu viens de ' + word.lower() + ', Il/elle vient de ' + word.lower() + ', Nous venons de ' + word.lower() + ', Vous venez de ' + word.lower() + ', Ils/elles viennent de ' + word.lower()

    write_csv(card_frontside, card_backside, translation, csv_output_filename)


'''def present_indicatif_pronominal(driver, word, csv_output_filename):

def passe_compose_pronominal(driver, word, csv_output_filename):'''

csv_input = input('Words .csv file path: ') + '.csv'
csv_output_filename = input('Filename output: ') + '.csv'

# Creating display variable
os.environ["DISPLAY"] = ":0"

# Starting Firefox, opening reverso conjugator
driver = Firefox()
driver.get("https://conjugacao.reverso.net/conjugacao-frances.html")

# Auxiliar list
words = []

# Reading desired words
with open(csv_input, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
for i in range(len(data)):
    words.append(str(data[i][0]).capitalize())


print('\nPesquisando ' + str(len(words)) + ' verbos\n')

# Looping through the words
for word in words:
    # Searching
    driver.find_element_by_name('ctl00$txtVerb').send_keys(word)
    driver.find_element_by_id('lbConjugate').click()

    present_indicatif(driver, word, csv_output_filename)
    passe_compose(driver, word, csv_output_filename)
    futur_indicatif(driver, word, csv_output_filename)
    futur_proche(driver, word, csv_output_filename)
    passe_recent(driver, word, csv_output_filename)

driver.quit()