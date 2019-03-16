#! /usr/bin python3
import time
time.sleep(5)
print('Loading...Please Wait')
import csv
from signal import pause
from gpiozero import Button
from gpiozero import LED
from pyfingerprint.pyfingerprint import PyFingerprint
from picamera import PiCamera
import label_image
import sms
button_1 = Button(2)
button_2 = Button(3)
button_3 = Button(4)
button_yes = Button(17)
button_no = Button(27)
button_result= Button(22)

green_led=LED(10)
red_led=LED(9)
buzzer=LED(11)

def vote():
	path="/home/pi/examples/data.csv"
	while True:
		data=[]
		with open(path, newline='') as file:
			reader=csv.reader(file)
			for row in reader:
				datum=int(row[0])
				data.append(datum)
			
		## Tries to search the finger and calculate hash
		try:
			top_design()
			print('Press Red Button to Start')
			bottom_design()
			while True:
				if button_no.is_pressed:
					with PiCamera() as camera:
						camera.start_preview()
						time.sleep(3)
						camera.capture('/home/pi/examples/foo.jpg')
						camera.stop_preview()
					voter=label_image.detect('/home/pi/examples/foo.jpg')
					break
			if voter=='unknown':
				print('Unknown Voter')
			else:
				top_design()
				print('Name: ',voter)
				print('Waiting for finger...')
				bottom_design()
				time.sleep(1)

				## Wait that finger is read
				while ( f.readImage() == False ):
					pass
				time.sleep(.4)
				f.readImage()
				## Converts read image to characteristics and stores it in charbuffer 1
				f.convertImage(0x01)
				## Searchs template
				result = f.searchTemplate()
				positionNumber = result[0]
				accuracyScore = result[1]
				if ( positionNumber == -1 ):
					top_design()
					print('No match found!')
					bottom_design()
					red_led.on()
					time.sleep(2)
					red_led.off()
				else:
					top_design()
					print('Voter Number: ' + str(positionNumber))
					bottom_design()
					if positionNumber in data[3:]:
						top_design()
						print('Already voted')
						sms.sendsms('01868901459',str(voter)+' This person tried to cast a fake Vote')
						bottom_design()
						red_led.on()
						buzzer.on()
						#gsm function
						time.sleep(2)
						red_led.off()
						buzzer.off()
					else:
						while True:
							yes=0
							top_design()
							print('Choose Candidate:')
							print('Candidate-1	Candidate-2	Candidate-3	')
							print('     1              2               3 ')
							bottom_design()
							while True:
								if button_1.is_pressed:
									top_design()
									print('Are You Sure Candidate-1?')
									print('YES	NO')
									print(' Y	 N')
									bottom_design()
									time.sleep(1)
									while True:
										if button_yes.is_pressed:
											yes=1
											data[0]=data[0]+1
											data.append(positionNumber)
											with open(path, 'w') as file:
												writer=csv.writer(file)
												for i in range(len(data)):
													writer.writerow([data[i]])	
											top_design()
											print('Vote Complete')
											bottom_design()
											green_led.on()
											time.sleep(2)
											green_led.off()
											break
										if button_no.is_pressed:
											top_design()
											print('Confermation cancel')
											bottom_design()
											time.sleep(.5)
											break
									time.sleep(2)	
									break			
								if button_2.is_pressed:
									top_design()
									print('Are You Sure Candidate-2?')
									print('YES	NO')
									print(' Y	 N')
									bottom_design()
									time.sleep(1)
									while True:
										if button_yes.is_pressed:
											yes=1
											data[1]=data[1]+1
											data.append(positionNumber)
											with open(path, 'w') as file:
												writer=csv.writer(file)
												for i in range(len(data)):
													writer.writerow([data[i]])	
											top_design()
											print('Vote Complete')
											bottom_design()
											green_led.on()
											time.sleep(2)
											green_led.off()
											break
										if button_no.is_pressed:
											top_design()
											print('Confermation cancel')
											bottom_design()
											time.sleep(.5)
											break
									time.sleep(2)
									break
								if button_3.is_pressed:
									top_design()
									print('Are You Sure Candidate-3?')
									print('YES	NO')
									print(' Y	 N')
									bottom_design()
									time.sleep(1)
									while True:
										if button_yes.is_pressed:
											yes=1
											data[2]=data[2]+1
											data.append(positionNumber)
											with open(path, 'w') as file:
												writer=csv.writer(file)
												for i in range(len(data)):
													writer.writerow([data[i]])	
											top_design()
											print('Vote Complete')
											bottom_design()
											green_led.on()
											time.sleep(2)
											green_led.off()
											break
										if button_no.is_pressed:
											top_design()
											print('Confermation cancel')
											bottom_design()
											time.sleep(.5)
											break
									time.sleep(2)
									break
								if button_result.is_pressed:
									top_design()
									print('Total Vote:'+str(len(data[3:])))
									print('Candidate-1: '+str(data[0]))
									print('Candidate-2: '+str(data[1]))
									print('Candidate-3: '+str(data[2]))
									bottom_design()
									time.sleep(5)
									break
							if yes==1:
								break		

		except:
			raise
			#~ top_design()
			#~ print ('Error')
			#~ bottom_design()
			
			
