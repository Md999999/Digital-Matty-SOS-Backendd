from pydantic import BaseModel

class EmergencyContact(BaseModel):
    name: str
    phone: str
    relationship: str

class SOSRequest(BaseModel):
    message: str

class SOSEvent(BaseModel):
    message: str
    timestamp: str
