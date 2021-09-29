from scrapper import getSchedule
import pandas as pd
from datetime import datetime, timedelta
import time
import regex
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import gpiozero as io
from signal import pause

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Raspberry Pi Pin Config:
lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_backlight = digitalio.DigitalInOut(board.D4)

# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
)
japaneseMinuteCharacter = (
    0b00000,
    0b01010,
    0b10001,
    0b11110,
    0b01010,
    0b01010,
    0b10100,
    0b00000,
)
lcd.create_char(0, japaneseMinuteCharacter)
# Minami-APU
lcd.message = "Loading\nMinami-APU"
getSchedule(
    "https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=1&stSid=a3526885-da77-43dc-9bc3-3cfe3a7b1999",
    "Minami-APU",
)

# Minami-Eki
lcd.message = "Loading\nMinami-Eki"
getSchedule(
    "https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=2&stSid=e64c5d40-62af-4efd-b242-da26ae5502dd",
    "Minami-Eki",
)

# Daisan-APU
lcd.message = "Loading\nDaisan-APU"
getSchedule(
    "https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=1&stSid=924e8147-7112-437e-9fe8-a6a3bb8e07fd",
    "Daisan-APU",
)

# Daisan-Eki
lcd.message = "Loading\nDaisan-APU"
getSchedule(
    "https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=1&stSid=924e8147-7112-437e-9fe8-a6a3bb8e07fd",
    "Daisan-Eki",
)


def readData(station):
    data = pd.read_json(station + ".json", orient="columns")
    return data


def getIndex(arrivalTime):
    # print(arrival)
    index = 0
    for time in arrivalTime:
        now = datetime.now()
        then = datetime.combine(now, datetime.strptime(time, "%H:%M").time())
        minutesLeft = (then - now) // timedelta(minutes=1)
        if minutesLeft > 0:
            index = arrivalTime.index(time)
            break
    if index == (len(arrivalTime) - 1):
        print(time)
        return index
    elif index < (len(arrivalTime) - 1):
        nextBusIndex = index + 1
        print(time, arrivalTime[nextBusIndex])
        return index, nextBusIndex


def minamiEkibutton():
    data = readData("Minami-Eki")
    arrivalTime = pd.Series.tolist(data["ArrivalTime"])
    busNumber = pd.Series.tolist(data["BusNo"])
    busState = pd.Series.tolist(data["BusState"])
    index = getIndex(arrivalTime)
    currentBusState = []
    print(data)
    for i in busState:
        if str(i) == "":
            currentBusState.append(i)
        elif str(i).strip() == "通常運行":
            currentBusState.append("On time")
        else:
            res = regex.findall("(\d+)", str(i))
            currentBusState.append(str(res[0]) + "\x00" + " late")

    if type(index) is tuple:
        print(
            busNumber[index[0]],
            " ",
            arrivalTime[index[0]],
            " ",
            currentBusState[index[0]],
        )
        print(
            busNumber[index[1]],
            " ",
            arrivalTime[index[1]],
            " ",
            currentBusState[index[1]],
        )
        lcd.clear()
        lcd.message = (
            str(busNumber[index[0]])
            + " "
            + str(arrivalTime[index[0]])
            + " "
            + str(currentBusState[index[0]])
            + "\n"
            + str(busNumber[index[1]])
            + " "
            + str(arrivalTime[index[1]])
            + " "
            + str(currentBusState[index[1]])
        )
    else:
        print(busNumber[index], " ", arrivalTime[index], " ", currentBusState[index])
        lcd.clear()
        lcd.message = (
            str(busNumber[index])
            + " "
            + str(arrivalTime[index])
            + " "
            + str(currentBusState[index])
        )


def clearButton():
    lcd.clear()


minamiButton = io.Button(21, pull_up=False, hold_time=0.5)
minamiButton.when_pressed = minamiEkibutton
minamiButton.when_held = clearButton
pause()