def add_voter():
	try:
		top_design()
		print('Waiting for finger...')
		bottom_design()
		while ( f.readImage() == False ):
			pass
		time.sleep(.4)
		f.readImage()
		f.convertImage(0x01)
		result = f.searchTemplate()
		positionNumber = result[0]
		if ( positionNumber >= 0 ):
			top_design()
			print('Template already exists at position #' + str(positionNumber)+'\n\n')
			bottom_design()
		else:
			top_design()
			print('Remove finger...')
			bottom_design()
			time.sleep(2)
			top_design()
			print('Waiting for same finger again...')
			bottom_design()
			while ( f.readImage() == False ):
				pass
			time.sleep(.4)
			f.readImage()
			f.convertImage(0x02)
			if ( f.compareCharacteristics() == 0 ):
				top_design()
				print('Fingers do not match\n\n')
				bottom_design()
			else:
				f.createTemplate()
				positionNumber = f.storeTemplate()
				top_design()
				print('Finger enrolled successfully!')
				print('New template position #' + str(positionNumber)+'\n\n')
				bottom_design()
	except:
		top_design()
		print ('Error')
		bottom_design()

	top_design()
	print('Select an Option\n')
	print('Add Voter	Vote	Erase	Result')
	print('    1	          2       3       R')
	bottom_design()
		
def erase():
	top_design()
	print('All data Erased')
	bottom_design()
	path="/home/pi/examples/data.csv"
	data=[0,0,0]
	with open(path, 'w') as file:
		writer=csv.writer(file)
		for i in range(len(data)):
			writer.writerow([data[i]])
	top_design()
	print('Select an Option\n')
	print('Add Voter	Vote	Erase	Result')
	print('    1	          2       3       R')
	bottom_design()
	
	
def result():
	path="home/pi/examples/data.csv"
	data=[]
	with open(path, newline='') as file:
		reader=csv.reader(file)
		for row in reader:
			datum=int(row[0])
			data.append(datum)
	top_design()
	print('Total Vote:'+str(len(data[3:])))
	print('Candidate-1: '+str(data[0]))
	print('Candidate-2: '+str(data[1]))
	print('Candidate-3: '+str(data[2]))
	bottom_design()
	top_design()
	print('Select an Option\n')
	print('Add Voter	Vote	Erase	Result')
	print('    1	          2       3       R')
	bottom_design()

def top_design():
	print('#############################################\n')
def bottom_design():
	print('\n#############################################')









try:
	f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

	if ( f.verifyPassword() == False ):
		raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
	top_design()
	print('The fingerprint sensor could not be initialized!')
	print('Exception message: ' + str(e))
	bottom_design()
	exit(1)

## Gets some sensor information
top_design()
print('Registered Voter: ' + str(f.getTemplateCount()))
bottom_design()


top_design()
print('Select an Option\n')
print('Add Voter	Vote	Erase	Result')
print('    1	          2       3       R')
bottom_design()

button_1.when_pressed = add_voter
button_2.when_pressed = vote
button_3.when_pressed = erase
button_result.when_pressed = result
pause()
