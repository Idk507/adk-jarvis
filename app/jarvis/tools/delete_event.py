from .calendar_utils import get_calendar_service, parse_datetime

def delete_event(event_id,confirm : bool) -> dict :
    if not confirm:
        return {"status": "error",
            "message": "Event not deleted"}
    try : 
        service = get_calendar_service()
        if not service :
            return {
                "status": "error",
                "message": "Failed to get calendar service. Check your credentials."
            }
        calendar_id = "primary"  # Use the primary calendar
        # Delete the event
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        return {
            "status" : "success",
            "message" : f"event {event_id} deleted successfully.",
            "event_id": event_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error deleting event: {str(e)}"
        }
        