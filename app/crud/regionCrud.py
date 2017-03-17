from app import db
from flask import session
from app.masterData.models import region

def getRegions():
    regions = region.query.filter_by(tenant_uuid=session['tenant_uuid'])
    return [[r.id, r.title, r.abbr] for r in regions]

def getRegion(id):
    r = region.query.filter_by(id=id, tenant_uuid=session['tenant_uuid'])
    return [r.id, r.title, r.abbr]

def postRegion(data):
    requiredData = ['title', 'abbr']
    if all(column in requiredData for column in data):
        row = region(title = data['title'],
                     abbr = data['abbr'],
                     tenant_uuid = session['tenant_uuid'])
        try:
            db.session.add(row)
            db.session.commit()
            return {'success': 'row added'}
        except Exception as E:
            if 'unique constraint' in unicode(E):
                return {'error': 'Region already exist'}
            else:
                return {'error': unicode(E)}
    return {'error': 'bad request'}
