from app import db
from flask import session
from app.masterData.models import subRegion
import regionCrud
import uuid as UUID
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getSubRegions():
    viewLog(table='subRegion')
    return subRegion.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getSubRegion(uuid):
    viewLog(table='subRegion', uuid=unicode(uuid))
    return subRegion.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postSubRegion(data):
    r = regionCrud.getRegion(data['region'])
    row = subRegion(title = data['title'],
                    abbr = data['abbr'],
                    tenant_uuid = session['tenant_uuid'],
                    uuid = UUID.uuid4(),
                    created=datetime.now(),
                    createdBy=session['user_uuid'],
                    region_uuid=r.uuid,
                    region=r)

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='subRegion', uuid=unicode(row.uuid))
        return {'success': 'Sub Region added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='subRegion')
            return {'error': 'Sub Region already exist'}
        else:
            errorLog(unicode(E), table='subRegion')
            return {'error': unicode(E)}

def putSubRegion(data, uuid):
    row = getSubRegion(uuid)
    reg = regionCrud.getRegion(data['region'])
    changes = compareDict(row=row, data=data)['modified']
    if reg != row.region:
        changes['region'] = (row.region.uuid,r.uuid)

    row.title = data['title']
    row.abbr = data['abbr']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']
    row.region = reg
    row.region_uuid = reg.uuid

    try:
        db.session.commit()
        putLog(table='subRegion', uuid=unicode(uuid), changes=changes)
        return {'success': 'Sub Region updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='subRegion')
            return {'error': 'Sub Region already exist'}
        else:
            errorLog(unicode(E), table='subRegion')
            return {'error': unicode(E)}

def deleteSubRegion(uuid):
    row = getSubRegion(uuid)
    if not row.countries:
        try:
            db.session.delete(row)
            db.session.commit()
            deleteLog(table='subRegion', uuid=unicode(uuid))
            return {'success': 'Region deleted'}
        except Exception as E:
            errorLog(unicode(E), table='subRegion')
            return {'error': unicode(E)}
    else:
        errorLog('Delete attempt without removing Countries', table='subRegion')
        return {'error': 'You must first remove countries from Sub Region'}

def subRegionSelectData():
    subRegions = getSubRegions()
    dataList = []
    for sr in subRegions:
        dataList.append((sr.uuid, sr.title))
    return dataList

def subRegionListData():
    subRegions = getSubRegions()
    data = []
    for sr in subRegions:
        temp = [sr.uuid, sr.title, sr.abbr, sr.region.abbr if sr.region else ""]
        data.append(temp)
    return data
