from app import db
from flask import session
from models import rating
import uuid as UUID
from datetime import datetime
from app.crud import impactCrud, probabilityCrud
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getRatings():
    viewLog(table='rating')
    return rating.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getRating(uuid):
    viewLog(table='rating', uuid=unicode(uuid))
    return rating.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postRating(data):
    i = impactCrud.getImpact(data['impact'])
    p = probabilityCrud.getProbability(data['probability'])
    row = rating(value = data['value'],
                 desc = data['desc'],
                 tenant_uuid = session['tenant_uuid'],
                 uuid = UUID.uuid4(),
                 impact_uuid=i.uuid,
                 impact=i,
                 probability_uuid=p.uuid,
                 probability=p,
                 created=datetime.now(),
                 createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='rating', uuid=unicode(row.uuid))
        return {'success': 'Rating added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='rating')
            return {'error': 'Rating already exist'}
        else:
            errorLog(unicode(E), table='rating')
            return {'error': unicode(E)}

def putRating(data, uuid):
    row = getRating(uuid)
    i = impactCrud.getImpact(data['impact'])
    p = probabilityCrud.getProbability(data['probability'])

    changes = compareDict(row=row, data=data)['modified']
    if i != row.impact:
        changes['impact'] = (row.impact.uuid,i.uuid)
    if p != row.probability:
        changes['probability'] = (row.probability.uuid,p.uuid)

    row.value = data['value']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']
    row.impact_uuid = i.uuid
    row.impact = i
    row.probability_uuid = p.uuid
    row.probability = p

    try:
        db.session.commit()
        putLog(table='rating', uuid=unicode(uuid), changes=changes)
        return {'success': 'Rating updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='rating')
            return {'error': 'Rating already exist'}
        else:
            errorLog(unicode(E), table='rating')
            return {'error': unicode(E)}

def deleteRating(uuid):
    row = getRating(uuid)
    try:
        db.session.delete(row)
        db.session.commit()
        deleteLog(table='rating', uuid=unicode(uuid))
        return {'success': 'Rating deleted'}
    except Exception as E:
        errorLog(unicode(E), table='rating')
        return {'error': unicode(E)}

def ratingSelectData():
    data = getRatings()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.value))
    return dataList

def ratingListData():
    entries = getRatings()
    data = []
    for r in entries:
        temp = [r.uuid, r.value, r.desc, r.impact.value, r.probability.value]
        data.append(temp)
    return data
