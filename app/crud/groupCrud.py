from app import db
from flask import session
from app.user.models import group
import uuid as UUID
from datetime import datetime

def getGroups():
    return group.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getGroup(uuid):
    return group.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def groupSelectData():
    data = getGroups()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def groupListData():
    data = getGroups()
    output = []
    for r in data:
        temp = [r.uuid, r.name, r.email, r.role, '', r.locked, r.contact, r.active, r.confirmed]
        output.append(temp)
    return output
