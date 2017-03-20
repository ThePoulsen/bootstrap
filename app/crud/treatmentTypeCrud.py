from app import db
from flask import session
from app.masterData.models import treatmentType
import uuid as UUID
from datetime import datetime

def getTreatmentTypes():
    return treatmentType.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getTreatmentType(uuid):
    return treatmentType.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()
