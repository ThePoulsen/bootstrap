from app import db
from flask import session
from app.masterData.models import subRegion
import regionCrud
import uuid as UUID
from datetime import datetime

def getSubRegions():
    return subRegion.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getSubRegion(uuid):
    return subRegion.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postSubRegion(data):
    r = regionCrud.getRegion(data['region'])
    row = subRegion(title = data['title'],
                    abbr = data['abbr'],
                    tenant_uuid = session['tenant_uuid'],
                    uuid = UUID.uuid4(),
                    created=datetime.now(),
                    createdBy=session['user_uuid'],
                    region_id=r.id,
                    region=r)

    try:
        db.session.add(row)
        db.session.commit()
        return {'success': 'Sub Region added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Sub Region already exist'}
        else:
            return {'error': unicode(E)}

def putSubRegion(data, uuid):
    r = getSubRegion(uuid)
    reg = regionCrud.getRegion(data['region'])

    r.title = data['title']
    r.abbr = data['abbr']
    r.modified = datetime.now()
    r.modifiedBy = session['user_uuid']
    r.region = reg
    r.region_id = reg.id

    try:
        db.session.commit()
        return {'success': 'Sub Region updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Sub Region already exist'}
        else:
            return {'error': unicode(E)}

def deleteSubRegion(uuid):
    r = getSubRegion(uuid)
    try:
        db.session.delete(r)
        db.session.commit()
        return {'success': 'Region deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def subRegionSelectData():
    subRegions = getSubRegions()
    dataList = [] #[(0,'')]
    for sr in subRegions:
        dataList.append((sr.uuid, sr.title))
    return dataList

def subRegionListData():
    subRegions = getSubRegions()
    data = []
    for sr in subRegions:
        temp = [sr.uuid, sr.title, sr.abbr, sr.region.abbr]
        data.append(temp)
    return data
