from app import db
from flask import session
from app.masterData.models import country
import subRegionCrud
import uuid as UUID
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getCountries():
    viewLog(table='country')
    return country.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getCountry(uuid):
    viewLog(table='country', uuid=unicode(uuid))
    return country.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postCountry(data):
    sr = subRegionCrud.getSubRegion(data['subRegion'])
    row = country(title = data['title'],
                abbr = data['abbr'],
                tenant_uuid = session['tenant_uuid'],
                uuid = UUID.uuid4(),
                created=datetime.now(),
                createdBy=session['user_uuid'],
                subRegion_uuid=sr.uuid,
                subRegion=sr)

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='country', uuid=unicode(row.uuid))
        return {'success': 'Country added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='country')
            return {'error': 'Country already exist'}
        else:
            errorLog(unicode(E), table='country')
            return {'error': unicode(E)}

def putCountry(data, uuid):
    row = getCountry(uuid)
    changes = compareDict(row=row, data=data)['modified']
    sr = subRegionCrud.getSubRegion(data['subRegion'])

    row.title = data['title']
    row.abbr = data['abbr']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']
    row.subRegion = sr
    row.subRegion_uuid = sr.uuid

    try:
        db.session.commit()
        putLog(table='country', uuid=unicode(uuid), changes=changes)
        return {'success': 'Country updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='country')
            return {'error': 'Country already exist'}
        else:
            errorLog(unicode(E), table='country')
            return {'error': unicode(E)}

def deleteCountry(uuid):
    row = getCountry(uuid)
    if not row.zones:
        try:
            db.session.delete(row)
            db.session.commit()
            deleteLog(table='country', uuid=unicode(uuid))
            return {'success': 'Country deleted'}
        except Exception as E:
            errorLog(unicode(E), table='country')
            return {'error': unicode(E)}
    else:
        return {'error': 'You must first remove zones from Sub Region'}

def countrySelectData():
    rows = getCountries()
    dataList = [] #[(0,'Select Country')]
    for c in rows:
        dataList.append((c.uuid, c.title))
    return dataList

def countryListData():
    rows = getCountries()
    data = []
    for c in rows:
        temp = [c.uuid, c.title, c.abbr, c.subRegion.abbr if c.subRegion else '']
        data.append(temp)
    return data
