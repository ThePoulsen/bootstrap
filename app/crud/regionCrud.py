from app import db
from flask import session
from app.masterData.models import region
import uuid as UUID
from datetime import datetime
import subRegionCrud
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getRegions():
    viewLog(table='region')
    return region.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getRegion(uuid):
    viewLog(table='region', uuid=unicode(uuid))
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
            row.subRegions.append(subRegionCrud.getSubRegion(unicode(sr)))

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='region', uuid=unicode(row.uuid))
        return {'success': 'Region added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='region')
            return {'error': 'Region already exist'}
        else:
            errorLog(unicode(E), table='region')
            return {'error': unicode(E)}

def putRegion(data, uuid):
    row = getRegion(uuid)
    changes = compareDict(row=row, data=data)['modified']
    row.title = data['title']
    row.abbr = data['abbr']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    if data['subRegions']:
        for sr in data['subRegions']:
            row.subRegions.append(subRegionCrud.getSubRegion(unicode(sr)))
    else:
        row.subRegions[:] = []

    if data['subRegions'] != row.subRegions[:]:
        changes['subRegions'] = (row.subRegions.uuid,r.uuid)

    try:
        db.session.commit()
        putLog(table='region', uuid=unicode(uuid), changes=changes)
        return {'success': 'Region updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='region')
            return {'error': 'Region already exist'}
        else:
            errorLog(unicode(E), table='region')
            return {'error': unicode(E)}

def deleteRegion(uuid):
    row = getRegion(uuid)
    if not row.subRegions:
        try:
            db.session.delete(row)
            db.session.commit()
            deleteLog(table='region', uuid=unicode(uuid))
            return {'success': 'Region deleted'}
        except Exception as E:
            errorLog(unicode(E), table='region')
            return {'error': unicode(E)}
    else:
        errorLog('Delete attempt without removing Sub Regions', table='region')
        return {'error': 'You must first remove Sub Regions from Region'}

def regionSelectData():
    regions = region.query.filter_by(tenant_uuid=session['tenant_uuid']).all()
    dataList = [] #[(0,'Select Region')]
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
