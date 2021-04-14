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

# Create display variable
os.environ["DISPLAY"] = ":0"

# Lists
words = ['Maison', 'Serpent', 'Enfant', 'Soeur', 'Frère', 'Jouet']
translations = []
tag = []
example = []

driver = Firefox()
driver.get("https://context.reverso.net/traducao/frances-portugues/")

for word in words:
    # Search the word
    driver.find_element_by_xpath('//*[@id="entry"]').send_keys(word)
    driver.find_element_by_xpath('//*[@id="search-button"]').click()

    # Extracting tag
    tag.append(driver.find_element_by_xpath('/html/body/div[3]/section[1]/div[2]/section[3]/div[1]/button[1]').text.capitalize())
    print(tag)

    # Extracting translation
    translation = driver.find_element_by_xpath('//*[@id="translations-content"]').text.split('\n')[0]
    translations.append(translation.capitalize())
    print(translations)

    # Extracting example
    example.append(driver.find_element_by_xpath('/html/body/div[3]/section[1]/div[2]/section[4]/div[1]/div[1]/span').text)
    print(example)

    time.sleep(1)

driver.quit()