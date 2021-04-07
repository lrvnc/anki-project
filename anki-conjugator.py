import os
from selenium.webdriver import Firefox
import time

#Create display variable
os.environ["DISPLAY"] = ":0"

driver = Firefox()
driver.get("https://conjugator.reverso.net/conjugation-french.html")

search_box = driver.find_element_by_name('ctl00$txtVerb')
search_box.send_keys('Faire')

conjugate = driver.find_element_by_id('lbConjugate')
conjugate.click()

search_box = driver.find_element_by_name('ctl00$txtVerb')
search_box.send_keys('Aller')

conjugate = driver.find_element_by_id('lbConjugate')
conjugate.click()

time.sleep(5)
driver.quit()