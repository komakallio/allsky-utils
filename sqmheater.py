#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import sys

PIN = 21

def usageAndExit():
	print("usage: sqmheater.py [on|off]")
	sys.exit(1)


if __name__ == '__main__':
	if len(sys.argv) != 2:
		usageAndExit()

	if sys.argv[1] == 'on':
		state = GPIO.HIGH
	elif sys.argv[1] == 'off':
		state = GPIO.LOW
	else:
		usageAndExit()

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(PIN, GPIO.OUT)
	GPIO.output(PIN, state)
