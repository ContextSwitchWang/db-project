from flask import Flask, render_template, url_for, g
app = Flask(__name__)
app.config['DEBUG'] = True

teamname="Team Awesome"
wpi_logo='WPI_Inst_Prim_FulClr_Rev.png'

with app.app_context():
	pass

def run_before_request():
	g.wpi_logo_url = url_for('static', filename=wpi_logo)

app.before_request(run_before_request)

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('hello.html',
    						teamname=teamname,
    						img_url=g.wpi_logo_url,
    						css_url=url_for('static', filename='login.css'))


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template('404.html',
    						teamname=teamname,
    						img_url=g.wpi_logo_url), 404
