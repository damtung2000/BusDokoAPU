import time
start = time.time()
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
url = "https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=1&stSid=a3526885-da77-43dc-9bc3-3cfe3a7b1999"
driver.get(url)
english = driver.find_element_by_class_name('languageButton')
english.click()
English = driver.find_element_by_id('modal-language-en')
English.click()
time.sleep(1)
# arrivalTime = driver.find_elements_by_class_name('arrivalTime')
# 
# busNo = driver.find_elements_by_class_name('courseNo')
# # busNum = driver.find_elements_by_xpath('//*[@class="courseNo"]/div')
# busState = driver.find_elements_by_class_name('busState')

soup = BeautifulSoup(driver.page_source,'html.parser')
arrivalTime = soup.find_all('td',attrs={'class': 'arrivalTime'})
busNo = soup.find_all('td',{'class': 'courseNo'})
busState = soup.find_all('td',attrs= {'class': 'busState'})
for i in arrivalTime:
    print(i.text.strip())
for i in busNo:
    print(i.text.strip())
for i in busState:
    print(i.text.strip())
print(time.time()-start)
breakpoint()
arrivaltime = []
busno = []
busstate = []
for i in arrivalTime:
    arrivaltime.append(i.text)
for i in busNo:
    busno.append(i.text)
for i in busState:
    busstate.append(i.text)

busCondition = list(zip(busno,arrivaltime,busstate))

df=pd.DataFrame(busCondition, columns = ["BusNo","ArrivalTime","BusState"])
# write to json
df.to_json('busResult.json')
print(df)

