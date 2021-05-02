import os
from selenium.webdriver import Firefox
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep, time
import csv

def write_csv(card_frontside, card_backside, example, tag, csv_output_filename):
    doc = open('anki-cards/' + str(csv_output_filename), 'a')
    doc.write(card_frontside + ', "' + card_backside + '", "' + example +'", ' + tag + '\n')
    doc.close()

def translate(driver, word):
    # Scraping
    tag = driver.find_element_by_xpath('/html/body/div[3]/section[1]/div[2]/section[3]/div[1]/button[1]').text.capitalize()
    translation = driver.find_element_by_xpath('//*[@id="translations-content"]').text.split('\n')[0]
    example = driver.find_element_by_xpath('/html/body/div[3]/section[1]/div[2]/section[4]/div[1]/div[1]/span').text
    return tag, translation.capitalize(), example

def transcription(driver, word):
    ft = driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[3]/et').text
    return ft



csv_input = input('Words .csv file path: ') + '.csv'
csv_output_filename = input('Filename output: ') + '.csv'

# Creating display variable
os.environ["DISPLAY"] = ":0"

# Starting Firefox, opening reverso conjugator
driver = Firefox()
driver.get("https://context.reverso.net/traducao/frances-portugues/")

# New tab with Michaelis fr-pt
driver.execute_script('''window.open("https://michaelis.uol.com.br/escolar-frances","_blank");''')

# Tab handles
context = driver.window_handles[0]
michaelis = driver.window_handles[1]

# Auxiliar list
words = []

# Reading desired words
with open(csv_input, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
for i in range(len(data)):
    words.append(str(data[i][0]).capitalize())

print('\nPesquisando ' + str(len(words)) + ' palavras\n')

for word in words:

    tic = time()

    # Open Context
    driver.switch_to.window(context)
    driver.find_element_by_xpath('//*[@id="entry"]').send_keys(word)
    driver.find_element_by_xpath('//*[@id="search-button"]').click()
    tag, translation, example = translate(driver, word)

    # Open Michaelis
    driver.switch_to.window(michaelis)
    driver.find_element_by_id('input-search').send_keys(word)
    driver.find_element_by_id('btn-search').click()

    if driver.find_element_by_id('content').text.startswith('O verbete não foi encontrado.'):
        print(word + ': transcrição fonética não encontrada')
        write_csv(word, translation, example, tag, csv_output_filename)
    else:
        ft = transcription(driver, word)
        write_csv(word + ' ' + ft, translation, example, tag, csv_output_filename)

    tac = time()

    print(word + ': feito! (' + str(round(tac - tic, 2)) + 's)')

print('\nFim da execução\n')

driver.quit()