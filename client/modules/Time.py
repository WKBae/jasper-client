import datetime
import re
from client.app_utils import getTimezone
from semantic.dates import DateService

WORDS = ["몇시"]


def handle(text, mic, profile):

    tz = getTimezone(profile)
    now = datetime.datetime.now(tz=tz)
    service = DateService()
    response = service.convertTime(now)
    mic.say("현재 시간은 %s입니다." % response)


def isValid(text):

    return bool(re.search(r'\btime\b', text, re.IGNORECASE))
