from flask      import request, flash, redirect, url_for, session
from user       import User
import logging
import renderers
import          settings


def loginHandler():
    if request.method == 'POST':
        logging.info("Login Attempt with: ")
        logging.info(request)
        logging.info(request.form)
        error = 'Invalid username/password'
        user_name = request.form['user_name']
        user_pass = request.form['user_pass']
        if request.form.has_key('guest'):
            user_name = 'guest'
        if User.verify(user_name, user_pass):
            flash('You were successfully logged in')
            return redirect(url_for('dashboard'))
        else:
            return renderers.helloLoginRenderer(error=error)
    else:
        return renderers.helloLoginRenderer()

def usersHandler():
    if not settings.ACLUsers(session['username'], session['roles']):
        flash('You are not authorized to view this page')
        return renderers.dashboardRenderer()
    if request.method == 'POST':
        error = None
        if request.form.has_key('delete'):
            user = request.form['delete']
            logging.info('Deletion of ' + user + ' initiated')
            if not User.delete(user):
                error = 'Deletion Aborted because user is not found'
        elif request.form.has_key('add_user'):
            user = request.form['user_name']
            logging.info('Add user ' + user + ' initiated')
            if not User.add(user,
                     request.form['user_pass'],
                     [request.form['user_role']]):
                error = 'Add user failed'
        elif request.form.has_key('add_role'):
            user = request.form['user_name']
            logging.info('Add role to user ' + user + ' initiated')
            if not User.addRole(user,
                     [request.form['user_role']]):
                error = 'Add user role failed'
        if error:
            logging.warning(error)
            flash(error)
        return redirect(url_for('users'))
    else:
        return renderers.usersRenderer()
