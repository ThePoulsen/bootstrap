from app import db
from flask import session
from app.masterData.models import valueChainArea
import uuid as UUID
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getValueChainAreas():
    viewLog(table='valueChainArea')
    return valueChainArea.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getValueChainArea(uuid):
    viewLog(table='valueChainArea', uuid=unicode(uuid))
    return valueChainArea.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postValueChainArea(data):
    row = valueChainArea(title = data['title'],
                         desc = data['desc'],
                         tenant_uuid = session['tenant_uuid'],
                         uuid = UUID.uuid4(),
                         created=datetime.now(),
                         createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='valueChainArea', uuid=unicode(row.uuid))
        return {'success': 'Value Chain Area added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='valueChainArea')
            return {'error': 'Value Chain Area already exist'}
        else:
            errorLog(unicode(E), table='valueChainArea')
            return {'error': unicode(E)}

def putValueChainArea(data, uuid):
    row = getValueChainArea(uuid)
    changes = compareDict(row=row, data=data)['modified']
    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        putLog(table='valueChainArea', uuid=unicode(uuid), changes=changes)
        return {'success': 'Value Chain Area updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='valueChainArea')
            return {'error': 'Value Chain Area already exist'}
        else:
            errorLog(unicode(E), table='valueChainArea')
            return {'error': unicode(E)}

def deleteValueChainArea(uuid):
    entry = getValueChainArea(uuid)
    if entry.valueChains:
        errorLog('Delete attempt without removing Value Chains', table='valueChainArea')
        return {'error': 'Value Chain Area cannot be deleted as long as there are Value Chains assigned this Value Chain Area'}
    try:
        db.session.delete(entry)
        db.session.commit()
        deleteLog(table='valueChainArea', uuid=unicode(uuid))
        return {'success': 'Value Chain Area deleted'}
    except Exception as E:
        errorLog(unicode(E), table='valueChainArea')
        return {'error': unicode(E)}

def valueChainAreaSelectData():
    data = getValueChainAreas()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def valueChainAreaListData():
    entries = getValueChainAreas()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
