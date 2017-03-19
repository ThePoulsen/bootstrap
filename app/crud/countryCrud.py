from app import db
from flask import session
from app.masterData.models import country
import subRegionCrud
import uuid as UUID
from datetime import datetime

def getCountries():
    return country.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getCountry(uuid):
    return country.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postCountry(data):
    r = subRegionCrud.getSubRegion(data['subRegion'])
    if r == None:
        subRegion_id = None
    else:
        subRegion_id = r.id
    c = country(title = data['title'],
                abbr = data['abbr'],
                tenant_uuid = session['tenant_uuid'],
                uuid = UUID.uuid4(),
                created=datetime.now(),
                createdBy=session['user_uuid'],
                subRegion_id=subRegion_id,
                subRegion=r)

    try:
        db.session.add(c)
        db.session.commit()
        return {'success': 'Country added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Country already exist'}
        else:
            return {'error': unicode(E)}

def putCountry(data, uuid):
    c = getCountry(uuid)
    sr = subRegionCrud.getSubRegion(data['subRegion'])
    if sr == None:
        subRegion_id = None
    else:
        subRegion_id = sr.id

    c.title = data['title']
    c.abbr = data['abbr']
    c.modified = datetime.now()
    c.modifiedBy = session['user_uuid']
    c.subRegion = sr
    c.subRegion_id = subRegion_id

    try:
        db.session.commit()
        return {'success': 'Country updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Country already exist'}
        else:
            return {'error': unicode(E)}

def deleteCountry(uuid):
    c = getCountry(uuid)
    if not c.zones:
        try:
            db.session.delete(c)
            db.session.commit()
            return {'success': 'Country deleted'}
        except Exception as E:
            return {'error': unicode(E)}
    else:
        return {'error': 'You must first remove zones from Sub Region'}

def countrySelectData():
    countries = getCountries()
    dataList = [] #[(0,'Select Country')]
    for sr in countries:
        dataList.append((sr.uuid, sr.title))
    return dataList

def countryListData():
    countries = getCountries()
    data = []
    for c in countries:
        temp = [c.uuid, c.title, c.abbr, c.subRegion.abbr if c.subRegion else '']
        data.append(temp)
    return data
