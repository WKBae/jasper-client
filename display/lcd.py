# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import requests
import bs4
import lcd_i2c as LCD

from display import Display

class LcdDisplay(Display):
	grades = ['', 'Good', 'Normal', 'Bad', 'Worse']

	def __init__(self, config):
		if 'lcd_address' in config:
			LCD.I2C_ADDR = int(config['lcd_address'])
		LCD.lcd_init()

		self.key = config['keys']['DUST_API'] # KaN7MvIVm%2Bz29aS4YWJlPSZZ1mWJ42n8RZq3K0UL0jFDk3m%2FCofalymRMjl4c%2B4NdweiRiAN0rRemtHt33IWAw%3D%3D
		self.location = config['dust_location'] # 명륜동

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

		LCD.lcd_string('PM10 %s:%s' % (pm10Value, grades[int(pm10Grade1h)]), LCD.LCD_LINE_1)
		LCD.lcd_string('PM25 %s:%s' % (pm25Value, grades[int(pm25Grade1h)]), LCD.LCD_LINE_2)
