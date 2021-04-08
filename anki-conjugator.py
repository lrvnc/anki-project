import os
from selenium.webdriver import Firefox
import time
import pandas as pd

#Create display variable
os.environ["DISPLAY"] = ":0"

driver = Firefox()
driver.get("https://conjugator.reverso.net/conjugation-french.html")

#List of desired words
words = ['sortir', 'mettre', 'prendre', 'faire']

#Lists to save the verbs
card_frontside = []
card_backside = []
back = ''

#Loop through desired words
for word in words:
    #Search the word
    search_box = driver.find_element_by_name('ctl00$txtVerb')
    search_box.send_keys(word)

    conjugate = driver.find_element_by_id('lbConjugate')
    conjugate.click()
    
    #Scrap le présent, le futur and le passé composé
    present = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[1]/div[2]/div').text.split()
    futur = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[1]/div[4]/div').text.split()
    passe_compose = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/form/div[3]/div/div[1]/div[4]/div/div/div[3]/div[2]/div').text.split()
    print(passe_compose)

    #Formating le présent
    card_frontside.append(present[0] + ': ' + word) #Setting the front of the card

    for i in range(1,len(present),2): #Setting the back of the card
        back += present[i].capitalize() + ' ' + present[i+1] + ', '

    card_backside.append(back[0:len(back)-2])
    back = ''

    #Formating le futur
    card_frontside.append(futur[0] + ': ' + word) #Setting the front of the card

    for i in range(1,len(futur),2): #Setting the back of the card
        back += futur[i].capitalize() + ' ' + futur[i+1] + ', '

    card_backside.append(back[0:len(back)-2])
    back = ''

    #Formating le passé composé
    card_frontside.append(passe_compose[0] + ' ' + passe_compose[1] + ' (avec avoir): ' + word)
    
    back = passe_compose[2].capitalize() + ' ' + passe_compose[3] + ', '
    for i in range(4,19,3): #Setting the back of the card
        back += passe_compose[i].capitalize() + ' ' + passe_compose[i+1] + ' ' + passe_compose[i+2] + ', '
    card_backside.append(back[0:len(back)-2])
    back = ''

    if len(passe_compose) != 19:
        card_frontside.append(passe_compose[0] + ' ' + passe_compose[1] + ' (avec être): ' + word)
        
        for i in range(19,len(passe_compose),3): #Setting the back of the card
            back += passe_compose[i].capitalize() + ' ' + passe_compose[i+1] + ' ' + passe_compose[i+2] + ', '
            print(back)
        card_backside.append(back[0:len(back)-2])
        back = ''



d = {'front': card_frontside, 'back': card_backside}
df = pd.DataFrame(data=d)

doc = open('verbs_csv', 'w')
doc.write(df.to_csv(header=False, index=False))
doc.close()

driver.quit()