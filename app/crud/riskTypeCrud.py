from app import db
from flask import session
from app.masterData.models import riskType
import uuid as UUID
from datetime import datetime

def getRiskTypes():
    return riskType.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getRiskType(uuid):
    return riskType.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postRiskTyp(data):
    pass

def putRiskTyp(data, uuid):
    pass

def deleteRiskTyp(uuid):
    pass

def riskTypSelectData():
    pass

def riskTypListData():
    pass
