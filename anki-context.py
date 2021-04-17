import os
from selenium.webdriver import Firefox
import time
import pandas as pd

def write_csv(words, translations, examples, tags):
    d = {'word': words, 'traslation': translations, 'example': examples, 'tag': tags}
    df = pd.DataFrame(data=d)

    doc = open('context_csv', 'w')
    doc.write(df.to_csv(header=False, index=False))
    doc.close()

# Create display variable
os.environ["DISPLAY"] = ":0"

# Lists
words = ['Maison', 'Serpent', 'Enfant', 'Soeur', 'Frère', 'Jouet']
translations = []
tags = []
examples = []

driver = Firefox()
driver.get("https://context.reverso.net/traducao/frances-portugues/")

for word in words:
    # Search the word
    driver.find_element_by_xpath('//*[@id="entry"]').send_keys(word)
    driver.find_element_by_xpath('//*[@id="search-button"]').click()

    # Extracting tag
    tags.append(driver.find_element_by_xpath('/html/body/div[3]/section[1]/div[2]/section[3]/div[1]/button[1]').text.capitalize())

    # Extracting translation
    translation = driver.find_element_by_xpath('//*[@id="translations-content"]').text.split('\n')[0]
    translations.append(translation.capitalize())

    # Extracting example
    examples.append(str(driver.find_element_by_xpath('/html/body/div[3]/section[1]/div[2]/section[4]/div[1]/div[1]/span').text))

    # Write .csv file
    write_csv(words[0:words.index(word)+1], translations, examples, tags)

    time.sleep(1)

driver.quit()