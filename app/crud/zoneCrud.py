from app import db
from flask import session
from app.masterData.models import zone
import countryCrud
import uuid as UUID
from datetime import datetime

def getZones():
    return zone.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getZone(uuid):
    return zone.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postZone(data):
    c = countryCrud.getCountry(data['country'])
    if c == None:
        country_uuid = None
    else:
        country_uuid = c.uuid
    z = zone(title = data['title'],
             abbr = data['abbr'],
             tenant_uuid = session['tenant_uuid'],
             uuid = UUID.uuid4(),
             created=datetime.now(),
             createdBy=session['user_uuid'],
             country_uuid=country_uuid,
             country=c)

    try:
        db.session.add(c)
        db.session.commit()
        return {'success': 'Zone added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Zone already exist'}
        else:
            return {'error': unicode(E)}

def putZone(data, uuid):
    z = getZone(uuid)
    c = countryCrud.getCountry(data['country'])
    if c == None:
        country_uuid = None
    else:
        country_uuid = c.uuid

    z.title = data['title']
    z.abbr = data['abbr']
    z.modified = datetime.now()
    z.modifiedBy = session['user_uuid']
    z.country = c
    z.country_uuid = country_uuid

    try:
        db.session.commit()
        return {'success': 'Zone updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Zone already exist'}
        else:
            return {'error': unicode(E)}

def deleteZone(uuid):
    z = getZone(uuid)
    try:
        db.session.delete(z)
        db.session.commit()
        return {'success': 'Zone deleted'}
    except Exception as E:
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
