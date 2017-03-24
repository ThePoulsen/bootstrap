## -*- coding: utf-8 -*-

from app import db
from flask import session
from app.masterData.models import deliveryPoint
import uuid as UUID
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getDeliveryPoints():
    viewLog(table='deliveryPoint')
    return deliveryPoint.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getDeliveryPoint(uuid):
    viewLog(table='deliveryPoint', uuid=unicode(uuid))
    return deliveryPoint.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postDeliveryPoint(data):
    row = deliveryPoint(title = data['title'],
                         desc = data['desc'],
                         tenant_uuid = session['tenant_uuid'],
                         uuid = UUID.uuid4(),
                         created=datetime.now(),
                         createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='deliveryPoint', uuid=unicode(row.uuid))
        return {'success': 'Delivery Point added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Delivery Point already exist'}
        else:
            return {'error': unicode(E)}

def putDeliveryPoint(data, uuid):
    row = getDeliveryPoint(uuid)
    changes = compareDict(row=row, data=data)['modified']

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        putLog(table='deliveryPoint', uuid=unicode(uuid), changes=changes)
        return {'success': 'Delivery Point updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Delivery Point already exist'}
        else:
            return {'error': unicode(E)}

def deleteDeliveryPoint(uuid):
    entry = getDeliveryPoint(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        deleteLog(table='deliveryPoint', uuid=unicode(uuid))
        return {'success': 'Delivery Point deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def deliveryPointSelectData():
    rows = getDeliveryPoints()
    dataList = []
    for r in rows:
        dataList.append((r.uuid, r.title))
    return dataList

def deliveryPointListData():
    rows = getDeliveryPoints()
    data = []
    for r in rows:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
