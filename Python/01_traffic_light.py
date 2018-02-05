#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

dictColor = {
	'red': 0xFF00, 
	'green': 0x00FF, 
	'yellow': 0x0FFF,
	'black': 0x0000}

pins = (11, 12)  # pins is a dict

GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
GPIO.setup(pins, GPIO.OUT)     # Set pins' mode is output
GPIO.output(pins, GPIO.LOW)    # Set pins to LOW(0V) to off led

p_R = GPIO.PWM(pins[0], 2000)  # set Frequece to 2KHz
p_G = GPIO.PWM(pins[1], 2000)

p_R.start(0)      # Initial duty Cycle = 0(leds off)
p_G.start(0)

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(col):   # For example : col = 0x1122
	R_val = col  >> 8
	G_val = col & 0x00FF
	
	R_val = map(R_val, 0, 255, 0, 100)
	G_val = map(G_val, 0, 255, 0, 100)
	# print('R: ', R_val)
	# print('G: ', G_val)
	p_R.ChangeDutyCycle(R_val)     # Change duty cycle
	p_G.ChangeDutyCycle(G_val)

def flashColor(col, count):
	print("Flash {} {} times".format(col, count))
	for i in range(1, count+1):
		setColor(dictColor[col])
		time.sleep(0.5)
		setColor(dictColor['black'])
		time.sleep(0.2)
	return

def displayColor(col, seconds):
	print("Display {} for {} seconds".format(col, seconds))
	setColor(dictColor[col])
	time.sleep(seconds)
	return

def loop():
	while True:
		displayColor('green', 3)
		flashColor('yellow', 3)
		displayColor('red', 3)

def destroy():
	p_R.stop()
	p_G.stop()
	GPIO.output(pins, GPIO.LOW)    # Turn off all leds
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
