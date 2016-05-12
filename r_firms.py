import bottle_session
import bottle
import db
import json
from utils import *


def r_firms(app, config, db, my, cursor):
    @app.route('/firms', name='firms')
    def firms(session):
        user_name = check_session(app, session)
        return bottle.template('firms', app=app, user_name=user_name, config=config)
