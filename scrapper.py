import time
start = time.time()
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_options = Options()
chrome_options.add_argument("--headless")
def getSchedule(url,name):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
#     english = driver.find_element_by_class_name('languageButton')
#     english.click()
#     English = driver.find_element_by_id('modal-language-en')
#     English.click()
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "arrivalTime")))
        arrivalTime = driver.find_elements_by_class_name('arrivalTime')

        busNo = driver.find_elements_by_class_name('courseNo')
    # busNum = driver.find_elements_by_xpath('//*[@class="courseNo"]/div')
    
        busState = driver.find_elements_by_class_name('busState')
#         for i in arrivalTime:
#             print(i.text)
#         for i in busNo:
#             print(i.text)
#         for i in busState:
#             print(i.text)
        arrivaltime = []
        busno = []
        busstate = []
        busCondition = []
        i = 0
        for i in arrivalTime:
            arrivaltime.append(i.text)
        for i in busNo:
            busno.append(i.text[0:2])
        for i in busState:
            busstate.append(i.text)
        busCondition = {'BusNo':busno,'ArrivalTime':arrivaltime,'BusState':busstate}

    #     busCondition = list(zip(busno,arrivaltime,busstate))
    # columns = ["BusNo","ArrivalTime","BusState"]

        #apply result to dataframe
        df=pd.DataFrame(busCondition)
        # write to json
        df.to_json('%s.json' % name)
        print(df)
        print(time.time()-start)
    finally:
        driver.quit()
    

<<<<<<< HEAD
   # soup = BeautifulSoup(driver.page_source,'html.parser')
   
        
# getSchedule("https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=1&stSid=a3526885-da77-43dc-9bc3-3cfe3a7b1999",'Minami')
=======
    #apply result to dataframe
    df=pd.DataFrame(busCondition)
    # write to json
    df.to_json('%s.json' % name)
    print(df)
    print(time.time()-start)
#getSchedule("https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=1&stSid=a3526885-da77-43dc-9bc3-3cfe3a7b1999",'Minami')
>>>>>>> master

