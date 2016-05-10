import bottle_session
import bottle
import db
import json

from r_api import r_api
from r_login import r_login
from r_deal import r_deal
from r_contractors import r_contractors
from r_devis import r_devis

from utils import *

def read_config(confname):
    with open(confname) as json_data_file:
        data = json.load(json_data_file)
        return (data)

app = bottle.app()
plugin = bottle_session.SessionPlugin(cookie_lifetime=3600*24*7)
app.install(plugin)
config = read_config("config.json")
print config
my, cursor = db.connect(config['mysql']['host'],config['mysql']['user'],config['mysql']['pass'],config['mysql']['db'])

r_api(app, config, db, my, cursor)
r_login(app, config, db, my, cursor)
r_deal(app, config, db, my, cursor)
r_contractors(app, config, db, my, cursor)
r_devis(app, config, db, my, cursor)

@app.route('/', name='index')
def index(session):
    user_name = check_session(app, session)
    deals = db.get_deals(cursor)
    print deals
    return bottle.template('main', app=app, user_name=user_name, deals=deals, config=config);

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='./static/')

app.run(host='0.0.0.0', port=8042, debug=True, reloader=True)
