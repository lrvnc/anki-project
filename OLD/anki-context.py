import os
from selenium.webdriver import Firefox
import time
import pandas as pd
import csv

def write_csv(words, translations, examples, tags, csv_fileName):
    d = {'word': words, 'traslation': translations, 'example': examples, 'tag': tags}
    df = pd.DataFrame(data=d)

    doc = open('anki-cards/' + str(csv_fileName), 'w')
    doc.write(df.to_csv(header=False, index=False))
    doc.close()

csv_file = input('CSV file address: ')
csv_fileName = input('CSV file name output: ')

# Create display variable
os.environ["DISPLAY"] = ":0"

inicio = time.time()

# Lists
with open(csv_file, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

words = []
for i in range(len(data)):
    words.append(str(data[i][0]).capitalize())

print('Pesquisando ' + str(len(words)) + ' palavras\n')

translations = []
tags = []
examples = []
card_front = []

driver = Firefox()
driver.get("https://context.reverso.net/traducao/frances-portugues/")

# New tab with Michaelis fr-pt
driver.execute_script('''window.open("https://michaelis.uol.com.br/escolar-frances","_blank");''')

context = driver.window_handles[0] # handle to context tab
michaelis = driver.window_handles[1] # handle to michaelis tab

for word in words:

    tic = time.time()

    # Search the word in contex
    driver.switch_to.window(context)
    driver.find_element_by_xpath('//*[@id="entry"]').send_keys(word)
    driver.find_element_by_xpath('//*[@id="search-button"]').click()

    # Extracting tag
    tags.append(driver.find_element_by_xpath('/html/body/div[3]/section[1]/div[2]/section[3]/div[1]/button[1]').text.capitalize())

    # Extracting translation
    translation = driver.find_element_by_xpath('//*[@id="translations-content"]').text.split('\n')[0]
    translations.append(translation.capitalize())

    # Extracting example
    examples.append(driver.find_element_by_xpath('/html/body/div[3]/section[1]/div[2]/section[4]/div[1]/div[1]/span').text)

    # Search the fonetic transcription on Michaelis
    driver.switch_to.window(michaelis)
    driver.find_element_by_id('input-search').send_keys(word)
    driver.find_element_by_id('btn-search').click()

    # Extracting fonetic transcription
    fonetic_transcription = driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[3]/et').text

    # Formating card's front
    card_front.append(word + ' ' + fonetic_transcription)

    # Write .csv file
    write_csv(card_front, translations, examples, tags, csv_fileName)
    tac = time.time()
    print(word.capitalize() + ': feito! (' + str(tac-tic) + 's)')

driver.quit()

fim = time.time()

print('')
print('Tempo total de execução: ' + str(fim-inicio) + 's')