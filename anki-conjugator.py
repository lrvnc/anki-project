import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
import os

os.environ["DISPLAY"] = ":0"

driver = Firefox()

# Pegar conteúdo HTML a partir da URL
url = 'https://www.askpython.com/python/environment-variables-in-python'

option = Options()
option.headless = True

driver.get(url)

time.sleep(5)

driver.quit()
