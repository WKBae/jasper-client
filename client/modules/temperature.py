# -*- coding: utf-8 -*-

import os
import glob
import time
import re


WORDS = [u"온도"]

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '10*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
	

def handle(text, mic, profile):
    mic.say("주변 온도는 %.1f도입니다." % read_temp()[0])

def isValid(text):
    return bool(re.search(ur'\b(주변|집 ?안|방 ?안) 온도[을를]?\b', text, re.IGNORECASE | re.UNICODE))