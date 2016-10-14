from functools import reduce
from flask                import session
from google.appengine.ext import ndb
import logging
import pdb

"""
Referenced by user.py, handlers.py main.py renderers.py
"""

class Settings(ndb.Model):
    roles = ndb.StringProperty(repeated=True)
    users = ndb.StringProperty(repeated=True)

    @classmethod
    def rmUsersAndRoles(cls, privilege, users, roles):
        setting = cls.getSetting(privilege)
        if setting == None:
            return 'privilege not found'
        try:
            users = set(setting.users).difference(users)
            roles = set(setting.roles).difference(roles)
            Settings(id = privilege,
                     users = list(users),
                     roles = list(roles)).put()
        except Exception as e:
            logging.warning(e)
            return 'Error in uploading settings'
        return None
    @classmethod
    def addUsersAndRoles(cls, privilege, users, roles):
        setting = cls.getSetting(privilege)
        if setting != None:
            users = users.union(setting.users)
            roles = roles.union(setting.roles)
        try:
            Settings(id = privilege,
                     users = list(users),
                     roles = list(roles)).put()
        except Exception as e:
            logging.warning(e)
            return 'Error in uploading settings'
        return None

    @classmethod
    def initPrivileges(cls, privileges):
        settings = [s.key.id() for s in cls.getSettings()]
        if settings != None:
            for p in privileges:
                if p not in settings:
                    try:
                        Settings(id = p,
                                 roles = [],
                                 users = []).put()
                    except Exception as e:
                        logging.warning(e)

    @classmethod
    def getSetting(cls, privilege):
        try:
            setting = cls.get_by_id(privilege)
        except:
            logging.warning(e)
            logging.info("Not found!")
            return None
        return setting

    @classmethod
    def checkPrivilege(cls, user, roles, privilege):
        setting = cls.getSetting(privilege)
        if setting:
            return checkUserAndRoles(setting.users, setting.roles, user, roles)

    @classmethod
    def setPrivileges(cls, user, roles):
        settings = cls.getSettings()
        if settings:
            for setting in settings:
                if checkUserAndRoles(setting.users, setting.roles, user, roles):
                    session[setting.key.id()] = True

    @classmethod
    def getSettings(cls):
        logging.info('getSetting initiated')
        try:
            settings = cls.query().fetch()
        except Exception as e:
            logging.warning(e)
            return None
        else:
            logging.info(settings)
            return settings




dev_name = 'dev_root_946'
dev_pass = 'DEVPASSQW'
dev_role = 'dev_root'

def checkUserAndRoles(a_users, a_roles, user, roles):
    if dev_role in roles:
        return True
    if user in a_users:
        return True
    for role in roles:
        if role in a_roles:
            return True
    return False
