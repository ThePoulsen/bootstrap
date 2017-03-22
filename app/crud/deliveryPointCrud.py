## -*- coding: utf-8 -*-

from app import db
from flask import session
from app.masterData.models import deliveryPoint
import uuid as UUID
from datetime import datetime

def getDeliveryPoints():
    return deliveryPoint.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getDeliveryPoint(uuid):
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
        return {'success': 'Delivery Point added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Delivery Point already exist'}
        else:
            return {'error': unicode(E)}

def putDeliveryPoint(data, uuid):
    row = getDeliveryPoint(uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
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
        return {'success': 'Delivery Point deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def deliveryPointSelectData():
    data = getDeliveryPoints()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def deliveryPointListData():
    entries = getDeliveryPoints()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
