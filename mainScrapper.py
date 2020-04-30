from scrapper import getSchedule
import pandas as pd
from datetime import datetime, timedelta
import time
# import board
# import digitalio
# import adafruit_character_lcd.character_lcd as characterlcd
import regex
# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2
start = time.time()  
# Raspberry Pi Pin Config:
# lcd_rs = digitalio.DigitalInOut(board.D26)
# lcd_en = digitalio.DigitalInOut(board.D19) 
# lcd_d7 = digitalio.DigitalInOut(board.D27)
# lcd_d6 = digitalio.DigitalInOut(board.D22)
# lcd_d5 = digitalio.DigitalInOut(board.D24)
# lcd_d4 = digitalio.DigitalInOut(board.D25)
# lcd_backlight = digitalio.DigitalInOut(board.D4)
 
# Initialise the lcd class
# lcd = characterlcd.Character_LCD_Mono(
#      lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
# )

#Minami-APU
getSchedule("https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=1&stSid=a3526885-da77-43dc-9bc3-3cfe3a7b1999",'Minami-APU')

#Minami-Eki
# getSchedule("https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=2&stSid=e64c5d40-62af-4efd-b242-da26ae5502dd", 'Minami-Eki')

#Daisan-APU
# getSchedule("https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=1&stSid=924e8147-7112-437e-9fe8-a6a3bb8e07fd", 'Daisan-APU')

#Daisan-Eki
# getSchedule("https://www.busdoko-oita.jp/map/SpecialRoute/Route?spId=1&drId=1&stSid=924e8147-7112-437e-9fe8-a6a3bb8e07fd", 'Daisan-Eki')

def readData(station):
    data = pd.read_json(station + '.json',orient='columns')
    return data

def getIndex(arrival):
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

data = readData('Minami-APU')
arrival = pd.Series.tolist(data['ArrivalTime'])
busno = pd.Series.tolist(data['BusNo'])
state = pd.Series.tolist(data['BusState'])
indx = getIndex(arrival)
State = []
for i in state:
    if str(i) == "":
        State.append(i)
    elif str(i).strip() == "通常運行":
        State.append("On time")
    else:
        res = regex.findall("\d+",str(i))
        State.append(res[0] + '\x00' + ' late')
       
if type(indx) is tuple:
    print(busno[indx[0]],' ', arrival[indx[0]], ' ', State[indx[0]])
    print(busno[indx[1]],' ', arrival[indx[1]], ' ', State[indx[1]])
#     lcd.clear()
#     lcd.message = str(busno[indx[0]])+ ' ' + str(arrival[indx[0]]) + ' ' + str(State[indx[0]]) + '\n' + str(busno[indx[1]]) + ' ' +str(arrival[indx[1]]) + ' ' + str(State[indx[1]])
else:
    print(busno[indx],' ', arrival[indx], ' ', State[indx])
#     lcd.clear()
#     lcd.message = str(busno[indx]) + ' ' + str(arrival[indx]) + ' ' + str(State[indx])
print(time.time()-start)
