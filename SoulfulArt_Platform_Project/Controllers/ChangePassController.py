from os import remove
from django.shortcuts import render
from datetime import datetime
from django.template.response import TemplateResponse
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):

	#user data used for change bug former accoringly to user type
	user = request.user

	if user.is_authenticated:
		return render(request, 'ChangePassword.html')
	else:
		return render(request, 'SignIn.html')

def change_pass(request):

	#user data used for change bug former accoringly to user type
	user = request.user
	current_username = user.username

	if not user.check_password(request.POST.get("user_current_pass")):
		messages.error(request, 'Current Password is incorrect. Try again, please!')
		return HttpResponseRedirect('/User_Platform/Profile/ChangePass')

	if (request.POST.get("user_new_pass_0")!=\
	request.POST.get("user_new_pass_1")):
		messages.error(request, 'News passwords didn\'t match. Try again, please!')
		return HttpResponseRedirect('/User_Platform/Profile/ChangePass')

	user.set_password(request.POST.get("user_new_pass_0"))

	user.save()

	logout(request)

	messages.success(request, 'Password changed!')

	user = authenticate(request, username=current_username,\
	password=request.POST.get("user_new_pass_0"))

	if user.is_authenticated:
			return HttpResponseRedirect('/User_Platform/Profile/ChangePass')
	else:
		return render(request, 'SignIn.html')
