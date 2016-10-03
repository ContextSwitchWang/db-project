def ACLUsers(role):
	return role == 'admin' or role == 'guest'