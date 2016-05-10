import bottle_session
import bottle

def check_session(app, session):
    valid_session = session.get('valid')
    user_name = session.get('name')
    if valid_session:
        return user_name
    else:
        bottle.redirect(app.get_url('login'))
