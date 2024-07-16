from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://www.google.com/search?q=pogoda+warszawa&rlz=1C1GCEA_enPL1017PL1017&oq=pogoda+wa&gs_lcrp=EgZjaHJvbWUqEQgAEEUYJxg7GJ0CGIAEGIoFMhEIABBFGCcYOxidAhiABBiKBTIJCAEQRRg5GIAEMg0IAhAAGIMBGLEDGIAEMg0IAxAAGIMBGLEDGIAEMg0IBBAAGIMBGLEDGIAEMgYIBRBFGDwyBggGEEUYPDIGCAcQRRg8qAIAsAIA&sourceid=chrome&ie=UTF-8'

driver = webdriver.Chrome()

driver.get(url)

temp_elements = driver.find_elements(By.CSS_SELECTOR, 'span.DetailsSummary--tempValue--jEiXE')

x = 0
temp_list = []

for element in temp_elements:
    x += 1
    temp = element.text
    temp_list.append(temp)

print(x)
print(temp_list)
print(len(temp_list))

driver.quit()



temp_elements = driver.find_elements(By.CSS_SELECTOR, 'span.DetailsSummary--tempValue--jEiXE')

x = 0
temp_list = []

for element in temp_elements:
    x += 1
    temp = element.text
    temp_list.append(temp)

print(x)
print(temp_list)
print(len(temp_list))

driver.quit()
