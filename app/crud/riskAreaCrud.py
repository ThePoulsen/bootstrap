from app import db
from flask import session
from app.masterData.models import riskArea
import uuid as UUID
from datetime import datetime

def getRiskAreas():
    return riskArea.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getRiskArea(uuid):
    return riskArea.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postRiskArea(data):
    pass

def putRiskArea(data, uuid):
    pass

def deleteRiskArea(uuid):
    pass

def riskAreaSelectData():
    pass

def riskAreaListData():
    pass
