import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time
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
omega = (
    0b00000,
    0b01110,
    0b10001,
    0b10001,
    0b10001,
    0b01010,
    0b11011,
    0b00000,
)

pi = (
    0b00000,
    0b00000,
    0b11111,
    0b01010,
    0b01010,
    0b01010,
    0b10011,
    0b00000,
)

mu = (
    0b00000,
    0b10010,
    0b10010,
    0b10010,
    0b10010,
    0b11101,
    0b10000,
    0b10000,
)

drop = (
    0b00100,
    0b00100,
    0b01010,
    0b01010,
    0b10001,
    0b10001,
    0b10001,
    0b01110,
)

temp = (
    0b00100,
    0b01010,
    0b01010,
    0b01110,
    0b01110,
    0b11111,
    0b11111,
    0b01110,
)

bun = (
	0b00000,
	0b01010,
	0b10001,
	0b11110,
	0b01010,
	0b01010,
	0b10100,
	0b00000,
)
lcd.create_char(0, bun)
lcd.create_char(1, pi)
lcd.create_char(2, mu)
lcd.create_char(3, drop)
lcd.create_char(4, temp)
lcd.display = True
string = "1" + "\x00" + " late"
lcd.message = string
time.sleep(5)
lcd.backlight = False
time.sleep(3)
lcd.display = False
time.sleep(3)
lcd.display = True
