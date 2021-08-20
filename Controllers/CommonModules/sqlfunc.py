#this functions returns the usernames of all users with manager
#functions
def select_managers(User):
		
	users = User.objects.all()
	users = users.filter(user_functions__func_manage_department = 1)

	return users

def select_user_by_id(user_id, User, current_user):

	if user_id == "-1":
		return None

	elif user_id == "0" and current_user!=None:
		return current_user

	else: return User.objects.get(id = int(user_id))