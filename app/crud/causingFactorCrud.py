from app import db
from flask import session
from app.masterData.models import causingFactor
import uuid as UUID
from datetime import datetime

def getCausingFactors():
    return causingFactor.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getCausingFactor(uuid):
    return causingFactor.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postCausingFactor(data):
    pass

def putCausingFactor(data, uuid):
    pass

def deleteCausingFactor(uuid):
    pass

def causingFactorSelectData():
    pass

def causingFactorListData():
    pass
