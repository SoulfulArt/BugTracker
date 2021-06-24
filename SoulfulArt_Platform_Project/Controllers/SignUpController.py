from Models_MVC.models import User
from django.contrib.auth.models import User as UserDjango
from os import remove
from Models_MVC.models import Project
from django.shortcuts import render
from datetime import datetime
from django.template.response import TemplateResponse
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
import boto3 #aws services
from django.contrib.auth import authenticate, login

def index(request):

	return render(request, 'SignUpPage.html')

def create_user(request):

	#check if user typed must fields and also verify password
	if check_errors(request):
		return HttpResponseRedirect('/SignUp')

	else:
		#user data used for change bug former accoringly to user type
		user = request.user
		user_new = User.objects.create(\
		user_name=request.POST.get("full_name"),\
		user_username = request.POST.get("user_username"),\
		user_mail_1=request.POST.get("user_mail1"),\
		user_mail_2=request.POST.get("user_mail2"),\
		user_phone=request.POST.get("user_phone"),\
		user_document_1=request.POST.get("user_document_1"),\
		user_document_2=request.POST.get("user_document_2"),\
		user_country=request.POST.get("user_country"),\
		user_state=request.POST.get("user_state"),\
		user_district=request.POST.get("user_district"),\
		user_zip_code=request.POST.get("user_zip_code"),\
		user_street=request.POST.get("user_street"),\
		user_street_number=request.POST.get("user_street_number"),\
		user_city=request.POST.get("user_city"),\
		user_birth=request.POST.get("user_birth")
		)

		if (request.POST.get("user_wants_news")=='on'):
			user_new.user_wants_news=True

		else: user_new.user_wants_news=False

		#if a new pic was uploaded
		if (request.FILES):
			s3 = boto3.resource('s3')
			bucket_name = 'soulfulplatform'
			file_local = request.FILES
			data = file_local['profilepic']
			key_file = 'UserFiles/ProfilePics/user_'+str(user_new.id)+'_profilepic'
			s3.Bucket(bucket_name).put_object(Key=key_file, Body=data)
			user_new.user_photo = 'user_'+str(user_new.id)+'_profilepic'

		user_new.save()

		#creating user on Djago Admin Auth center
		user_new_django = UserDjango.objects.create_user(\
		user_new.user_username,\
		request.POST.get("user_mail1"),\
		request.POST.get("user_pass0")
		)

		messages.success(request, 'User Created!')

		#login new user
		user_auth = authenticate(request,\
		username=user_new.user_username,\
		password=request.POST.get("user_pass0"))

		return HttpResponseRedirect('/User_Platform/Profile')

def check_errors(request):

	error_problem = False

	if (request.POST.get("full_name")==None or\
	request.POST.get("full_name")==""):
		messages.error(request, 'Please, type your full Name!')
		error_problem = True

	if (request.POST.get("user_username")==None or\
	request.POST.get("user_username")==""):
	#checking if user name exists
		test_username =\
		User.objects.filter(user_username=request.POST.get("user_username")).exists()

		if (test_username):
			messages.error(request, 'Username already exists!')
			error_problem = True

	if (request.POST.get("user_mail1")==None or\
	request.POST.get("user_mail1")==""):
		messages.error(request, 'Please, type your e-mail!')
		error_problem = True

	if (request.POST.get("user_document_1")==None or\
	request.POST.get("user_document_1")==""):
		messages.error(request, 'Please, type your document!')
		error_problem = True

	if (request.POST.get("user_country")==None or\
	request.POST.get("user_country")==""):
		messages.error(request, 'Please, type your country!')
		error_problem = True

	if (request.POST.get("user_pass0")!=request.POST.get("user_pass1")):
		messages.error(request, 'Passwords didn\'t match!')
		error_problem = True

	if (request.POST.get("user_pass0")=="" or\
	request.POST.get("user_pass0")==None):
		messages.error(request, 'Please, type a password!')
		error_problem = True

	return error_problem
