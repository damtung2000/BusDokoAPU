import time

start = time.time()
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")


def getSchedule(url, name):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    #     english = driver.find_element_by_class_name('languageButton')
    #     english.click()
    #     English = driver.find_element_by_id('modal-language-en')
    #     English.click()
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "arrivalTime"))
        )
        arrivalTimeElements = driver.find_elements_by_class_name("arrivalTime")

        busNumberElements = driver.find_elements_by_class_name("courseNo")

        busStateElements = driver.find_elements_by_class_name("busState")
        #         for i in arrivalTime:
        #             print(i.text)
        #         for i in busNo:
        #             print(i.text)
        #         for i in busState:
        #             print(i.text)
        arrivalTime = []
        busNumber = []
        busState = []
        busCondition = []
        i = 0
        for i in arrivalTimeElements:
            arrivalTime.append(i.text)
        for i in busNumberElements:
            busNumber.append(i.text[0:2])
        for i in busStateElements:
            busState.append(i.text)
        busCondition = {
            "BusNo": busNumber,
            "ArrivalTime": arrivalTime,
            "BusState": busState,
        }

        #     busCondition = list(zip(busno,arrivaltime,busstate))
        # columns = ["BusNo","ArrivalTime","BusState"]

        # apply result to dataframe
        df = pd.DataFrame(busCondition)
        # write to json
        df.to_json("%s.json" % name)
        print(df)
        print(time.time() - start)
    finally:
        driver.quit()
