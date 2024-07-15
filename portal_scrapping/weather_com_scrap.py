from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://weather.com/weather/hourbyhour/l/52470ef5376650623511d8279c999373aa4e8c46d1865a74b5274fe665fdf5dd#detailIndex4'

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
