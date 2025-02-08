# # # import json
# # # from google_apis import create_service

# # # client_secret = 'client_secret.json'

# # # def construct_google_calendar_client(client_secret):
# # #     API_NAME = 'calendar'
# # #     API_VERSION = 'v3'
# # #     SCOPES = ['https://www.googleapis.com/auth/calendar']
# # #     service = create_service(client_secret, API_NAME, API_VERSION, SCOPES)
# # #     return service

# # # calendar_service = construct_google_calendar_client(client_secret)

# # # def create_calendar_list(calendar_name):
# # #     calendar = {
# # #         'summary': calendar_name
# # #     }
# # #     created_calendar_list = calendar_service.calendars().insert(body=calendar).execute()
# # #     return created_calendar_list

# # # def list_calendar_list(max_capacity=200):
# # #     if isinstance(max_capacity, str):
# # #         max_capacity = int(max_capacity)

# # #     all_calendars = []
# # #     all_calendars_cleaned = []
# # #     next_page_token = None
# # #     capacity_tracker = 0

# # #     while True:
# # #         calendar_list = calendar_service.calendarList().list(
# # #             maxResults = min(200, max_capacity - capacity_tracker),
# # #             pageToken = next_page_token
# # #         ).execute()
# # #         calendars = calendar_list.get('items', [])
# # #         all_calendars.extend(calendars)
# # #         capacity_tracker+=len(calendars)
# # #         if capacity_tracker >= max_capacity:
# # #             break
# # #         next_page_token = calendar_list.get('nextPageToken')
# # #         if not next_page_token:
# # #             break

# # #     for calendar in all_calendars:
# # #         all_calendars_cleaned.append(
# # #             {
# # #                 'id': calendar['id'],
# # #                 "name": calendar['summary'],
# # #                 "description": calendar.get('description', '')
# # #             })
# # #     return all_calendars_cleaned    


# # # def list_calendar_events(calendar_id='primary', max_capacity=200):
# # #     if isinstance(max_capacity, str):
# # #         max_capacity = int(max_capacity)

# # #     all_events = []
# # #     next_page_token = None
# # #     capacity_tracker = 0

# # #     while True:
# # #         events_list = calendar_service.events().list(
# # #             calendarId = calendar_id,
# # #             maxResults = min(200, max_capacity - capacity_tracker),
# # #             pageToken = next_page_token
# # #         ).execute()
# # #         events = events_list.get('items', [])
# # #         all_events.extend(events)
# # #         capacity_tracker+=len(events)
# # #         if capacity_tracker >= max_capacity:
# # #             break
# # #         next_page_token = events.get('nextPageToken')
# # #         if not next_page_token:
# # #             break
# # #     return all_events

# # # def insert_calendar_event(calendar_id, **kwargs):
# # #     request_body = json.loads(kwargs['kwargs'])
# # #     event = calendar_service.events().insert(
# # #         calendarId=calendar_id, 
# # #         body=request_body
# # #         ).execute()
# # #     return event

# # import json
# # from google_apis import create_service

# # client_secret = 'client_secret.json'

# # # Initialize Google Calendar API service
# # def construct_google_calendar_client(client_secret):
# #     API_NAME = 'calendar'
# #     API_VERSION = 'v3'
# #     SCOPES = ['https://www.googleapis.com/auth/calendar']
# #     service = create_service(client_secret, API_NAME, API_VERSION, SCOPES)
# #     return service

# # calendar_service = construct_google_calendar_client(client_secret)

# # # ✅ List all events from a specific calendar
# # def list_calendar_events(calendar_id='primary', max_capacity=200):
# #     """
# #     Retrieve a list of events from a specific Google Calendar.
# #     """
# #     try:
# #         if isinstance(max_capacity, str):
# #             max_capacity = int(max_capacity)

# #         all_events = []
# #         next_page_token = None
# #         capacity_tracker = 0

# #         while True:
# #             events_list = calendar_service.events().list(
# #                 calendarId=calendar_id,
# #                 maxResults=min(200, max_capacity - capacity_tracker),
# #                 pageToken=next_page_token
# #             ).execute()

# #             events = events_list.get('items', [])
# #             all_events.extend(events)
# #             capacity_tracker += len(events)

# #             if capacity_tracker >= max_capacity:
# #                 break

# #             next_page_token = events_list.get('nextPageToken')
# #             if not next_page_token:
# #                 break

