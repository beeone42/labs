import bottle_session
import bottle
import db
import json

from r_api import r_api
from r_login import r_login
from r_firms import r_firms

from utils import *


def read_config(confname):
    with open(confname) as json_data_file:
        data = json.load(json_data_file)
        return (data)

app = bottle.app()
plugin = bottle_session.SessionPlugin(cookie_lifetime=3600 * 24 * 7)
app.install(plugin)
config = read_config("config.json")
print config
my, cursor = db.connect(config['mysql']['host'], config['mysql'][
                        'user'], config['mysql']['pass'], config['mysql']['db'])

r_api(app, config, db, my, cursor)
r_login(app, config, db, my, cursor)
r_firms(app, config, db, my, cursor)


@app.route('/', name='index')
def index(session):
    user_name = check_session(app, session)
    return bottle.template('main', app=app, user_name=user_name, config=config)


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='./static/')

app.run(host='0.0.0.0', port=8042, debug=True, reloader=True)
