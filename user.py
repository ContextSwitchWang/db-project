from google.appengine.ext import ndb
import logging


# Let's make it top level for now
class User(ndb.Model):
    user_pass = ndb.StringProperty()
    role = ndb.StringProperty()

    @classmethod
    def getUser(cls, name):
        logging.info('Downloading User Info for ' + name)
        try:
            user = cls.get_by_id(name)
        except Exception as e:
            logging.warning('Error in Searching User')
            logging.warning(e)
            return False
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
            return [(user.key.id(), user.user_pass, user.role) for user in users] + [("dommy", "1234556", 'dommy')]


    @classmethod
    def verify(cls, name, user_pass):
        logging.info('User Verification')
        user = cls.getUser(name)
        if user:
            logging.info("pass is: " + str(user.user_pass))
            if user.user_pass == user_pass:
                logging.info('Verified')
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
    def add(cls, name, user_pass, role):
        if user != '':
                try:
                    User(id = name,
                     user_pass = user_pass,
                     role = role).put()
                except Exception as e:
                    logging.warning(e)
                    logging.warning('Error in adding user')
                else:
                    return True
        return False

