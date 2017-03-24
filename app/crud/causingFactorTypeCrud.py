from app import db
from flask import session
from app.masterData.models import causingFactorType
import uuid as UUID
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getCausingFactorTypes():
    viewLog(table='causingFactor')
    return causingFactorType.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getCausingFactorType(uuid):
    viewLog(table='causingFactor', uuid=unicode(uuid))
    return causingFactorType.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postCausingFactorType(data):
    row = causingFactorType(title = data['title'],
                        desc = data['desc'],
                        tenant_uuid = session['tenant_uuid'],
                        uuid = UUID.uuid4(),
                        created=datetime.now(),
                        createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='causingFactor', uuid=unicode(row.uuid))
        return {'success': 'Causing Factor Type added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='causingFactor')
            return {'error': 'Causing Factor Type already exist'}
        else:
            errorLog(unicode(E), table='causingFactor')
            return {'error': unicode(E)}

def putCausingFactorType(data, uuid):
    row = getCausingFactorType(uuid)
    changes = compareDict(row=row, data=data)['modified']
    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        putLog(table='causingFactor', uuid=unicode(uuid), changes=changes)
        return {'success': 'Causing Factor Type updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='causingFactor')
            return {'error': 'Causing Factor Type already exist'}
        else:
            errorLog(unicode(E), table='causingFactor')
            return {'error': unicode(E)}

def deleteCausingFactorType(uuid):
    entry = getCausingFactorType(uuid)
    if not entry.causingFactors:
        try:
            db.session.delete(entry)
            db.session.commit()
            deleteLog(table='causingFactor', uuid=unicode(uuid))
            return {'success': 'Causing Factor Type deleted'}
        except Exception as E:
            errorLog(unicode(E), table='causingFactor')
            return {'error': unicode(E)}
    else:
        return {'error': 'Cannot be deleted as there are Causing Factors assigned this Type'}

def causingFactorTypeSelectData():
    data = getCausingFactorTypes()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def causingFactorTypeListData():
    entries = getCausingFactorTypes()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
