from app import db
from flask import session
from app.masterData.models import processArea
import uuid as UUID
from datetime import datetime

def getProcessAreas():
    return processArea.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getProcessArea(uuid):
    return processArea.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postProcessArea(data):
    pass

def putProcessArea(data, uuid):
    pass

def deleteProcessArea(uuid):
    pass

def processAreaSelectData():
    pass

def processAreaListData():
    pass
