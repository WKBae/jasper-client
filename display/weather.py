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

		def setup_pin(pin):
			GPIO.setup(pin, GPIO.OUT)
			p = GPIO.PWM(pin, 60)
			p.start(0)
			return p

		elems = ['sun', 'cloud', 'rain', 'snow']
		for elem in elems:
			setattr(self, elem, tuple(map(setup_pin, getattr(self, elem + "_pin"))))
		
		self._lastSun = None
		self._lastCloud = None
		self._lastRain = None
		self._lastSnow = None

	def period(self):
		return 1

	@staticmethod
	def _update_rate(targets, cycles):
		for i in range(0, 3):
			targets[i].ChangeDutyCycle(cycles[i] * 100 / 255)

	def update(self):
		if WeatherDisplay.Sun != self._lastSun:
			WeatherDisplay._update_rate(self.sun, WeatherDisplay.Sun)
			self._lastSun = WeatherDisplay.Sun
		
		if WeatherDisplay.Cloud != self._lastCloud:
			WeatherDisplay._update_rate(self.cloud, WeatherDisplay.Cloud)
			self._lastCloud = WeatherDisplay.Cloud
		
		if WeatherDisplay.Rain != self._lastRain:
			WeatherDisplay._update_rate(self.rain, WeatherDisplay.Rain)
			self._lastRain = WeatherDisplay.Rain
		
		if WeatherDisplay.Snow != self._lastSnow:
			WeatherDisplay._update_rate(self.snow, WeatherDisplay.Snow)
			self._lastSnow = WeatherDisplay.Snow
