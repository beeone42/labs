import bottle_session
import bottle
import db
import json
import hashlib

def r_login(app, config, db, my, cursor):
    @app.route('/login', method='GET', name='login')
    def login(session):
        return bottle.template('login', app=app, user_name='login', config=config)

    @app.route('/login', method='POST')
    def do_login(session):
        username = bottle.request.forms.get('username')
        password = bottle.request.forms.get('password')
        users = db.get_users(cursor, 0, username)
        sha = hashlib.new('sha1')
        sha.update(password)
        if (users[0]['password'] == sha.hexdigest()):
            session.regenerate()
            session['valid']=True
            session['name']=username
            bottle.redirect("/")
        else:
            bottle.redirect("/login")

    @app.route('/logout', name='logout')
    def logout(session):
        session['valid']=False
        session['name']=None
        session.destroy()
        return bottle.template('logout', app=app, user_name='logout');
