from flask      import Flask, render_template, url_for, g, request, flash, session, redirect
from db_login import log_the_user_in, valid_login
import          pdb
import          logging
import          renderers

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = '\xe8\xadI\ni\x89\xe7_\xbb\x9a\x02=\xeb\xd2|\xa5T5\xb8Q\x18Vw\xa2'

#TODO: mv to google storage
wpi_logo='WPI_Inst_Prim_FulClr_Rev.png'

with app.app_context():
    pass

def run_before_request():
    g.wpi_logo_url = url_for('static', filename=wpi_logo)
    g.teamname = "Team Awesome"

app.before_request(run_before_request)

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def helloLogin():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return renderers.helloLoginRenderer()

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template('404.html'), 404

@app.route('/login', methods=['POST', 'GET'])
def login():
    logging.info("Login Attempt with: ")
    logging.info(request)
    logging.info(request.form)
    error = 'Invalid username/password'
    if request.method == 'POST':
        if request.form.has_key('guest'):
            return log_the_user_in('guest')
        if valid_login(request.form['user_name'], request.form['user_pass']):
            return log_the_user_in(request.form['user_name'])

    return renderers.helloLoginRenderer(error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('helloLogin'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
            return redirect(url_for('helloLogin'))
    return renderers.dashboardRenderer()