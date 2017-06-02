# -*- coding: utf-8 -*-
import schedule
import jasperpath
import re
import datetime
from client.app_utils import getTimezone
from semantic.dates import DateService



WORDS = [u"타이머"]

def get_time(line):
    tz = getTimezone(profile)
    now = datetime.datetime.now(tz=tz)

    hourMatch = re.search(ur'([0-9]+)시간', line, re.IGNORECASE | re.UNICODE)
    minuteMatch = re.search(ur'([0-9]+)분', line, re.IGNORECASE | re.UNICODE)
    
    if hourMatch == None:
        if minuteMatch != None:
            minute = int(minuteMatch.group(1))
            timer = datetime.timedelta(minutes=minute)
        else:
            minute = 0
            timer = now
    else:
        hour = int(hourMatch.group(1))
        if minuteMatch != None:
            minute = int(minuteMatch.group(1))
            timer = datetime.timedelta(hours=hour, minutes=minute)
        else:
            minute = 0
            timer = datetime.timedelta(hours=hour)
        
    service = DateService()
    response = service.convertTime(timer)

    return response


def handle(text, mic, profile):
    mic.say("타이머를 추가하시겠습니까?")
    line = mic.activeListen()
    time = get_time(line)
   
    def job():
        mic.speaker.play(jasperpath.data('audio', 'beep_lo.wav'))

    schedule.every().days.at(time).do(job)
    mic.say("%s 타이머가 추가 되었습니다.")

def isValid(text):
    return bool(re.search(ur'(\b타이머를? 추가해?\b', text, re.IGNORECASE | re.UNICODE))