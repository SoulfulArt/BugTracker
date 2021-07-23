from datetime import datetime
from Models_MVC.models import User
from django.shortcuts import render
from Models_MVC.models import Project
from django.http import HttpResponseRedirect
from Controllers.ControllerFunctions import login_test

def index(request):

	#constants and variables
	proj_list = Project.objects.all() #list of all functions on database
	number_of_proj = len(proj_list)
	current_page = 1
	proj_showed = []
	max_char_desc = 15 #number of characteres showed on department email
	proj_per_page = 5 #number of functions per page
	number_of_pages = int(number_of_proj/proj_per_page) + 1
	edit_fields = "hidden" #used to show edit elements
	new_proj_fields = "hidden"
	filter_fields = "hidden"
	show_clean_filter = "hidden" #used to show clean applied filters button

	#For used to show only certaing functions per page
	if current_page==1:
		current_proj_page = 0

	else:
		current_proj_page = (current_page-1)*(proj_per_page-1) + (current_page-1)

	for i in range(current_proj_page,current_proj_page + proj_per_page):
		if (i<number_of_proj): #test if object exists
			proj_showed.append(proj_list[i])

	if 'select_all_proj' in request.session:
		select_all_proj = request.session['select_all_proj']
	else:
		select_all_proj = ""

	context = {
	'proj_list': proj_list,
	'current_page': current_page,
	'number_of_pages': number_of_pages,
	'proj_per_page': proj_per_page,
	'proj_showed': proj_showed,
	'select_all_proj': select_all_proj,
	'edit_fields': edit_fields,
	'new_proj_fields': new_proj_fields,
	'filter_fields': filter_fields,
	'max_char_desc': max_char_desc,
	'show_clean_filter': show_clean_filter,
	'number_of_proj': number_of_proj
	}

	if login_test(request, User):
	    return render(request, 'CreateProject.html', context)
	else:
	    return render(request, 'SignIn.html', context)

def funcform(request):

	#constants and variables
	proj_list = Project.objects.all() #list of all department on database
	max_char_desc = 15 #number of characteres showed on department email
	number_of_proj = len(proj_list)
	proj_showed = [] #functions that will be shown
	edit_fields = "hidden" #used to show edit elements
	new_proj_fields = "hidden" #used to show create new department elements
	filter_fields = "hidden" #used to show filter department elements
	show_clean_filter = "hidden" #used to show clean applied filters button
	filter_values = {} #used to keep filter values
	filter_values_view ={} #used to show current filter values on page

	#Creating a session with filter values
	if (request.POST.get('filter_proj')=='Filter Apply'):
		clean_session(request)
		request.session['proj_name_filter']=\
		request.POST.get('proj_name_filter')
		request.session['active_filter_yes']=\
		request.POST.get('active_filter_yes')
		request.session['active_filter_no']=\
		request.POST.get('active_filter_no')
		request.session['proj_phone_filter']=\
		request.POST.get('proj_phone_filter')

	#Avoid asignment when session is empty
	if 'proj_name_filter' in request.session:
		filter_values ={\
		'proj_name_filter': request.session['proj_name_filter'],\
		'active_filter_yes': request.session['active_filter_yes'],\
		'active_filter_no': request.session['active_filter_no'],\
		'proj_phone_filter': request.session['proj_phone_filter']
		}
		filter_fields = ''
		show_clean_filter = ''
		proj_list = filter_proj(filter_values, request)
		number_of_proj = len(proj_list)
		filter_values_view = filter_to_view(filter_values, request)

	#delete functions
	if (request.POST.get('del_proj')=="Delete"):
		delete_proj(request)
		proj_list = Project.objects.all() #list of all department on database

	#show edit elements
	if (request.POST.get('show_edit_form')=="Edit"):
		edit_fields = ""
		filter_fields = 'hidden'

	#Edit elements
	if (request.POST.get('edit_proj')=="Edit"):
		edit_proj(request)
		#refresh functions
		proj_list = Project.objects.all() #list of all department on database

	#Create department elements
	if (request.POST.get('create_proj')=="Create Project"):
		insert_proj(request)
		proj_list = Project.objects.all() #list of all department on database

	#clean filter
	if (request.POST.get('clean_filter')=='Clean Filter'):
		filter_values = {}
		show_clean_filter = 'hidden'
		filter_fields='hidden'
		clean_session(request)
		proj_list = Project.objects.all() #list of all department on database

	if request.method == 'POST':
		proj_per_page = int(request.POST.get("proj_per_page"))
		current_page = int(request.POST.get("select_current_page"))
		number_of_pages = int(number_of_proj/proj_per_page) + 1

	#when the current page is greater than the number of pages
	if current_page > number_of_pages:
		current_page = number_of_pages

	#For used to show only certaing functions per page
	if current_page==1:
		current_proj_page = 0

	else:
		current_proj_page = (current_page-1)*(proj_per_page-1) + (current_page-1)

	for i in range(current_proj_page,current_proj_page + proj_per_page):
		if (i<number_of_proj): #test if object exists
			proj_showed.append(proj_list[i])

	#select all department checkbox
	if (request.POST.get('select-all-department')=='on'):
		request.session['select_all_proj']=\
		"checked"
	else:
		request.session['select_all_proj']=\
		""

	#show new department elements
	if (request.POST.get('create_proj_form')=="Create New Project"):
		new_proj_fields = ""
		filter_fields = 'hidden'

	#Filter department elements
	if (request.POST.get('filter_proj_form')=="Filter Projects"):
		filter_fields = ""

	context = {
	'proj_list': proj_list,
	'max_char_desc': max_char_desc,
	'current_page': current_page,
	'number_of_pages': number_of_pages,
	'proj_per_page': proj_per_page,
	'edit_fields': edit_fields,
	'new_proj_fields': new_proj_fields,
	'filter_fields': filter_fields,
	'proj_showed': proj_showed,
	'show_clean_filter': show_clean_filter,
	'filter_values_view': filter_values_view,
	'number_of_proj': number_of_proj
	}

	if login_test(request, User):
	    return HttpResponseRedirect('/CreateProj', context)
	else:
	    return HttpResponseRedirect('/SignIn')

