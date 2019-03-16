import time
import csv
from signal import pause
from gpiozero import Button
from pyfingerprint.pyfingerprint import PyFingerprint

button_1 = Button(2)
button_2 = Button(3)
button_3 = Button(4)
button_yes = Button(17)
button_no = Button(27)
button_result= Button(22)
while(not(button_1.is_pressed) and not(button_2.is_pressed) and not(button_3.is_pressed) and not(button_result.is_pressed)):
	print(button_1.is_pressed)
