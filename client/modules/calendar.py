# -*- coding: utf-8 -*-

import httplib2
import sys
import datetime
import re
import gflags

from client.app_utils import getTimezone
from dateutil import tz
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import *

FLAGS = gflags.FLAGS
WORDS = [ u"일정" ]

clinet_id = '816217761407-ffqnt48rm4latmloq9tlb4gq7ftqfjk5.apps.googleusercontent.com'
client_secret = 'JOJ_qz6w3IH9okpG10DTWA0u'

monthDict = {'1월': '01', 
		'2월': '02', 
		'3월': '03', 
		'4월': '04', 
		'5월': '05', 
		'6월': '06', 
		'7월': '07', 
		'8월': '08', 
		'9월': '09', 
		'10월': '10', 
		'11월': '11', 
	    '12월': '12'}

scope = 'https://www.googleapis.com/auth/calendar'

def addEvent(profile, mic):

	while True:
		try:
			mic.say("언제 일정을 추가하고 싶습니까?")
			eventData = mic.activeListen()
			createdEvent = service.events().quickAdd(calendarId='primary', text=eventData).execute()
			eventRawStartTime = createdEvent['start']
			
			m = re.search('([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})', str(eventRawStartTime))
			eventDateYear = str(m.group(1))
			eventDateMonth = str(m.group(2))
			eventDateDay = str(m.group(3))
			eventTimeHour = str(m.group(4))
			eventTimeMinute =  str(m.group(5))
			appendingTime = "오전"

			if len(eventTimeMinute) == 1:
				eventTimeMinute = eventTimeMinute + "0"

			eventTimeHour = int(eventTimeHour)

			if ((eventTimeHour - 12) > 0 ):
					eventTimeHour = eventTimeHour - 12
					appendingTime = "오후"
		
			dictKeys = [ key for key, val in monthDict.items() if val==eventDateMonth ]
			eventDateMonth = dictKeys[0]
			mic.say(createdEvent['summary'] + str(eventDateMonth) + " " + str(eventDateDay) + appendingTime + str(eventTimeHour) + ":" + str(eventTimeMinute) + " 일정 추가")
			mic.say("이 일정을 추가하시겠습니까?")
			userResponse = mic.activeListen()
			
			if bool(re.search('예', userResponse, re.IGNORECASE)):
				mic.say("추가 되었습니다")
				return
	
			service.events().delete(calendarId='primary', eventId=createdEvent['id']).execute()

		except KeyError:

			mic.say("일정을 추가 할 수 없습니다. 인터넷 연결을 확인해주십시오.")
			mic.say("다시 시도 하시겠니까?")
			responseRedo = mic.activeListen()

			if bool(re.search('아니오', responseRedo, re.IGNORECASE)):
				return


def getEventsToday(profile, mic):

	tz = getTimezone(profile)

	d = datetime.datetime.now(tz=tz)
	utcString = d.isoformat()	
	m = re.search('((\+|\-)[0-9]{2}\:[0-9]{2})', str(utcString))
	utcString = str(m.group(0))
	todayStartTime = str(d.strftime("%Y-%m-%d")) + "T00:00:00" + utcString
	todayEndTime = str(d.strftime("%Y-%m-%d")) + "T23:59:59" + utcString
	page_token = None
	
	while True:

		events = service.events().list(calendarId='primary', pageToken=page_token, timeMin=todayStartTime, timeMax=todayEndTime).execute() 
		
		if(len(events['items']) == 0):
			mic.say("오늘 일정은 없습니다.")
			return

		for event in events['items']:

			try:
				eventTitle = event['summary']
				eventTitle = str(eventTitle)
				eventRawStartTime = event['start']
				eventRawStartTime = eventRawStartTime['dateTime'].split("T")
				temp = eventRawStartTime[1]
				startHour, startMinute, temp = temp.split(":", 2)
				startHour = int(startHour)
				appendingTime = "오전"

				if ((startHour - 12) > 0 ):
					startHour = startHour - 12
					appendingTime = "오후"

				startMinute = str(startMinute)
				startHour = str(startHour)
				mic.say(eventTitle + appendingTime + startHour + ":" + startMinute + " ")
			except KeyError, e:
				mic.say("바르게 일정이 추가 되었는지 확인하십시오")
			
		page_token = events.get('nextPageToken')

		if not page_token:
			return

def getEventsTomorrow(profile, mic):

	
	one_day = datetime.timedelta(days=1)
	tz = getTimezone(profile)
	
	d = datetime.datetime.now(tz=tz) + one_day
	utcString = d.isoformat()
	m = re.search('((\+|\-)[0-9]{2}\:[0-9]{2})', str(utcString))
	utcString = m.group(0)
	tomorrowStartTime = str(d.strftime("%Y-%m-%d")) + "T00:00:00" + utcString
	tomorrowEndTime = str(d.strftime("%Y-%m-%d")) + "T23:59:59" + utcString

	page_token = None

	while True:

		
		events = service.events().list(calendarId='primary', pageToken=page_token, timeMin=tomorrowStartTime, timeMax=tomorrowEndTime).execute()
		if(len(events['items']) == 0):
			mic.say("내일 일정은 없습니다.")
			return
	
		for event in events['items']:
			
			try:
				eventTitle = event['summary']
				eventTitle = str(eventTitle)
				eventRawStartTime = event['start']
				eventRawStartTime = eventRawStartTime['dateTime'].split("T")
				temp = eventRawStartTime[1]
				startHour, startMinute, temp = temp.split(":", 2)
				startHour = int(startHour)
				appendingTime = "오전"

				if ((startHour - 12) > 0 ):
					startHour = startHour - 12
					appendingTime = "오후"

				startMinute = str(startMinute)
				startHour = str(startHour)
				mic.say(eventTitle + appendingTime +startHour + ":" + startMinute + " ")

			except KeyError, e:
				mic.say("바르게 일정이 추가 되었는지 확인하십시오")
			
		page_token = events.get('nextPageToken')
		
		if not page_token:
			return


flow = OAuth2WebServerFlow(client_id, client_secret, scope)
storage = Storage('credentials.dat')
credentials = storage.get()

if credentials is None or credentials.invalid:
	credentials = run_flow(flow, storage)


http = httplib2.Http()
http = credentials.authorize(http)
service = build('calendar', 'v3', http=http)


def handle(text, mic, profile):
		
	if bool(re.search('추가', text, re.IGNORECASE)):
		addEvent(profile,mic)

	if bool(re.search('오늘', text, re.IGNORECASE)):
		getEventsToday(profile,mic)

	if bool(re.search('내일', text, re.IGNORECASE)):
		getEventsTomorrow(profile,mic)


def isValid(text):
	return bool(re.search(r'\b일정\b', text, re.IGNORECASE))