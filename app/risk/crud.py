from app import db
from flask import session
from app.rating.models import rating
from models import risk
import uuid as UUID
from datetime import datetime
from app.crud import impactCrud, probabilityCrud, riskAreaCrud, riskTypeCrud, userCrud
from app.audit.services import viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getRisks():
    viewLog(table='risk')
    return risk.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getRisk(uuid):
    viewLog(table='risk', uuid=unicode(uuid))
    return risk.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postRisk(data):
    i = impactCrud.getImpact(data['impact'])
    p = probabilityCrud.getProbability(data['probability'])
    ra = riskAreaCrud.getRiskArea(data['riskArea'])
    rt = riskTypeCrud.getRiskType(data['riskType'])
    ro = userCrud.getUser(data['owner'])
    row = risk(title = data['title'],
                 desc = data['desc'],
                 owner = data['owner'],
                 riskOwner = ro,
                 tenant_uuid = session['tenant_uuid'],
                 uuid = UUID.uuid4(),
                 impact_uuid=i.uuid,
                 impact=i,
                 probability_uuid=p.uuid,
                 probability=p,
                 riskArea_uuid=ra.uuid,
                 riskArea=ra,
                 riskType_uuid=rt.uuid,
                 riskType=rt,
                 created=datetime.now(),
                 createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='risk', uuid=unicode(row.uuid))
        return {'success': 'Risk added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='risk')
            return {'error': 'Risk already exist'}
        else:
            errorLog(unicode(E), table='risk')
            return {'error': unicode(E)}

def putRisk(data, uuid):
    row = getRisk(uuid)
    i = impactCrud.getImpact(data['impact'])
    p = probabilityCrud.getProbability(data['probability'])
    ra = riskAreaCrud.getRiskArea(data['riskArea'])
    rt = riskTypeCrud.getRiskType(data['riskType'])
    ro = userCrud.getUser(data['owner'])

    changes = compareDict(row=row, data=data)['modified']
    if i != row.impact:
        changes['impact'] = (row.impact.uuid,i.uuid)
    if p != row.probability:
        changes['probability'] = (row.probability.uuid,p.uuid)
    if ra != row.riskArea:
        changes['riskArea'] = (row.riskArea.uuid,p.uuid)
    if rt != row.riskType:
        changes['riskType'] = (row.riskType.uuid,p.uuid)
    if ro != row.riskOwner:
        changes['riskOwner'] = (row.riskOwner.uuid,p.uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']
    row.impact_uuid = i.uuid
    row.impact = i
    row.probability_uuid = p.uuid
    row.probability = p
    row.riskArea_uuid = ra.uuid
    row.riskArea = ra
    row.riskType_uuid = rt.uuid
    row.riskType = rt
    row.owner = data['owner']
    row.riskOwner = ro

    try:
        db.session.commit()
        putLog(table='risk', uuid=unicode(uuid), changes=changes)
        return {'success': 'Risk updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='risk')
            return {'error': 'Risk already exist'}
        else:
            errorLog(unicode(E), table='risk')
            return {'error': unicode(E)}

def deleteRisk(uuid):
    row = getRisk(uuid)
    try:
        db.session.delete(row)
        db.session.commit()
        deleteLog(table='risk', uuid=unicode(uuid))
        return {'success': 'Risk deleted'}
    except Exception as E:
        errorLog(unicode(E), table='risk')
        return {'error': unicode(E)}

def riskSelectData():
    data = getRisks()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def riskListData():
    entries = getRisks()
    data = []
    for r in entries:
        impact = r.impact.uuid
        probability = r.probability.uuid
        riskRating = rating.query.filter_by(tenant_uuid=session['tenant_uuid'], impact_uuid=impact, probability_uuid=probability).first()
        createdBy = userCrud.getUser(r.createdBy).name
        temp = [r.uuid, r.title, r.desc, r.impact.value, r.probability.value, riskRating.desc, r.created.strftime('%Y-%m-%d'), createdBy, r.riskOwner.name]
        data.append(temp)
    return data
