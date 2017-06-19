# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

from display import Display

class WeatherDisplay(Display):
	Sun = (0, 0, 0)
	Cloud = (0, 0, 0)
	Rain = (0, 0, 0)
	Snow = (0, 0, 0)

	def __init__(self, config):
		if 'weather' in config:
			weather = config['weather']
			sun = weather['sun']
			self.sun_pin = (sun.r, sun.g, sun.b)
			cloud = weather['cloud']
			self.cloud_pin = (cloud.r, cloud.g, cloud.b)
			rain = weather['rain']
			self.rain_pin = (rain.r, rain.g, rain.b)
			snow = weather['snow']
			self.snow_pin = (snow.r, snow.g, snow.b)
		else:
			self.sun_pin = (17, 18, 27)
			self.cloud_pin = (23, 24, 25)
			self.rain_pin = (5, 6, 12)
			self.snow_pin = (13, 19, 16)

		GPIO.setmode(GPIO.BCM)
		elems = ['sun', 'cloud', 'rain', 'snow']

		def setup_pin(pin):
			GPIO.setup(pin, GPIO.OUT)
			p = GPIO.PWM(pin, 60)
			p.start(0)
			return p

		for elem in elems:
			setattr(self, elem, tuple(map(setup_pin, getattr(self, elem + "_pin"))))
		
	def period(self):
		return 1

	@staticmethod
	def _update_rate(targets, cycles):
		for i in range(0, 3):
			targets[i].ChangeDutyCycle(cycles[i] * 100 / 255)

	def update(self):
		if Sun != self._lastSun:
			_update_rate(self.sun, Sun)
			self._lastSun = Sun
		
		if Cloud != self._lastCloud:
			_update_rate(self.cloud, Cloud)
			self._lastCloud = Cloud
		
		if Rain != self._lastRain:
			_update_rate(self.rain, Rain)
			self._lastRain = Rain
		
		if Snow != self._lastSnow:
			_update_rate(self.snow, Snow)
			self._lastSnow = Snow
	
