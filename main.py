from flask      import Flask, render_template, url_for, g, request, flash, session, redirect
from settings   import Settings
import          pdb
import          logging
import          renderers
import          handlers

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = '\xe8\xadI\ni\x89\xe7_\xbb\x9a\x02=\xeb\xd2|\xa5T5\xb8Q\x18Vw\xa2'
privilege_strings = {'usermanage', 'privilegemanage'}
#TODO: mv to google storage
wpi_logo='WPI_Inst_Prim_FulClr_Rev.png'


with app.app_context():
    Settings.initPrivileges(privilege_strings)

@app.before_request
def staticResourcesSetup():
    g.wpi_logo_url = url_for('static', filename=wpi_logo)
    g.teamname = "Team Awesome"

@app.before_request
def checkPrivilege():
    if request.path[0:7] == '/static':
        logging.info('Static resources access allowed')
        return
    if request.path in {'/login'
                        }:
        logging.info('Login allowed')
        return

    if 'username' not in session:
        logging.warning('Unauthorized access attemped!')
        return renderers.helloLoginRenderer()

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template('404.html'), 404

@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    return handlers.loginHandler()

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('roles', None)
    for x in privilege_strings:
        session.pop(x, None)
    logging.info('User logged out')
    return renderers.helloLoginRenderer()

@app.route('/dashboard')
def dashboard():
    return renderers.dashboardRenderer()

@app.route('/users', methods=['POST', 'GET'])
def users():
    return handlers.usersHandler()

@app.route('/privileges', methods=['POST', 'GET'])
def privileges():
    return handlers.privilegesHandler()
