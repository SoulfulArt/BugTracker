from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def index(request):

	username = request.POST.get('user_name_signin')
	password = request.POST.get('user_pass_signin')
	user = authenticate(request, username=username, password=password)

	if user is not None:
		login(request, user)
		return HttpResponseRedirect('/User_Platform/UserPage')

	elif (password=='' or password==None) and\
	(username=='' or username==None):
		context = {'error_message': 'Please type username and password!'}
		return render(request, 'SignIn.html', context)

	elif username=='' or username==None:
		context = {'error_message': 'Please type your username!'}
		return render(request, 'SignIn.html', context)

	elif password=='' or password==None:
		context = {'error_message': 'Please type your password!'}
		return render(request, 'SignIn.html', context)

	else:
		context = {'error_message': 'Sign In Failed!'}
		return render(request, 'SignIn.html', context)

	context = {'error_message': ''}
	return render(request, 'SignIn.html', context)
