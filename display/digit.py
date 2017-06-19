# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import spidev
import time

from display import Display

class DigitDisplay(Display):

	digit = [0b1110111, 0b0100100, 0b1101011, 0b1101101, 0b0111100,
		0b1011101, 0b1011111, 0b1100100, 0b1111111, 0b1111100]

	def __init__(self, config):
		if 'digit_latch' in config:
			self.latch = int(config['digit_latch'])
		else:
			self.latch = 22

		if 'digit_spi' in config:
			self.spi_device = int(config['digit_spi'])
		else:
			self.spi_device = 0

		spi = spidev.SpiDev()
		spi.open(0, self.spi_device)
		#spi.lsbfirst = True

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.latch, GPIO.OUT)
		GPIO.output(self.latch, False)

		self.dot_shown = False
		self.update()

	def write_time(self, hours, minutes, dot_top, dot_bottom):
	    h1 = hours / 10 % 10
	    h2 = hours % 10
	    m1 = minutes / 10 % 10
	    m2 = minutes % 10

	    bytes = [digit[m2], digit[m1], digit[h2], digit[h1]]
	    if dot_top:
	        bytes[1] |= 0b10000000
	    if dot_bottom:
	        bytes[2] |= 0b10000000

	    spi.writebytes(bytes)
	    GPIO.output(self.latch, True)
	    time.sleep(0.00005)
	    GPIO.output(self.latch, False)

	def period(self):
		return 1

	def update(self):
	    now = time.localtime()
	    self.dot_shown = not self.dot_shown
	    write_time(now.tm_hour, now.tm_min, dot_shown, dot_shown)

