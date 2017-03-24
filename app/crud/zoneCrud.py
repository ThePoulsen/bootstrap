from app import db
from flask import session
from app.masterData.models import zone
import countryCrud
import uuid as UUID
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getZones():
    viewLog(table='zone')
    return zone.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getZone(uuid):
    viewLog(table='zone', uuid=unicode(uuid))
    return zone.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postZone(data):
    c = countryCrud.getCountry(data['country'])
    z = zone(title = data['title'],
             abbr = data['abbr'],
             tenant_uuid = session['tenant_uuid'],
             uuid = UUID.uuid4(),
             created=datetime.now(),
             createdBy=session['user_uuid'],
             country_uuid=c.uuid,
             country=c)

    try:
        db.session.add(c)
        db.session.commit()
        postLog(table='zone', uuid=unicode(row.uuid))
        return {'success': 'Zone added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='zone')
            return {'error': 'Zone already exist'}
        else:
            errorLog(unicode(E), table='zone')
            return {'error': unicode(E)}

def putZone(data, uuid):
    row = getZone(uuid)
    c = countryCrud.getCountry(data['country'])

    changes = compareDict(row=row, data=data)['modified']
    if c != row.country:
        changes['country'] = (row.country.uuid,r.uuid)

    row.title = data['title']
    row.abbr = data['abbr']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']
    row.country = c
    row.country_uuid = c.uuid

    try:
        db.session.commit()
        putLog(table='zone', uuid=unicode(uuid), changes=changes)
        return {'success': 'Zone updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='zone')
            return {'error': 'Zone already exist'}
        else:
            errorLog(unicode(E), table='zone')
            return {'error': unicode(E)}

def deleteZone(uuid):
    row = getZone(uuid)
    try:
        db.session.delete(row)
        db.session.commit()
        deleteLog(table='zone', uuid=unicode(uuid))
        return {'success': 'Zone deleted'}
    except Exception as E:
        errorLog(unicode(E), table='zone')
        return {'error': unicode(E)}

def zoneSelectData():
    zones = getZones()
    dataList = []
    for z in zones:
        dataList.append((z.uuid, z.title))
    return dataList

def zoneListData():
    zones = getZones()
    data = []
    for z in zones:
        temp = [z.uuid, z.title, z.abbr, z.country.abbr if z.country else '']
        data.append(temp)
    return data
