from app import db
from flask import session
from app.masterData.models import likelihood
import uuid as UUID
from datetime import datetime

def getLikelihoods():
    return likelihood.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getLikelihood(uuid):
    return likelihood.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postLikelihood(data):
    row = likelihood(title = data['title'],
                     desc = data['desc'],
                     value = data['value'],
                     tenant_uuid = session['tenant_uuid'],
                     uuid = UUID.uuid4(),
                     created=datetime.now(),
                     createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        return {'success': 'Likelihood added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Likelihood already exist'}
        else:
            return {'error': unicode(E)}

def putLikelihood(data, uuid):
    row = getLikelihood(uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.value = data['value']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        return {'success': 'Likelihood updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Likelihood already exist'}
        else:
            return {'error': unicode(E)}

def deleteLikelihood(uuid):
    entry = getLikelihood(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        return {'success': 'Likelihood deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def likelihoodSelectData():
    data = getLikelihoods()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def likelihoodListData():
    entries = getLikelihoods()
    data = []
    for r in entries:
        temp = [r.uuid, r.value, r.title, r.desc]
        data.append(temp)
    return data
