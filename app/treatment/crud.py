## -*- coding: utf-8 -*-

from app import db
from flask import session
from app.treatment.models import treatment
import uuid as UUID
from datetime import datetime
from app.crud import treatmentTypeCrud, riskResponseCrud
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getTreatments():
    viewLog(table='treatment')
    return treatment.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getTreatment(uuid):
    viewLog(table='treatment', uuid=unicode(uuid))
    return treatment.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postTreatment(data):
    t = treatmentTypeCrud.getTreatmentType(data['treatmentType'])
    r = riskResponseCrud.getRiskResponse(data['riskResponse'])

    row = treatment(title = data['title'],
                    desc = data['desc'],
                    tenant_uuid = session['tenant_uuid'],
                    uuid = UUID.uuid4(),
                    treatmentType_uuid=t.uuid,
                    treatmentType=t,
                    riskResponse_uuid=r.uuid,
                    riskResponse=r,
                    created=datetime.now(),
                    createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='treatment', uuid=unicode(row.uuid))
        return {'success': 'Treatment added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='treatment')
            return {'error': 'Treatment already exist'}
        else:
            errorLog(unicode(E), table='treatment')
            return {'error': unicode(E)}

def putTreatment(data, uuid):
    row = getTreatment(uuid)
    t = treatmentTypeCrud.getTreatmentType(data['treatmentType'])
    r = riskResponseCrud.getRiskResponse(data['riskResponse'])

    # Discover changes to row
    changes = compareDict(row=row, data=data)['modified']
    if t != row.treatmentType:
        changes['treatmentType'] = (row.treatmentType.uuid,t.uuid)
    if r != row.riskResponse:
        changes['riskResponse'] = (row.riskResponse.uuid,r.uuid)

    # Assign changes to row
    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']
    row.riskResponse_uuid = r.uuid
    row.riskResponse = r
    row.treatmentType_uuid = t.uuid
    row.treatmentType = t

    try:
        db.session.commit()
        putLog(table='treatment', uuid=unicode(uuid), changes=changes)
        return {'success': 'Treatment updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='treatment')
            return {'error': 'Treatment already exist'}
        else:
            errorLog(unicode(E), table='treatment')
            return {'error': unicode(E)}

def deleteTreatment(uuid):
    row = getTreatment(uuid)
    try:
        req = deleteLog(table='treatment', uuid=unicode(uuid))
        db.session.delete(row)
        db.session.commit()
        return {'success': 'Treatment deleted'}
    except Exception as E:
        errorLog(unicode(E), table='treatment')
        return {'error': unicode(E)}

def treatmentSelectData():
    data = getTreatments()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def treatmentListData():
    entries = getTreatments()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc, r.treatmentType.title, r.riskResponse.title]
        data.append(temp)
    return data
