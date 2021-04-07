import os
from selenium.webdriver import Firefox
import time
from bs4 import BeautifulSoup

#Create display variable
os.environ["DISPLAY"] = ":0"

driver = Firefox()
driver.get("https://conjugator.reverso.net/conjugation-french.html")

words = ['faire', 'aller']

tic = time.time()

for word in words:
    #Loop through desired words
    search_box = driver.find_element_by_name('ctl00$txtVerb')
    search_box.send_keys(word)

    conjugate = driver.find_element_by_id('lbConjugate')
    conjugate.click()
    
    present = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[1]/div[2]/div').text
    print(present)

    print('-------')

    future = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[1]/div[4]/div').text
    print(future)

tac = time.time()

print(tac - tic, ' segundos')

driver.quit()