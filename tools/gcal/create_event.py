#!/usr/bin/env python3

from datetime import datetime, timedelta
from cal_setup import get_calendar_service


def main():
	service = get_calendar_service()

	d = datetime.now().date()
	tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
	start = tomorrow.isoformat()
	end = (tomorrow + timedelta(hours=1)).isoformat()

	event_result = service.events().insert(calendarId='vaoa144p5ftjje4tsqlrjvhr74@group.calendar.google.com',
		body={
			"summary": input("Titolo: "),
			"description": input("Descrizione: "),
			"start": {"dateTime": start, "timeZone": 'Europe/Rome'},
			"end": {"dateTime": end, "timeZone": 'Europe/Rome'},
			}
		).execute()

	print("created event")
	print("id: ", event_result['id'])
	print("summary: ", event_result['summary'])
	print("starts at: ", event_result['start']['dateTime'])
	print("ends at: ", event_result['end']['dateTime'])

if __name__ == '__main__':
	main()
