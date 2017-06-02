# -*- coding: utf-8 -*-
import schedule
import jasperpath
import re
import datetime
from client.app_utils import getTimezone
from semantic.dates import DateService



WORDS = [u"타이머"]

def get_time(line, profile):
    tz = getTimezone(profile)
    now = datetime.datetime.now(tz=tz)

    hourMatch = re.search(ur'([0-9]+)시간', line, re.IGNORECASE | re.UNICODE)
    minuteMatch = re.search(ur'([0-9]+)분', line, re.IGNORECASE | re.UNICODE)
    
    if hourMatch == None:
        if minuteMatch != None:
            minute = int(minuteMatch.group(1))
            timer = now + datetime.timedelta(minutes=minute)
        else:
            minute = 0
            timer = now
    else:
        hour = int(hourMatch.group(1))
        if minuteMatch != None:
            minute = int(minuteMatch.group(1))
            timer = now + datetime.timedelta(hours=hour, minutes=minute)
        else:
            minute = 0
            timer = now + datetime.timedelta(hours=hour)
        
    return timer


def handle(text, mic, profile):
    mic.say("타이머를 추가하시겠습니까?")
    line = mic.activeListen()
    time = get_time(line, profile)
   
    def job():
        mic.speaker.play(jasperpath.data('audio', 'beep_lo.wav'))

    schedule.every().days.at("%02d:%02d" % (time.hour, time.minute)).do(job)
    service = DateService()
    response = service.convertTime(time)

    mic.say("%s 타이머가 추가되었습니다." % response)

def isValid(text):
    return bool(re.search(ur'\b타이머를? 추가해?\b', text, re.IGNORECASE | re.UNICODE))