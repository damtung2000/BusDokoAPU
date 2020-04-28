from gpiozero import Button
from signal import pause
button = Button(21,pull_up=False)
def pressed():
  print("Button pressed")
button.when_pressed = pressed
pause()

