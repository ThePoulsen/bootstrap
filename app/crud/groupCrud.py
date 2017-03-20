from app import db
from flask import session
from app.user.models import group
import uuid as UUID
from datetime import datetime

def getGroups():
    return group.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getGroup(uuid):
    return group.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()
