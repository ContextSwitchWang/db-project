from flask                import render_template, url_for, session, request
from user                 import User
import logging
import settings


def helloLoginRenderer(**kwargs):
    return render_template('helloLogin.html',
#                            css_url=url_for('static', filename='login.css'),
                            guest=User.getUser('guest'),
                            **kwargs)
def dashboardRenderer():

    return render_template('dashboard.html')

def usersRenderer():
    users = User.getAllUsers()
    return render_template('users.html',
                            users=users)

def privilegeRenderer():
	return render_template('privilege.html',
                            settings=[(s.key.id(), s.users, s.roles) for s in settings.Settings.getSettings()])