import os
os.environ["DISPLAY"] = ":0"

#Simple assignment
from selenium.webdriver import Firefox

driver = Firefox()
driver.get("https://selenium.dev")
print(driver.current_url)
driver.get("https://google.com")
driver.back()
driver.forward()
driver.refresh()
print(driver.title)