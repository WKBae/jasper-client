# -*- coding: utf-8 -*-

import time
import re

WORDS = [u"타이머"]

def get_time(line):
    hourMatch = re.search(ur'([0-9]+)시', line, re.IGNORECASE | re.UNICODE)
    minuteMatch = re.search(ur'([0-9]+)분', line, re.IGNORECASE | re.UNICODE)
    
    if hourMatch == None:
        if minuteMatch != None:
            minute = int(minuteMatch.group(1))
        else:
            minute = 0
    else:
        hour = int(hourMatch.group(1))
        if minuteMatch != None:
            minute = int(minuteMatch.group(1))
        else:
            minute = 0


def handle(text, mic, profile):
    mic.say("타이머를 추가하시겠습니까?")
    line = mic.activeListen()
    get_time(line)
    mic.say("알람이 추가되었습니다.")

def isValid(text):
    return bool(re.search(ur'([0-9]+시|[0-9]+분)', text, re.IGNORECASE | re.UNICODE))
