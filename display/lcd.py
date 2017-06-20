# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import requests
import bs4
import _lcd_i2c as LCD

from display import Display

class LcdDisplay(Display):
	grades = ['', 'Good', 'Normal', 'Bad', 'Worse']

	def __init__(self, config):
		if 'lcd_address' in config:
			LCD.I2C_ADDR = int(config['lcd_address'])
		LCD.lcd_init()

		self.key = config['keys']['DUST_API'] # KaN7MvIVm%2Bz29aS4YWJlPSZZ1mWJ42n8RZq3K0UL0jFDk3m%2FCofalymRMjl4c%2B4NdweiRiAN0rRemtHt33IWAw%3D%3D
		self.location = "명륜동" # config['dust_location']

	def period(self):
		return 5 * 60 # update every 5 mins

	def update(self):
		r = requests.get('http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
			+ '?stationName=%s&dataTerm=month&pageNo=1&numOfRows=10&ServiceKey=%s&ver=1.3' % (self.location, self.key))

		soup = bs4.BeautifulSoup(r.text)
		pm10Value = soup.find('pm10value').string
		pm25Value = soup.find('pm25value').string
		pm10Grade1h = soup.find('pm10grade1h').string
		pm25Grade1h = soup.find('pm25grade1h').string

		if not pm10Value or not pm10Grade1h:
			LCD.lcd_string('PM10 - Error', LCD.LCD_LINE_1)
		else:
			LCD.lcd_string('PM10 %s:%s' % (pm10Value, LcdDisplay.grades[int(pm10Grade1h)]), LCD.LCD_LINE_1)
		if not pm25Value or not pm25Grade1h:
			LCD.lcd_string('PM25 - Error', LCD.LCD_LINE_2)
		else:
			LCD.lcd_string('PM25 %s:%s' % (pm25Value, LcdDisplay.grades[int(pm25Grade1h)]), LCD.LCD_LINE_2)
