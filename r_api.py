import bottle_session
import bottle
import db
import json
from utils import *

def r_api(app, config, db, my, cursor):
    @app.route('/api/devis', method='GET', name='api_devis')
    @app.route('/api/devis/', method='GET', name='api_devis')
    def api_devis(session):
        check_session(app, session)
        devis = db.get_devis(cursor)
        print devis
        return dict(data=devis)

    @app.route('/api/devis/<did:int>', method='GET')
    def api_devis(did, session):
        assert isinstance(did, int)
        check_session(app, session)
        devis = db.get_devis(cursor, did)
        return dict(data=devis)

    @app.route('/api/deals', method='GET', name='api_deals')
    @app.route('/api/deals/', method='GET', name='api_deals')
    def api_deals(session):
        check_session(app, session)
        deals = db.get_deals(cursor)
        print deals
        return dict(data=deals)

    @app.route('/api/deals/<did:int>', method='GET')
    def api_deals(did, session):
        assert isinstance(did, int)
        check_session(app, session)
        deals = db.get_deals(cursor, did)
        return dict(data=deals)

    @app.route('/api/deals/nextid/<site_id:int>', method='GET')
    def api_deals_next_id(site_id, session):
        assert isinstance(site_id, int)
        check_session(app, session)
        res = db.find_next_bdcid(cursor, site_id)
        print res
        return dict(data=res)

    @app.route('/api/deal/<did:int>', method='POST', name='api_deal_update')
    def api_deal_update(did, session):
        assert isinstance(did, int)
        check_session(app, session)
        res = db.update_deal(my, cursor, did,
                             bottle.request.forms.get('bdcid'),
                             bottle.request.forms.get('description'),
                             bottle.request.forms.get('site_id'),
                             bottle.request.forms.get('creator_id'),
                             bottle.request.forms.get('validator_id'),
                             bottle.request.forms.get('state'))
        return dict(success=True, res=res)

    @app.route('/api/contractors', method='GET', name='api_contractors')
    @app.route('/api/contractors/', method='GET', name='api_contractors')
    def api_contractors(session):
        check_session(app, session)
        contractors = db.get_contractors(cursor)
        return dict(data=contractors)

    @app.route('/api/contractor/<cid:int>', method='POST', name='api_contractor_update')
    def api_contractor_update(cid, session):
        assert isinstance(cid, int)
        check_session(app, session)
        res = db.update_contractor(my, cursor, cid,
                             bottle.request.forms.get('enterprise'),
                             bottle.request.forms.get('contact_name'),
                             bottle.request.forms.get('contact_tel'),
                             bottle.request.forms.get('contact_mail'))
        return dict(success=True, res=res)
    
    @app.route('/api/devis/<did:int>/<deid:int>', method='POST', name='api_devis_update')
    def api_contractor_update(did, deid, session):
        assert isinstance(did, int)
        assert isinstance(deid, int)
        check_session(app, session)
        res = db.update_devis(my, cursor, deid, did,
                             bottle.request.forms.get('contractor_id'),
                             bottle.request.forms.get('amount'),
                             bottle.request.forms.get('date_received'),
                             bottle.request.forms.get('state'))
        return dict(success=True, res=res)