# #         return all_events

# #     except Exception as e:
# #         print(f"Error retrieving events: {str(e)}")
# #         return {"error": f"Failed to retrieve events: {str(e)}"}

# # # ✅ Insert a new event
# # def insert_calendar_event(calendar_id, **kwargs):
# #     """
# #     Insert a new event into a Google Calendar.
# #     """
# #     try:
# #         # Ensure kwargs is properly extracted
# #         if 'kwargs' in kwargs:
# #             event_data = kwargs['kwargs']
# #             if isinstance(event_data, str):
# #                 event_data = json.loads(event_data)  # Convert JSON string to dict
# #         else:
# #             return {"error": "Missing event details"}

# #         # Set Indian timezone (Asia/Kolkata) if not provided
# #         if 'start' in event_data and 'timeZone' not in event_data['start']:
# #             event_data['start']['timeZone'] = 'Asia/Kolkata'
# #         if 'end' in event_data and 'timeZone' not in event_data['end']:
# #             event_data['end']['timeZone'] = 'Asia/Kolkata'

# #         # Debugging: Print event data before inserting
# #         print("Event Data to Insert:", json.dumps(event_data, indent=2))

# #         # Insert event
# #         event = calendar_service.events().insert(
# #             calendarId=calendar_id,
# #             body=event_data
# #         ).execute()

# #         print("Event Created Successfully:", event)
# #         return event

# #     except Exception as e:
# #         print(f"Error inserting event: {str(e)}")
# #         return {"error": f"Failed to insert event: {str(e)}"}

# # # ✅ Update an existing event
# # def update_calendar_event(calendar_id, event_id, **kwargs):
# #     """
# #     Update an existing event in Google Calendar.
# #     """
# #     try:
# #         # Fetch the existing event details
# #         event = calendar_service.events().get(calendarId=calendar_id, eventId=event_id).execute()

# #         # Ensure kwargs is properly extracted
# #         if 'kwargs' in kwargs:
# #             update_data = kwargs['kwargs']
# #             if isinstance(update_data, str):
# #                 update_data = json.loads(update_data)  # Convert JSON string to dict
# #         else:
# #             return {"error": "Missing update details"}

# #         # Merge updates with existing event data
# #         event.update(update_data)

# #         # Set Indian timezone (Asia/Kolkata) if not provided
# #         if 'start' in event and 'timeZone' not in event['start']:
# #             event['start']['timeZone'] = 'Asia/Kolkata'
# #         if 'end' in event and 'timeZone' not in event['end']:
# #             event['end']['timeZone'] = 'Asia/Kolkata'

# #         # Debugging: Print updated event data before modifying
# #         print("Updated Event Data:", json.dumps(event, indent=2))

# #         # Update event in Google Calendar
# #         updated_event = calendar_service.events().update(
# #             calendarId=calendar_id,
# #             eventId=event_id,
# #             body=event
# #         ).execute()

# #         print("Event Updated Successfully:", updated_event)
# #         return updated_event

# #     except Exception as e:
# #         print(f"Error updating event: {str(e)}")
# #         return {"error": f"Failed to update event: {str(e)}"}


# import json
# from google_apis import create_service

# client_secret = 'client_secret.json'

# def construct_google_calendar_client(client_secret):
#     API_NAME = 'calendar'
#     API_VERSION = 'v3'
#     SCOPES = ['https://www.googleapis.com/auth/calendar']
#     return create_service(client_secret, API_NAME, API_VERSION, SCOPES)

# calendar_service = construct_google_calendar_client(client_secret)

# def list_calendar_list(max_capacity=50):
#     all_calendars = []
#     next_page_token = None

#     while True:
#         calendar_list = calendar_service.calendarList().list(maxResults=max_capacity, pageToken=next_page_token).execute()
#         all_calendars.extend(calendar_list.get('items', []))
#         next_page_token = calendar_list.get('nextPageToken')
#         if not next_page_token or len(all_calendars) >= max_capacity:
#             break

#     return [{"id": c['id'], "name": c['summary']} for c in all_calendars]

# def list_calendar_events(calendar_id='primary', max_capacity=50):
#     all_events = []
#     next_page_token = None

