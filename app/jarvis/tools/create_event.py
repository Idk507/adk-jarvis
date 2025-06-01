import datetime 
from .calender_utils import get_calender_service, parse_datetime


def create_event(
    summary : str,
    start_time : str,
    end_time : str,) -> dict:
    try :
        service = get_calender_service()
        if not service:
            return {
                "status": "error",
                "message" : "Failed to get calendar service. Check your credentials."
            }

        calendar_id = "primary"  # Use the primary calendar
        
        #parse times 
        start_dt = parse_datetime(start_time)
        end_dt = parse_datetime(end_time)

        if not start_dt or not end_dt:
            return {
                "status": "error",
                "message" : "Invalid date format. Use YYYY-MM-DD HH:MM:SS format."
            }

        #dynamcally determine timezone 
        timezone_id = "Asia/Kolkata"  # Default timezone 

        try : 
            settings = service.settings().list().execute()
            for setting in settings.get("items", []):
                if setting.get("id") == "timezone":
                    timezone_id = setting.get("value")
                    break
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to retrieve timezone settings: {str(e)}"
            }

        #event body
        event_body = {}

        #add start and end time 
        event_body["start"] = {
            "dateTime": start_dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": timezone_id,
        
        } 
        event_body["end"] = {
            "dateTime": end_dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": timezone_id,
        }

        event = (
            service.events()
            .insert(calendarId=calendar_id, body=event_body)
            .execute()
        
        )

        return  {
            "status": "success",
            "message": "Event created successfully.",
            "event_id": event.get("id"),
            "event_link": event.get("htmlLink"),
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }
