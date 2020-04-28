from scrapper import getSchedule
import pandas as pd
from datetime import datetime, timedelta
import time
import regex
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# 
# def button_callback(channel):
#     print("Button was pushed!")
#     
# GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #set pin 21 to be input
# GPIO.add_event_detect(21,GPIO.RISING,callback=button_callback)

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
bun = (0b00000,
    0b01010,
    0b10001,
    0b11110,
    0b01010,
    0b01010,
    0b10100,
    0b00000,
)
lcd.create_char(0,bun)
# Minami-APU
# getSchedule("https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=1&stSid=a3526885-da77-43dc-9bc3-3cfe3a7b1999",'Minami-APU')

# Minami-Eki
# getSchedule("https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=2&stSid=e64c5d40-62af-4efd-b242-da26ae5502dd", 'Minami-Eki')

# Daisan-APU
# getSchedule("https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=1&stSid=924e8147-7112-437e-9fe8-a6a3bb8e07fd", 'Daisan-APU')

# Daisan-Eki
# getSchedule("https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=1&stSid=924e8147-7112-437e-9fe8-a6a3bb8e07fd", 'Daisan-Eki')

# lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
def readData(station):
    data = pd.read_json(station + '.json',orient='columns')
    return data

def getIndex():
    # print(arrival)
    indx = 0
    for i in arrival:
        now = datetime.now()
        then = datetime.combine(now, datetime.strptime(i, '%H:%M').time())
        minutesLeft = (then - now) // timedelta(minutes=1)
        if (minutesLeft > 0):
            indx = arrival.index(i)
            break
    if indx == (len(arrival)-1):
        print(i)
        return indx
    elif indx < (len(arrival)-1):
        nextBusindx = indx + 1
        print(i, arrival[nextBusindx])
        return indx, nextBusindx

#getSchedule("https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=1&stSid=a3526885-da77-43dc-9bc3-3cfe3a7b1999",'Minami-APU')
data = readData('Minami-Eki')
arrival = pd.Series.tolist(data['ArrivalTime'])
busno = pd.Series.tolist(data['BusNo'])
state = pd.Series.tolist(data['BusState'])
indx = getIndex()
indx = (1,2) #for testing only
State = []
print(data)
for i in state:
    if str(i) == "":
        State.append(i)
    elif str(i) == "On schedule":
        State.append("On time")
    else:
        res = regex.findall("(\d+)",str(i))
#         print(i)
#         print(res)
        State.append(str(res[0]) + "\x00" + " late")     
#         print(State)

if type(indx) is tuple:
    print(busno[indx[0]],' ', arrival[indx[0]], ' ', State[indx[0]])
    print(busno[indx[1]],' ', arrival[indx[1]], ' ', State[indx[1]])
    lcd.clear()
    lcd.message = str(busno[indx[0]])+ ' ' + str(arrival[indx[0]]) + ' ' + str(State[indx[0]]) + '\n' + str(busno[indx[1]]) + ' ' +str(arrival[indx[1]]) + ' ' + str(State[indx[1]])
else:
    print(busno[indx],' ', arrival[indx], ' ', State[indx])
    lcd.clear()
    lcd.message= str(busno[indx]) + ' ' + str(arrival[indx]) + ' ' + str(State[indx])

    


