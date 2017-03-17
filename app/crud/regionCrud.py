from app import db
from flask import session
from app.masterData.models import region, subRegion
import uuid as UUID
from datetime import datetime

def getRegions():
    return region.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getRegion(uuid):
    return region.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postRegion(data):
    row = region(title = data['title'],
                 abbr = data['abbr'],
                 tenant_uuid = session['tenant_uuid'],
                 uuid = UUID.uuid4(),
                 created=datetime.now(),
                 createdBy=session['user_uuid'])
    if data['subRegions']:
        for sr in data['subRegions']:
            row.subRegions.append(subRegion.query.filter_by(uuid=unicode(sr)).first())

    try:
        db.session.add(row)
        db.session.commit()
        return {'success': 'Region added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Region already exist'}
        else:
            return {'error': unicode(E)}

def putRegion(data, uuid):
    r = region.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

    r.title = data['title']
    r.title = data['abbr']
    r.modified = datetime.now()
    r.modifiedBy = session['user_uuid']

    if data['subRegions']:
        for sr in data['subRegions']:
            r.subRegions.append(subRegion.query.filter_by(uuid=unicode(sr)).first())
    else:
        r.subRegions[:] = []

    try:
        db.session.commit()
        return {'success': 'Region updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Region already exist'}
        else:
            return {'error': unicode(E)}

def deleteRegion(uuid):
    r = region.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()
    try:
        db.session.delete(r)
        db.session.commit()
        return {'success': 'Region deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def regionSelectData():
    regions = region.query.filter_by(tenant_uuid=session['tenant_uuid']).all()
    dataList = []
    for r in regions:
        dataList.append((r.uuid, r.title))
    return dataList

def regionListData():
    regions = getRegions()
    data = []
    for r in regions:
        temp = [r.uuid, r.title, r.abbr, [sr.abbr for sr in r.subRegions]]
        data.append(temp)
    return data
