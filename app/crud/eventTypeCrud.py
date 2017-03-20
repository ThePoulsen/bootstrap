from app import db
from flask import session
from app.masterData.models import eventType
import uuid as UUID
from datetime import datetime

def getsEventType():
    return eventType.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getEventType(uuid):
    return eventType.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postEventType(data):
    pass

def putEventType(data, uuid):
    pass

def deleteEventType(uuid):
    pass

def eventTypeSelectData():
    pass

def eventTypeListData():
    pass
