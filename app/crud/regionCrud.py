from app import db
from flask import session
from app.masterData.models import region, subRegion
import uuid as UUID

def getRegions():
    regions = region.query.filter_by(tenant_uuid=session['tenant_uuid']).all()
    return [[r.uuid, r.title, r.abbr, [s.title for s in r.subRegions]] for r in regions]

def getRegion(uuid):
    r = region.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()
    return [r.uuid, r.title, r.abbr, [s.title for s in r.subRegions]]

def postRegion(data):
    requiredData = ['title', 'abbr']
    if all(column in requiredData for column in data):
        row = region(title = data['title'],
                     abbr = data['abbr'],
                     tenant_uuid = session['tenant_uuid'],
                     uuid = UUID.uuid4())
        try:
            db.session.add(row)
            db.session.commit()
            return {'success': 'Region added'}
        except Exception as E:
            if 'unique constraint' in unicode(E):
                return {'error': 'Region already exist'}
            else:
                return {'error': unicode(E)}
    return {'error': 'bad request'}

def deleteRegion(uuid):
    r = region.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()
    print r
    try:
        db.session.delete(r)
        db.session.commit()
        return {'success': 'Region deleted'}
    except Exception as E:
        return {'error': unicode(E)}