#     while True:
#         events_list = calendar_service.events().list(calendarId=calendar_id, maxResults=max_capacity, pageToken=next_page_token).execute()
#         all_events.extend(events_list.get('items', []))
#         next_page_token = events_list.get('nextPageToken')
#         if not next_page_token or len(all_events) >= max_capacity:
#             break

#     return all_events

# def insert_calendar_event(calendar_id, event_details):
#     event_details['start']['timeZone'] = 'Asia/Kolkata'
#     event_details['end']['timeZone'] = 'Asia/Kolkata'
#     event = calendar_service.events().insert(calendarId=calendar_id, body=event_details).execute()
#     return event

# def update_calendar_event(calendar_id, event_id, updated_details):
#     updated_details['start']['timeZone'] = 'Asia/Kolkata'
#     updated_details['end']['timeZone'] = 'Asia/Kolkata'
#     event = calendar_service.events().update(calendarId=calendar_id, eventId=event_id, body=updated_details).execute()
#     return event

# def delete_calendar_event(calendar_id, event_id):
#     calendar_service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
#     return {"status": "Event deleted successfully"}


import json
from google_apis import create_service

client_secret = 'client_secret.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

calendar_service = create_service(client_secret, API_NAME, API_VERSION, SCOPES)

def list_calendar_list(max_capacity=50):
    all_calendars = []
    calendar_list = calendar_service.calendarList().list(maxResults=max_capacity).execute()
    for calendar in calendar_list.get('items', []):
        all_calendars.append({'id': calendar['id'], 'name': calendar['summary']})
    return all_calendars

def list_calendar_events(calendar_id='primary', max_capacity=50):
    events = calendar_service.events().list(calendarId=calendar_id, maxResults=max_capacity).execute()
    return events.get('items', [])

def construct_google_calendar_client(client_secret):
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    service = create_service(client_secret, API_NAME, API_VERSION, SCOPES)
    return service

calendar_service = construct_google_calendar_client(client_secret)

def insert_calendar_event(calendar_id, **kwargs):
    try:
        # Ensure kwargs are parsed correctly
        if isinstance(kwargs.get('kwargs'), str):
            request_body = json.loads(kwargs['kwargs'])
        else:
            request_body = kwargs.get('kwargs', {})

        # Ensure 'start' and 'end' exist
        if 'start' not in request_body:
            request_body['start'] = {}
        if 'end' not in request_body:
            request_body['end'] = {}

        # Set the default timezone to 'Asia/Kolkata'
        request_body['start'].setdefault('timeZone', 'Asia/Kolkata')
        request_body['end'].setdefault('timeZone', 'Asia/Kolkata')

        # Ensure required fields exist
        if 'dateTime' not in request_body['start']:
            raise ValueError("Missing 'start.dateTime' in event details.")
        if 'dateTime' not in request_body['end']:
            raise ValueError("Missing 'end.dateTime' in event details.")

        # Insert event into Google Calendar
        event = calendar_service.events().insert(
            calendarId=calendar_id,
            body=request_body
        ).execute()

        return event
    except Exception as e:
        return {"error": str(e)}

def update_calendar_event(calendar_id, event_id, **kwargs):
    try:
        # Ensure kwargs are parsed correctly
        if isinstance(kwargs.get('kwargs'), str):
            request_body = json.loads(kwargs['kwargs'])
        else:
            request_body = kwargs.get('kwargs', {})

        # Retrieve the existing event
        existing_event = calendar_service.events().get(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()

        # Merge the existing event details with the new ones
        updated_event = {**existing_event, **request_body}

        # Ensure 'start' and 'end' exist
        if 'start' not in updated_event:
            updated_event['start'] = {}
        if 'end' not in updated_event:
            updated_event['end'] = {}

        # Set the timezone to 'Asia/Kolkata'
        updated_event['start'].setdefault('timeZone', 'Asia/Kolkata')
        updated_event['end'].setdefault('timeZone', 'Asia/Kolkata')

        # Ensure required fields exist
        if 'dateTime' not in updated_event['start']:
            raise ValueError("Missing 'start.dateTime' in event details.")
        if 'dateTime' not in updated_event['end']:
            raise ValueError("Missing 'end.dateTime' in event details.")

        # Update the event in Google Calendar
        event = calendar_service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=updated_event
        ).execute()

        return event
    except Exception as e:
        return {"error": str(e)}


def delete_calendar_event(calendar_id, event_id):
    calendar_service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
    return f"Event {event_id} deleted successfully."
