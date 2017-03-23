## -*- coding: utf-8 -*-

from app import db
from flask import session
from app.valueChain.models import valueChain
import uuid as UUID
from datetime import datetime
from app.crud import valueChainAreaCrud

def getValueChains():
    return valueChain.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getValueChain(uuid):
    return valueChain.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postValueChain(data):
    r = valueChainAreaCrud.getValueChainArea(data['valueChainArea'])
    if r == None:
        valueChainArea_uuid = None
    else:
        valueChainArea_uuid = r.uuid

    row = valueChain(title = data['title'],
                        desc = data['desc'],
                        tenant_uuid = session['tenant_uuid'],
                        uuid = UUID.uuid4(),
                        valueChainArea_uuid=valueChainArea_uuid,
                        valueChainArea=r,
                        created=datetime.now(),
                        createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        return {'success': 'Value Chain added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Value Chain already exist'}
        else:
            return {'error': unicode(E)}

def putValueChain(data, uuid):
    r = valueChainAreaCrud.getValueChainArea(data['valueChainArea'])
    if r == None:
        valueChainArea_uuid = None
    else:
        valueChainArea_uuid = r.uuid

    row = getValueChain(uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']
    row.valueChainArea_uuid = valueChainArea_uuid
    row.valueChainArea = r

    try:
        db.session.commit()
        return {'success': 'Value Chain updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Value Chain already exist'}
        else:
            return {'error': unicode(E)}

def deleteValueChain(uuid):
    entry = getValueChain(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        return {'success': 'Value Chain deleted'}
    except Exception as E:
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
