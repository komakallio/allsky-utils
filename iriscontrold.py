#!/usr/bin/env python3

import subprocess, os, json, datetime, iriscontrol, time, logging, sys

logging.basicConfig(format='[%(asctime)s] %(message)s', stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

HELIOCRON = os.path.expandvars("$HOME/.cargo/bin/heliocron")
CHECK_INTERVAL_SECONDS = 60

was_daytime = None

def is_daytime():
	heliocron_json = subprocess.run([HELIOCRON, 'report', '--json'], stdout=subprocess.PIPE).stdout
	data = json.loads(heliocron_json)

	now = datetime.datetime.now().astimezone()
	sunrise = datetime.datetime.fromisoformat(data['sunrise'])
	sunset = datetime.datetime.fromisoformat(data['sunset'])

	return now > sunrise and now < sunset

def loop():
	global was_daytime
	while True:
		is_day = is_daytime()
		name = 'day' if is_day else 'night'
		command = 'close' if is_day else 'open'
		if is_day != was_daytime:
			logger.info(f'State changed to {name}, adjusting iris -> {command}')
		iriscontrol.main(command)
		was_daytime = is_day
		time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == '__main__':
	loop()
