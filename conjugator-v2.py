import os
from selenium.webdriver import Firefox
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep, time
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
    infinitif = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[2]/h2[1]/div/a').text
    translation = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[1]/div/div[3]/p').text.capitalize()

    # Formating
    card_frontside = 'Futur proche: ' + infinitif.capitalize()
    card_backside = 'Je vais ' + infinitif + ', Tu vas ' + infinitif + ', Il/elle va ' + infinitif + ', Nous allons ' + infinitif + ', Vous allez ' + infinitif + ', Ils/elles vont ' + infinitif
    
    write_csv(card_frontside, card_backside, translation, csv_output_filename)

def passe_recent(driver, word, csv_output_filename):
    # Scraping
    infinitif = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[2]/h2[1]/div/a').text
    translation = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[1]/div/div[3]/p').text.capitalize()

    # Formating
    card_frontside = 'Passé récent: ' + infinitif.capitalize()
    card_backside = 'Je viens de ' + infinitif + ', Tu viens de ' + infinitif + ', Il/elle vient de ' + infinitif + ', Nous venons de ' + infinitif + ', Vous venez de ' + infinitif + ', Ils/elles viennent de ' + infinitif

    write_csv(card_frontside, card_backside, translation, csv_output_filename)

def present_indicatif_pronominal(driver, word, csv_output_filename):
    # Scraping
    present_pronominal = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[1]/div[2]/div').text.split()
    translation = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[1]/div/div[3]/p').text.capitalize()

    # Formatting
    card_frontside = present_pronominal[0] + ': ' + word # Setting card frontside

    back = ''
    if len(present_pronominal) == 15:
        for i in range(1,7,2): # Setting card backside
            back += present_pronominal[i].capitalize() + ' ' + present_pronominal[i+1] + ', '

        for i in range(7,len(present_pronominal)-2,3):
            back += present_pronominal[i].capitalize() + ' ' + present_pronominal[i+1] + ' ' + present_pronominal[i+2] + ', '

        back += present_pronominal[13].capitalize() + ' ' + present_pronominal[14]

        card_backside = back
        write_csv(card_frontside, card_backside, translation, csv_output_filename)

    else:
        for i in range(1,len(present_pronominal),3): # Setting card backside
            back += present_pronominal[i].capitalize() + ' ' + present_pronominal[i+1] + ' ' + present_pronominal[i+2] + ', '
            
        card_backside = back[0:len(back)-2]
        write_csv(card_frontside, card_backside, translation, csv_output_filename)

def passe_compose_pronominal(driver, word, csv_output_filename):
    # Scraping
    pc_pronominal = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[3]/div[2]/div').text.split()
    translation = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[1]/div/div[3]/p').text.capitalize()
    
    # Formatting
    card_frontside = pc_pronominal[0] + ' ' + pc_pronominal[1] + ': ' + word # Setting card frontside

    back = 'Je ' + ' '.join(pc_pronominal[3:6]) + ', '

    for i in range(6,15,3): # Setting card backside
        back += pc_pronominal[i].capitalize() + ' ' + pc_pronominal[i+1] + ' ' + pc_pronominal[i+2] + ', '

    for i in range(15,len(pc_pronominal),4): # Setting card backside
        back += pc_pronominal[i].capitalize() + ' ' + pc_pronominal[i+1] + ' ' + pc_pronominal[i+2] + ' ' + pc_pronominal[i+3] + ', '

    card_backside = back[0:len(back)-2]
    write_csv(card_frontside, card_backside, translation, csv_output_filename)
    
def futur_indicatif_pronominal(driver, word, csv_output_filename):
    # Scraping
    futur_pronominal = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[1]/div[4]/div').text.split()
    translation = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[1]/div/div[3]/p').text.capitalize()

    # Formatting
    card_frontside = futur_pronominal[0] + ': ' + word # Setting card frontside

    back = ''
    if len(futur_pronominal) == 15:
        for i in range(1,7,2): # Setting card backside
            back += futur_pronominal[i].capitalize() + ' ' + futur_pronominal[i+1] + ', '

        for i in range(7,len(futur_pronominal)-2,3):
            back += futur_pronominal[i].capitalize() + ' ' + futur_pronominal[i+1] + ' ' + futur_pronominal[i+2] + ', '

        back += futur_pronominal[13].capitalize() + ' ' + futur_pronominal[14]

        card_backside = back
        write_csv(card_frontside, card_backside, translation, csv_output_filename)

    else:
        for i in range(1,len(futur_pronominal),3): # Setting card backside
            back += futur_pronominal[i].capitalize() + ' ' + futur_pronominal[i+1] + ' ' + futur_pronominal[i+2] + ', '
            
        card_backside = back[0:len(back)-2]
        write_csv(card_frontside, card_backside, translation, csv_output_filename)

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

    # Wait for translation
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[3]/div[1]/div/div[3]/p'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print ("Timed out waiting for page to load")

    if word.startswith("S'") or word.startswith("Se"): # For pronominal verbs
        tic = time()
        present_indicatif_pronominal(driver, word, csv_output_filename)
        passe_compose_pronominal(driver, word, csv_output_filename)
        futur_indicatif_pronominal(driver, word, csv_output_filename)
        tac = time()
        print(word + ': conjugado! (' + str(round(tac - tic, 2)) + 's)')

    else: # For normal verbs
        tic = time()
        present_indicatif(driver, word, csv_output_filename)
        passe_compose(driver, word, csv_output_filename)
        futur_indicatif(driver, word, csv_output_filename)
        futur_proche(driver, word, csv_output_filename)
        passe_recent(driver, word, csv_output_filename)
        tac = time()
        print(word + ': conjugado! (' + str(round(tac - tic, 2)) + 's)')

print('\nFim da execução\n')

driver.quit()