def insert_proj(request):

	#get bool option if function is active
	if request.POST.get('active_proj')=='on':
		active = True
	else:
		active = False

	#get bool option if function can manage departments
	if request.POST.get('manager_proj')=='on':
		manager = True
	else:
		manager = False

	new_proj = Project.objects.create(
	proj_name = request.POST.get('proj_name'),
	proj_creation_date = datetime.now(),
	proj_active = active,
	proj_manage_department = manager 
	)

	new_proj.save()

def edit_proj(request):

	for name, value in request.POST.items():
		if value=='on' and name.isnumeric():
			proj_current = Project.objects.get(id = int(name))

			#ifs to don't edit empty values on form
			if(request.POST.get('proj_name_edit')!=''):
				proj_current.proj_name =\
				request.POST.get('proj_name_edit')

			if(request.POST.get('active_proj_edit')=="Yes"):
				proj_current.proj_active = True

			if(request.POST.get('active_proj_edit')=="No"):
				proj_current.proj_active = False

			if(request.POST.get('manager_proj_edit')=="Yes"):
				proj_current.proj_manage_department = True

			if(request.POST.get('manager_proj_edit')=="No"):
				proj_current.proj_manage_department = False

			proj_current.save()

def filter_proj(filter_values, request):

	proj_list_filter = Project.objects.all()

	if filter_values['proj_name_filter']=='':
		proj_list_filter = Project.objects.all()
	else:
		proj_list_filter = Project.objects.all().filter(\
		proj_name__icontains = filter_values['proj_name_filter'])

	if filter_values['proj_phone_filter']!='':
		proj_list_filter = Project.objects.all().filter(\
		proj_phone__icontains = filter_values['proj_phone_filter'])

	if (filter_values['active_filter_no']=='on' and\
	filter_values['active_filter_yes']!='on'):
		proj_list_filter = proj_list_filter.filter(\
		proj_active = False)

	if (filter_values['active_filter_no']!='on' and\
	filter_values['active_filter_yes']=='on'):
		proj_list_filter = proj_list_filter.filter(\
		proj_active = True)

	return proj_list_filter

def delete_proj(request):
	proj_all = Project.objects.all()
	for name, value in request.POST.items():
		if value=='on' and name.isnumeric():
			proj_all.filter(id = int(name)).delete()

def filter_to_view(filter_values_view, request):

	if filter_values_view['active_filter_yes'] == 'on':
		filter_values_view['active_filter_yes']="checked"
	else:
		filter_values_view['active_filter_yes']=""

	if filter_values_view['active_filter_no'] == 'on':
		filter_values_view['active_filter_no']="checked"
	else:
		filter_values_view['active_filter_no']=""

	return filter_values_view

def clean_session(request):

	if 'proj_name_filter' in request.session:
		del request.session['proj_name_filter']
	if 'active_filter_yes' in request.session:
		del request.session['active_filter_yes']
	if 'active_filter_no' in request.session:
		del request.session['active_filter_no']
	if 'proj_phone_filter' in request.session:
		del request.session['proj_phone_filter']

def create_email(name_proj):
	return name_proj.replace(" ","").casefold()+'@soulfulart.com'
