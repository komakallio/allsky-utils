#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import sys
import os

STATE_FILE = os.path.expandvars('$HOME/.iris')
DEGREES_TO_TURN = 200
EXTRA_STEPS_WHEN_OPENING = 1.2 # multiplier
PINS = [26, 16, 13, 12]
STEP_DELAY = 0.002
STEPS = [[1,0,0,1],
         [1,0,0,0],
         [1,1,0,0],
         [0,1,0,0],
         [0,1,1,0],
         [0,0,1,0],
         [0,0,1,1],
         [0,0,0,1]]

def cleanup():
	for pin in PINS:
		GPIO.output(pin, GPIO.LOW)
	GPIO.cleanup()

def move(direction, stepCount=4096):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	for pin in PINS:
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)

	stepIndex = 0
	for i in range(0, stepCount):
		for pin in range(0, len(PINS)):
			GPIO.output(PINS[pin], STEPS[stepIndex][pin])
		stepIndex = (stepIndex + direction) % 8
		time.sleep(STEP_DELAY)

def usageAndExit():
	print("usage: iriscontrol.py [open|close]")
	sys.exit(1)


def main(command):
	state = open(STATE_FILE, 'r').read().strip()

	if state == command:
		if __name__ == '__main__':
			print(f"Iris already in state {state}")
		return

	if command == 'close':
		direction = 1
		steps = int(DEGREES_TO_TURN/360*4096)
	elif command == 'open':
		direction = -1
		steps = int(DEGREES_TO_TURN/360*4096*EXTRA_STEPS_WHEN_OPENING)
	else:
		usageAndExit()

	try:
		move(direction, steps)
		open(STATE_FILE, 'w').write(command + '\n')
	except KeyboardInterrupt:
		pass
	cleanup()


if __name__ == '__main__':
	if len(sys.argv) != 2:
		usageAndExit()
	main(sys.argv[1])
