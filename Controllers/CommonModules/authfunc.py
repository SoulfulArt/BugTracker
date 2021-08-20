def login_test(request, User):

	#login test
	user_data = User.objects.all()
	user = request.user
	user_session = user_data.filter(user_username__exact=user.username)

	if user.is_authenticated and user_session[0].user_type=="Admin":
			return True
	else:
		return False
