import RPi.GPIO as GPIO
import httplib2
import sys
import datetime
import re
import gflags
import bs4
from Adafruit_CharLCD import Adafruit_CharLCD

http = httplib2.Http()
key = 'KaN7MvIVm%2Bz29aS4YWJlPSZZ1mWJ42n8RZq3K0UL0jFDk3m%2FCofalymRMjl4c%2B4NdweiRiAN0rRemtHt33IWAw%3D%3D'
response, content = http.request('http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?stationName=%s&dataTerm=month&pageNo=1&numOfRows=10&ServiceKey=%s&ver=1.3' % ('명륜동', key))

soup = bs4.BeautifulSoup(content)
pm10Value = soup.find('pm10value').string
pm25Value = soup.find('pm25value').string
pm10Grade1h = soup.find('pm10grade1h').string
pm25Grade1h = soup.find('pm25grade1h').string

lcd = Adafruit_CharLCD()

lcd.begin(16,1)

lcd.message('pm10 %s:%s' % (pm10Value, grades[int(pm10Grade1h)]))
grades = ['', 'Good', 'Normal', 'Bad', 'Worse']
lcd.message('pm25 %s:%s' % (pm25Value, grades[int(pm25Grade1h)]))


