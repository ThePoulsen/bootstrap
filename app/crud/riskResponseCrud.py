from app import db
from flask import session
from app.masterData.models import riskResponse
import uuid as UUID
from datetime import datetime

def getRiskResponses():
    return riskResponse.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getRiskResponse(uuid):
    return riskResponse.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postRiskResponse(data):
    pass

def putRiskResponse(data, uuid):
    pass

def deleteRiskResponse(uuid):
    pass

def riskResponseSelectData():
    pass

def riskResponseListData():
    pass
