## -*- coding: utf-8 -*-

from app import db
from flask import session
from app.valueChain.models import valueChain
import uuid as UUID
from datetime import datetime
from app.crud import valueChainAreaCrud
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getValueChains():
    viewLog(table='valueChain')
    return valueChain.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getValueChain(uuid):
    viewLog(table='valueChain', uuid=unicode(uuid))
    return valueChain.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postValueChain(data):
    r = valueChainAreaCrud.getValueChainArea(data['valueChainArea'])
    row = valueChain(title = data['title'],
                        desc = data['desc'],
                        tenant_uuid = session['tenant_uuid'],
                        uuid = UUID.uuid4(),
                        valueChainArea_uuid=r.uuid,
                        valueChainArea=r,
                        created=datetime.now(),
                        createdBy=session['user_uuid'])

    try:
        postLog(table='valueChain', uuid=unicode(row.uuid))
        db.session.add(row)
        db.session.commit()
        return {'success': 'Value Chain added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='valueChain')
            return {'error': 'Value Chain already exist'}
        else:
            errorLog(unicode(E), table='valueChain')
            return {'error': unicode(E)}

def putValueChain(data, uuid):
    row = getValueChain(uuid)
    r = valueChainAreaCrud.getValueChainArea(data['valueChainArea'])

    changes = compareDict(row=row, data=data)['modified']
    if r != row.valueChainArea:
        changes['valueChainArea'] = (row.valueChainArea.uuid,r.uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']
    row.valueChainArea_uuid = r.uuid
    row.valueChainArea = r

    try:
        db.session.commit()
        putLog(table='valueChain', uuid=unicode(uuid), changes=changes)
        return {'success': 'Value Chain updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='valueChain')
            return {'error': 'Value Chain already exist'}
        else:
            errorLog(unicode(E), table='valueChain')
            return {'error': unicode(E)}

def deleteValueChain(uuid):
    row = getValueChain(uuid)
    try:
        db.session.delete(row)
        db.session.commit()
        deleteLog(table='valueChain', uuid=unicode(uuid))
        return {'success': 'Value Chain deleted'}
    except Exception as E:
        errorLog(unicode(E), table='valueChain')
        return {'error': unicode(E)}

def valueChainSelectData():
    data = getValueChains()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def valueChainListData():
    entries = getValueChains()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc, r.valueChainArea.title]
        data.append(temp)
    return data
