from app import db
from flask import session
from app.masterData.models import severity
import uuid as UUID
from datetime import datetime

def getSeverities():
    return severity.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getSeverity(uuid):
    return severity.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postSeverity(data):
    pass

def putSeverity(data, uuid):
    pass

def deleteSeverity(uuid):
    pass

def severitySelectData():
    pass

def severityListData():
    pass
