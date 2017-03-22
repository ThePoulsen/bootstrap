from app import db
from flask import session
from app.masterData.models import valueChainStepType
import uuid as UUID
from datetime import datetime

def getValueChainStepTypes():
    return valueChainStepType.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getValueChainStepType(uuid):
    return valueChainStepType.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postValueChainStepType(data):
    row = valueChainStepType(title = data['title'],
                         desc = data['desc'],
                         tenant_uuid = session['tenant_uuid'],
                         uuid = UUID.uuid4(),
                         created=datetime.now(),
                         createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        return {'success': 'Value Chain Step Type added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Value Chain Step Type already exist'}
        else:
            return {'error': unicode(E)}

def putValueChainStepType(data, uuid):
    row = getValueChainStepType(uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        return {'success': 'Value Chain Step Type updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Value Chain Step Type already exist'}
        else:
            return {'error': unicode(E)}

def deleteValueChainStepType(uuid):
    entry = getValueChainStepType(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        return {'success': 'Value Chain Step Type deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def valueChainStepTypeSelectData():
    data = getValueChainStepTypes()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def valueChainStepTypeListData():
    entries = getValueChainStepTypes()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
