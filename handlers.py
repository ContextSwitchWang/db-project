from flask      import request, flash, redirect, url_for, session
from user       import User
import logging
import renderers
from settings import          Settings
import pdb

def loginHandler():
    if request.method == 'POST':
        logging.info("Login Attempt with: ")
        logging.info(request)
        logging.info(request.form)
        error = 'Invalid username/password'
        user_name = request.form['user_name']
        user_pass = request.form['user_pass']
        if User.verifyAndLogin(user_name, user_pass):
            return 'successful'
        else:
            return 'invalid login/password'
    else:
        return renderers.helloLoginRenderer()

def usersHandler():
    # make it more secure by checking
    if not Settings.checkPrivilege(session['username'], session['roles'], 'usermanage'):
        session['usermanage'] = False
        flash('You are not authorized to view this page')
        return renderers.dashboardRenderer()
    if request.method == 'POST':
        error = None
        if request.form.has_key('delete'):
            user = request.form['delete']
            logging.info('Deletion of ' + user + ' initiated')
            error = User.delete(user)
        elif request.form.has_key('add_user'):
            user = request.form['user_name']
            logging.info('Add user ' + user + ' initiated')
            error = User.add(user,
                     request.form['user_pass'],
                     [request.form['user_role']])
        elif request.form.has_key('add_role'):
            user = request.form['user_name']
            logging.info('Add role to user ' + user + ' initiated')
            error = User.addRole(user,
                     {request.form['user_role']})
        elif request.form.has_key('del_role'):
            user = request.form['user_name']
            logging.info('Delete role from user ' + user + ' initiated')
            error = User.delRole(user,
                     {request.form['user_role']})
        else:
            error = 'Wrong request'
        if error:
            logging.warning(error)
            logging.warning(request)
            logging.warning(request.form)

            return error
        return 'successful'
        #return redirect(url_for('users'))
    else:
        return renderers.usersRenderer()
def privilegesHandler():
    if not Settings.checkPrivilege(session['username'], session['roles'], 'privilegemanage'):
        session['privilegemanage'] = False
        flash('You are not authorized to view this page')
        return renderers.dashboardRenderer()
    if request.method == 'POST':
        error = None
        if request.form.has_key('del') and request.form.has_key('add_user'):
            user = request.form['user_name']
            logging.info('Delete user from ' + user + ' initiated')
            error = Settings.rmUsersAndRoles(user,
                    {request.form['user_pass']},
                    set())
        elif request.form.has_key('del') and request.form.has_key('add_role'):
            user = request.form['user_name']
            logging.info('Delete role from ' + user + ' initiated')
            error = Settings.rmUsersAndRoles(user,
                    set(),
                    {request.form['user_role']})
        elif request.form.has_key('add_user'):
            user = request.form['user_name']
            logging.info('Add user ' + user + ' initiated')
            error = Settings.addUsersAndRoles(user,
                    {request.form['user_pass']},
                    set())
        elif request.form.has_key('add_role'):
            user = request.form['user_name']
            logging.info('Add role to user ' + user + ' initiated')
            error = Settings.addUsersAndRoles(user,
                    set(),
                    {request.form['user_role']})
        if error:
            logging.warning(error)
            return error
        else:
            return 'successful'
    return renderers.privilegeRenderer()
