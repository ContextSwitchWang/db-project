from flask      import request, flash, redirect, url_for, session
from user       import User
import logging
import renderers

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
            return log_the_user_in(user_name)
        else:
            return renderers.helloLoginRenderer(error=error)
    else:
        return renderers.helloLoginRenderer()

def log_the_user_in(user_name):
    session['username'] = user_name
    flash('You were successfully logged in')
    user = User.getUser(user_name)
    if user:
        session['role'] = user.role
    else:
        logging.warning('User role not acquired')
    return redirect(url_for('dashboard'))

def usersHandler():
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
                     request.form['user_role']):
                error = 'Add user failed'
        if error:
            logging.warning(error)
            flash(error)
        return redirect(url_for('users'))
    else:
        return renderers.usersRenderer()
            