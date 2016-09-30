from flask      import render_template, url_for, session
def helloLoginRenderer(**kwargs):
	return render_template('helloLogin.html',
							css_url=url_for('static', filename='login.css'),
							**kwargs)
def dashboardRenderer():
	return render_template('dashboard.html',
                            user_name=session['username'])