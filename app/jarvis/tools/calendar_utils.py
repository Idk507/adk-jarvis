import json 
import os 
from datetime import datetime
from pathlib import Path 

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

#scops needed for the calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_PATH = Path(os.path.expanduser("~/.credentials/calendar_token.json"))
CREDENTIALS_PATH = Path("credentials.json")


def get_calendar_Service():
    cred = None 
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_info(
            json.loads(TOKEN_PATH.read_text()), SCOPES
        )
    if not creds  or not creds.valid : 
        if creds and creds.expired and creds.refresh_token : 
            creds.refresh((Request()))
        else : 
            if not CREDENTIALS_PATH.exists() :
                raise FileNotFoundError(
                    f"Credentials file not found at {CREDENTIALS_PATH}"
                )
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_PATH.write_text(creds.to_json())
    return build("calendar", "v3", credentials=creds)

def format_event_time(event_time):
    if "dateTime" in event_time:
        return datetime.fromisoformat(event_time["dateTime"]).strftime("%Y-%m-%d %H:%M:%S")
    elif "date" in event_time:
        return datetime.fromisoformat(event_time["date"]).strftime("%Y-%m-%d")
    else:
        return "Unknown"


def parse_datetime(datetime_str):
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %I:%M %p",
        "%Y-%m-%d",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y %I:%M %p",
        "%m/%d/%Y",
        "%B %d, %Y %H:%M",
        "%B %d, %Y %I:%M %p",
        "%B %d, %Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue

    return None

def get_current_time() ->  dict :
    now = datetime.now()

    formatted_date = now.strftime("%m-%d-%Y")

    return {
        "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "formatted_date": formatted_date,
    }