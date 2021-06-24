from Models_MVC.models import User
from os import remove
from Models_MVC.models import Project
from django.shortcuts import render
from datetime import datetime
from django.template.response import TemplateResponse
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
import boto3 #aws services

def index(request):

	#user data used for change bug former accoringly to user type
	user_data = User.objects.all()
	user = request.user
	print(user.username)
	user_session = user_data.filter(user_username__exact=user.username)

	#convert date stored on DB to html format
	user_birth_front =\
	datetime.strftime(user_session[0].user_birth,'%Y-%m-%d') 

	page_properties = PageProperties

	file_name =\
	'Content/images/users/'+'user_'+str(user_session[0].id)+'_profilepic'

	#download user pic if it's not on the local server yet
	try:
		file_exist = open(file_name)

	except FileNotFoundError:
		download_user_pic(user_session[0].id, file_name)

	#chceck wants new checkbox
	if (user_session[0].user_wants_news==True):
		user_wants_news="checked"
	else: user_wants_news=""

	context = {
		'user_session': user_session,
		'user_birth_front': user_birth_front,
		'user_wants_news': user_wants_news,
		'page_properties': page_properties
	}

	if user.is_authenticated:
			return render(request, 'ProfilePage.html', context)
	else:
		return render(request, 'SignIn.html', context)

def update_user(request):

	#user data used for change bug former accoringly to user type
	user = request.user
	user_session = User.objects.get(user_username=user.username)

	#if a new pic was uploaded
	if (request.FILES):
		s3 = boto3.resource('s3')
		bucket_name = 'soulfulplatform'
		file_local = request.FILES
		data = file_local['profilepic']
		key_file = 'UserFiles/ProfilePics/user_'+str(user_session.id)+'_profilepic'
		s3.Bucket(bucket_name).put_object(Key=key_file, Body=data)
		user_session.user_photo = 'user_'+str(user_session.id)+'_profilepic'

	if (request.POST.get("full_name")!=None and\
	request.POST.get("full_name")!=""):
		user_session.user_name=request.POST.get("full_name")

	if (request.POST.get("user_username")!=None and\
	request.POST.get("user_username")!=""):
	#checking if user name exists
		test_username =\
		User.objects.filter(user_username=request.POST.get("user_username")).exists()

		if (test_username):
			messages.error(request, 'Username already exists!')
		else:
			user_session.user_username=request.POST.get("user_username")
			user.username = request.POST.get("user_username")
			user.save()

	if (request.POST.get("user_mail1")!=None and\
	request.POST.get("user_mail1")!=""):
		user_session.user_mail_1=request.POST.get("user_mail1")

	if (request.POST.get("user_mail2")!=None and\
	request.POST.get("user_mail2")!=""):
		user_session.user_mail_2=request.POST.get("user_mail2")

	if (request.POST.get("user_phone")!=None and\
	request.POST.get("user_phone")!=""):
		user_session.user_phone=request.POST.get("user_phone")

	if (request.POST.get("user_document_1")!=None and\
	request.POST.get("user_document_1")!=""):
		user_session.user_document_1=request.POST.get("user_document_1")

	if (request.POST.get("user_document_2")!=None and\
	request.POST.get("user_document_2")!=""):
		user_session.user_document_2=request.POST.get("user_document_2")

	if (request.POST.get("user_country")!=None and\
	request.POST.get("user_country")!=""):
		user_session.user_country=request.POST.get("user_country")

	if (request.POST.get("user_state")!=None and\
	request.POST.get("user_state")!=""):
		user_session.user_state=request.POST.get("user_state")

	if (request.POST.get("user_district")!=None and\
	request.POST.get("user_district")!=""):
		user_session.user_district=request.POST.get("user_district")

	if (request.POST.get("user_zip_code")!=None and\
	request.POST.get("user_zip_code")!=""):
		user_session.user_zip_code=request.POST.get("user_zip_code")

	if (request.POST.get("user_street")!=None and\
	request.POST.get("user_street")!=""):
		user_session.user_street=request.POST.get("user_street")

	if (request.POST.get("user_street_number")!=None and\
	request.POST.get("user_street_number")!=""):
		user_session.user_street_number=request.POST.get("user_street_number")

	if (request.POST.get("user_city")!=None and\
	request.POST.get("user_city")!=""):
		user_session.user_city=request.POST.get("user_city")

	if (request.POST.get("user_birth")!=None and\
	request.POST.get("user_birth")!=""):
		user_session.user_birth=request.POST.get("user_birth")

	if (request.POST.get("user_wants_news")=='on'):
		user_session.user_wants_news=True

	else: user_session.user_wants_news=False

	user_session.save()

	messages.success(request, 'Profile updated!')

	if user.is_authenticated:
			return HttpResponseRedirect('/User_Platform/Profile')
	else:
		return render(request, 'SignIn.html', context)

class PageProperties:

	def __init__(self):
		self.profilepic_height = 150
		self.profilepic_width = 150

#download user pic
def download_user_pic(user_id, save_path):

	s3 = boto3.client('s3')
	s3_resource = boto3.resource('s3') 
	bucket_name = 'soulfulplatform'
	s3_bucket = s3_resource.Bucket(bucket_name)
	path_file =\
	'UserFiles/ProfilePics/user_'+str(user_id)+'_profilepic'
	objs = list(s3_bucket.objects.filter(Prefix=path_file))

	#check if there's a profile pic for current user
	if objs:
		s3.download_file(bucket_name, path_file, save_path)
