# -*- coding: utf-8 -*-
import schedule
import time
import re

WORDS = [u"알람", u"추가"]


def get_weekdays(line):
    if bool(re.search(ur'\b월요일\b', line, re.IGNORECASE | re.UNICODE)):
        return schedule.every().monday
        
    if bool(re.search(ur'\b화요일\b', line, re.IGNORECASE | re.UNICODE)):
        return schedule.every().tuesday
        
    if bool(re.search(ur'\b수요일\b', line, re.IGNORECASE | re.UNICODE)):
        return schedule.every().wednesday
        
    if bool(re.search(ur'\b목요일\b', line, re.IGNORECASE | re.UNICODE)):
        return schedule.every().thursday
        
    if bool(re.search(ur'\b금요일\b', line, re.IGNORECASE | re.UNICODE)):
        return schedule.every().friday
        
    if bool(re.search(ur'\b토요일\b', line, re.IGNORECASE | re.UNICODE)):
        return schedule.every().saturday
        
    if bool(re.search(ur'\b일요일\b', line, re.IGNORECASE | re.UNICODE)):
        return schedule.every().sunday

    return schedule.every().days


def get_time(line): 
    #24시 기준인지? 아니면 오전 오후있는지? 없으면 오전으로 간주
    hourMatch = re.search(ur'([0-9]+)시', line, re.IGNORECASE | re.UNICODE)
    minuteMatch = re.search(ur'([0-9]+)분', line, re.IGNORECASE | re.UNICODE)
    if hourMatch == None:
        # TODO 몇시인지 말하라고 추궁
        print("[ALARM] no hour")
    else:
        hour = int(hourMatch.group(1))
        if minuteMatch != None:
            minute = int(minuteMatch.group(1))
        else:
            minute = 0

        if hour > 12:
            return "%02d:%02d" % (hour,minute)
        else:
            if bool(re.search(ur'\b오전\b', line, re.IGNORECASE | re.UNICODE)):
                return "%02d:%02d" % (hour,minute)
            else:
                return "%02d:%02d" % (hour+12,minute)


def handle(text, mic, profile):
    mic.say("언제 알람을 추가하시겠습니까?")
    line = mic.activeListen()
    weekdays = get_weekdays(line)

    def job():
        mic.speaker.play(jasperpath.data('audio', 'beep_lo.wav'))

    weekdays.at(get_time(line)).do(job)
    mic.say("알람이 추가되었습니다.")


def isValid(text):
    return bool(re.search(ur'\b알람을? 추가해?\b', text, re.IGNORECASE | re.UNICODE))
