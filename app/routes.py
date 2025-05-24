from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Dict, List
from app.models import EmergencyContact, SOSRequest, SOSEvent
from app.auth import get_current_user
from app.utils import success_response,error_response

router = APIRouter()

user_contacts: Dict[str, List[EmergencyContact]] = {}
sos_logs: Dict[str, List[Dict]] = {}

@router.post("/contacts")
def add_contact(contact: EmergencyContact, username: str = Depends(get_current_user)):
    if username not in user_contacts:
        user_contacts[username] = []
    user_contacts[username].append(contact)
    return success_response("Contact Added")

@router.get("/contacts", response_model=List[EmergencyContact])
def get_contacts(username: str = Depends(get_current_user)):
    return user_contacts.get(username, [])

@router.post("/sos")
def send_sos(sos: SOSRequest, username: str = Depends(get_current_user)):
    event = {
        "message": sos.message,
        "timestamp": datetime.utcnow().isoformat()
    }
    if username not in sos_logs:
        sos_logs[username] = []
    sos_logs[username].append(event)

    alerts = []
    for contact in user_contacts.get(username, []):
        alert = {
            "to": contact.name,
            "phone": contact.phone,
            "relationship": contact.relationship,
            "alert_message": f"ALERT! {username} triggered an SOS: '{sos.message}'"
        }
        print(f"Dispatching alert: {alert}")
        alerts.append(alert)

    return {
        "message": "SOS sent",
        "sos_event": event,
        "dispatched_alerts": alerts
    }

@router.get("/sos", response_model=List[SOSEvent])
def get_sos_logs(username: str = Depends(get_current_user)):
    return sos_logs.get(username, [])
