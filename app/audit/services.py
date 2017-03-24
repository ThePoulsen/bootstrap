## -*- coding: utf-8 -*-

from flask import session
from models import log
from datetime import datetime
import uuid as UUID
from app import db

def logEntry(event, table=None, tableRow_uuid=None):
    uuid = UUID.uuid4()
    timestamp = datetime.now()
    tenant_uuid = session['tenant_uuid']
    user_uuid = session['user_uuid']

    req = log(uuid = uuid,
              timestamp = timestamp,
              tenant_uuid = tenant_uuid,
              user_uuid = user_uuid,
              table = table,
              tableRow_uuid = tableRow_uuid,
              event = event)

    try:
        db.session.add(req)
        db.session.commit()
        return {'success': 'Log entry added'}
    except:
        return {'Error': 'Could not add log entry'}

def viewLog(table, uuid=None):
    if uuid == None:
        req = logEntry('Table list requested', table=table)
    else:
        req = logEntry('Item details requested', table=table, tableRow_uuid=uuid)
    return req

def postLog(table, uuid):
    req = logEntry(event='Item posted', table=table, tableRow_uuid=uuid)
    return req

def putLog(table, uuid, changes):
    req = logEntry(event='Item modified: {}'.format(changes), table=table, tableRow_uuid=uuid)
    return req

def deleteLog(table, uuid):
    req = logEntry(event='Item deleted', table=table, tableRow_uuid=uuid)

def errorLog(event, table, uuid=None):
    if uuid == None:
        req = logEntry(event=event, table=table)
    else:
        req = logEntry(event=event, table=table, tableRow_uuid=uuid)
