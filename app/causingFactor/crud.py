from app import db
from flask import session
from app.causingFactor.models import causingFactor
import uuid as UUID
from datetime import datetime
from app.crud import causingFactorTypeCrud
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getCausingFactors():
    viewLog(table='causingFactor')
    return causingFactor.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getCausingFactor(uuid):
    viewLog(table='causingFactor', uuid=unicode(uuid))
    return causingFactor.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postCausingFactor(data):
    c = causingFactorTypeCrud.getCausingFactorType(data['causingFactorType'])
    row = causingFactor(title = data['title'],
                        desc = data['desc'],
                        tenant_uuid = session['tenant_uuid'],
                        uuid = UUID.uuid4(),
                        causingFactorType_uuid=c.uuid,
                        causingFactorType=c,
                        created=datetime.now(),
                        createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='causingFactor', uuid=unicode(row.uuid))
        return {'success': 'Causing Factor added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='causingFactor')
            return {'error': 'Causing Factor already exist'}
        else:
            errorLog(unicode(E), table='causingFactor')
            return {'error': unicode(E)}

def putCausingFactor(data, uuid):
    row = getCausingFactor(uuid)
    c = causingFactorTypeCrud.getCausingFactorType(data['causingFactorType'])

    changes = compareDict(row=row, data=data)['modified']
    if c != row.causingFactorType:
        changes['causingFactorType'] = (row.causingFactorType.uuid,c.uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']
    row.causingFactorType_uuid = c.uuid
    row.causingFactorType = c

    try:
        db.session.commit()
        putLog(table='causingFactor', uuid=unicode(uuid), changes=changes)
        return {'success': 'Causing Factor updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='causingFactor')
            return {'error': 'Causing Factor already exist'}
        else:
            errorLog(unicode(E), table='causingFactor')
            return {'error': unicode(E)}

def deleteCausingFactor(uuid):
    row = getCausingFactor(uuid)
    try:
        db.session.delete(row)
        db.session.commit()
        deleteLog(table='causingFactor', uuid=unicode(uuid))
        return {'success': 'Causing Factor deleted'}
    except Exception as E:
        errorLog(unicode(E), table='causingFactor')
        return {'error': unicode(E)}

def causingFactorSelectData():
    data = getCausingFactors()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def causingFactorListData():
    entries = getCausingFactors()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc, r.causingFactorType.title]
        data.append(temp)
    return data
