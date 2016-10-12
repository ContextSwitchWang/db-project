from google.appengine.ext import ndb
from flask                import request, flash, session
import logging
import settings

# Let's make it top level for now
class User(ndb.Model):
    user_pass = ndb.StringProperty()
    roles = ndb.StringProperty(repeated=True)

    @classmethod
    def getUser(cls, name):
        logging.info('Downloading User Info for ' + name)
        try:
            user = cls.get_by_id(name)
        except Exception as e:
            logging.warning('Error in Searching User')
            logging.warning(e)
            return None
        else:
            if user:
                logging.info("User is: " + str(user))
                return user
            else:
                logging.warning("No user info received")
                return None

    @classmethod
    def getAllUsers(cls):
        logging.info('User List Downloading initiated')
        try:
            users = cls.query().fetch()
        except Exception as e:
            logging.warning('Error in Downloading users')
            logging.warning(e)
            return None
        else:
            logging.info('user listing:')
            logging.info(users)
            return [(user.key.id(), user.user_pass, user.roles) for user in users]


    @classmethod
    def verify(cls, name, user_pass):
        logging.info('User Verification')
        if name == settings.dev_name and user_pass == settings.dev_pass:
            logging.warning('Login via Hardcoded developer account')
            session['username'] = name
            session['roles'] = settings.dev_role
            return True
        user = cls.getUser(name)
        if user:
            logging.info("pass is: " + str(user.user_pass))
            if user.user_pass == user_pass:
                logging.info('Verified')
                session['username'] = name
                session['roles'] = user.roles
                return True
            else:
                logging.info('False Login Attempt!')
                return False


    @classmethod
    def delete(cls, name):
        user = User.getUser(name)
        if user:
            user.key.delete()
            logging.info("User deleted")
            return True
        else:
            return None
    @classmethod
    def addRole(cls, name, roles):
        user = User.getUser(name)
        if user:
            user.roles = list(roles.union(user.roles))
            try:
                user.put()
            except Exception as e:
                logging.warning(e)
                logging.warning('Error in adding user role')
            else:
                logging.info("User Role Added")
                return True

        return None
    @classmethod
    def add(cls, name, user_pass, roles):
        if name != '':
                try:
                    User(id = name,
                     user_pass = user_pass,
                     roles = roles).put()
                except Exception as e:
                    logging.warning(e)
                    logging.warning('Error in adding user')
                else:
                    return True
        else:
            logging.info('User_name cannot be empty')
        return False

