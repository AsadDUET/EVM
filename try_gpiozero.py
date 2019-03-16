from gpiozero import Button
from signal import pause
button = Button(2)
button1 = Button(3)
while True:
    print(button.is_pressed)
