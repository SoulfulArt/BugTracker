from datetime import datetime
from Models_MVC.models import User
from django.shortcuts import render
from Models_MVC.models import Project
from Models_MVC.models import Function
from django.http import HttpResponseRedirect
from Controllers.CommonModules.authfunc import login_test

import Controllers.CommonModules.formviews as fv
import Controllers.CommonModules.sqlfunc as sql

def index(request):

	#constants and variables
	proj_list = filter_proj(request) #list of all functions on database
	number_of_proj = len(proj_list)
	current_page = 1
	proj_showed = []
	max_char_desc = 15 #number of characteres showed on department email

	if 'proj_per_page' in request.session:
		proj_per_page = request.session['proj_per_page'] #number of functions per page
	else: proj_per_page = 5 #number of functions per page

	if 'current_page' in request.session:
		current_page = request.session['current_page'] #current per page
	else: current_page = 1

	number_of_pages = int(number_of_proj/proj_per_page) + 1

	#variables used to show or hide forms
	showfields = fv.ShowFields(request)

	#For used to show only certaing functions per page
	if current_page==1:
		current_proj_page = 0

	else:
		current_proj_page =\
		(current_page-1)*(proj_per_page-1) + (current_page-1)

	for i in range(current_proj_page,current_proj_page + proj_per_page):
		if (i<number_of_proj): #test if object exists
			proj_showed.append(proj_list[i])

	if 'select_all_proj' in request.session:
		select_all_proj = request.session['select_all_proj']
	else:
		select_all_proj = ""

	#Avoid asignment when session is empty
	if 'proj_name_filter' in request.session:
		filter_values ={\
		'proj_name_filter': request.session['proj_name_filter'],\
		'proj_link_filter': request.session['proj_link_filter'],\
		'proj_desc_filter': request.session['proj_desc_filter'],\
		'creation_date_filter': request.session['creation_date_filter'],\
		'last_update_filter': request.session['last_update_filter'],\
		'project_manager_filter': request.session['project_manager_filter']
		}
		request.session['show_clean_filter'] = ''
	else: filter_values={}

	context = {
	'proj_list': proj_list,
	'current_page': current_page,
	'number_of_pages': number_of_pages,
	'proj_per_page': proj_per_page,
	'proj_showed': proj_showed,
	'select_all_proj': select_all_proj,
	'max_char_desc': max_char_desc,
	'number_of_proj': number_of_proj,
	'edit_fields': showfields.edit_fields,
	'new_proj_fields': showfields.new_proj_fields,
	'filter_fields': showfields.filter_fields,
	'show_clean_filter': showfields.show_clean_filter,
	'elements': showfields.fields_elements,
	'user_managers': sql.select_managers(User),
	'filter_values': filter_values
	}

	if login_test(request, User):
	    return render(request, 'Projects.html', context)
	else:
	    return render(request, 'SignIn.html', context)

def funcform(request):

	#constants and variables
	proj_list = Project.objects.all() #list of all department on database
	number_of_proj = len(proj_list)
	show_clean_filter = "hidden" #used to show clean applied filters button

	#Creating a session with filter values
	if (request.POST.get('filter_proj')=='Filter Apply'):


		#converting string with creation date to datetime
		creation_date_filter = datetime.strptime(
			request.POST.get('creation_date_filter'),
			'%Y-%M-%d')

		request.session['proj_name_filter']=\
		request.POST.get('proj_name_filter')
		request.session['proj_link_filter']=\
		request.POST.get('proj_link_filter')
		request.session['creation_date_filter_y']=\
		creation_date_filter.year
		request.session['creation_date_filter_m']=\
		creation_date_filter.month
		request.session['creation_date_filter_d']=\
		creation_date_filter.day
		request.session['last_update_filter']=\
		request.POST.get('last_update_filter')
		request.session['project_manager_filter']=\
		int(request.POST.get('project_manager_filter'))
		request.session['proj_desc_filter']=\
		request.POST.get('proj_desc_filter')

	#delete functions
	if (request.POST.get('del_proj')=="Delete"):
		delete_proj(request)
		proj_list = Project.objects.all() #list of all department on database

	#Edit elements
	if (request.POST.get('edit_proj')=="Edit"):
		edit_proj(request)
		#refresh functions
		proj_list = Project.objects.all() #list of all department on database

	#Create department elements
	if (request.POST.get('create_proj')=="Create Project"):
		new_proj(request)
		proj_list = Project.objects.all() #list of all department on database

	#clean filter
	if (request.POST.get('clean_filter')=='Clean Filter'):
		filter_values = {}
		show_clean_filter = 'hidden'
		filter_fields='hidden'
		clean_session(request)
		proj_list = Project.objects.all() #list of all department on database

	request.session['proj_per_page'] =\
	int(request.POST.get("proj_per_page"))

	#used to go to page locations when any action button is pressed
	#if no action button was pressed it goes to top
	request.session['fields_elements'] = "#top"

	request.session['current_page'] =\
	int(request.POST.get("select_current_page"))

	#when a page is greater than the number of pages for the current
	#number of projects per page, we go back to page 1
	number_of_pages =\
	int(number_of_proj/request.session['proj_per_page']) + 1
	if number_of_pages < request.session['current_page']:
		request.session['current_page'] = 1

	#select all department checkbox
	if (request.POST.get('select-all-department')=='on'):
		request.session['select_all_proj']=\
		"checked"
	else:
		request.session['select_all_proj'] = ""

	#show edit elements
	if (request.POST.get('show_edit_form')=="Edit"):
		request.session['edit_fields'] = ""
		request.session['filter_fields'] = "hidden"
		request.session['new_proj_fields'] = "hidden"
		request.session['fields_elements'] = "#fields_elements"

	#cancel edit
	if (request.POST.get('cancel_edit_proj')=="Cancel"):
		request.session['filter_fields'] = "hidden"
		request.session['fields_elements'] = "#top"
		request.session['new_proj_fields'] = "hidden"
		request.session['edit_fields'] = "hidden"

	#show new project elements
	if (request.POST.get('create_proj_form')=="Create New Project"):
		request.session['new_proj_fields'] = ""
		request.session['edit_fields'] = "hidden"
		request.session['filter_fields'] = "hidden"
		request.session['fields_elements'] = "#fields_elements"

	#Filter department elements
	if (request.POST.get('filter_proj_form')=="Filter Projects"):
		request.session['filter_fields'] = ""
		request.session['edit_fields'] = "hidden"
		request.session['new_proj_fields'] = "hidden"
		request.session['fields_elements'] = "#fields_elements"

	if login_test(request, User):
	    return HttpResponseRedirect('/Projects')
	else:
	    return HttpResponseRedirect('/SignIn')

def new_proj(request):

	#get manager user instance
	pm = sql.select_user_by_id(
		request.POST.get('project_manager_new'),
		User,
		None)

	new_proj = Project.objects.create(
	project_name = request.POST.get('proj_name_new'),
	project_link = request.POST.get('proj_link_new'),
	project_creation_date = datetime.now(),
	project_last_Update = datetime.now(),
	project_description = request.POST.get('proj_description_new'),
	project_collaborator = pm
	)

	new_proj.save()

def edit_proj(request):

	check_update = False #used to verify if a project was changed

	for name, value in request.POST.items():
		if value=='on' and name.isnumeric():

			proj_current = Project.objects.get(id = int(name))

			#ifs to don't edit empty values on form
			if(request.POST.get('proj_name_edit')!='' and\
				request.POST.get('proj_name_edit')!=None):

				proj_current.project_name =\
				request.POST.get('proj_name_edit')
				check_update = True

			if(request.POST.get('proj_link_edit')!='' and\
				request.POST.get('proj_link_edit')!=None):

				proj_current.project_link =\
				request.POST.get('proj_link_edit')
				check_update = True

			if(request.POST.get('project_description_edit')!='' and\
				request.POST.get('project_description_edit')!=None):

				proj_current.project_description =\
				request.POST.get('project_description_edit')
				check_update = True

			#get manager user instance
			pm = sql.select_user_by_id(
				request.POST.get('project_manager_edit'),
				User,
				proj_current.project_collaborator)

			proj_current.project_collaborator = pm

			if(request.POST.get('project_manager_edit')=="-1"):
				proj_current.project_collaborator = None
				check_update = True

			if check_update == True:
				proj_current.project_last_Update = datetime.now()

			proj_current.save()

def filter_proj(request):

	proj_list_filter = Project.objects.all()

	print(proj_list_filter[0].project_creation_date)

	if 'proj_name_filter' in request.session:

		if request.session['proj_name_filter']!='' and\
		request.session['proj_name_filter']!=None:
			proj_list_filter = proj_list_filter.filter(\
			project_name__icontains = request.session['proj_name_filter'])

		if request.session['proj_link_filter']!='' and\
		request.session['proj_link_filter']!=None:
			proj_list_filter = proj_list_filter.filter(\
			project_link__icontains = request.session['proj_link_filter'])

		if request.session['last_update_filter']!='' and\
		request.session['last_update_filter']!=None:
			proj_list_filter = proj_list_filter.filter(\
			project_last_Update = request.session['last_update_filter'])

		if request.session['proj_desc_filter']!='' and\
		request.session['proj_desc_filter']!=None:
			proj_list_filter = proj_list_filter.filter(\
			project_description__icontains = request.session['proj_desc_filter'])

		if request.session['project_manager_filter']!='' and\
		request.session['project_manager_filter']!=None and\
		request.session['project_manager_filter']!=0 and\
		request.session['project_manager_filter']!=-1:
			proj_list_filter = proj_list_filter.filter(\
			project_collaborator__id = request.session['project_manager_filter'])

		if request.session['project_manager_filter']==-1:
			proj_list_filter = proj_list_filter.filter(\
			project_collaborator__id = None)

	return proj_list_filter

def delete_proj(request):
	proj_all = Project.objects.all()
	for name, value in request.POST.items():
		if value=='on' and name.isnumeric():
			proj_all.filter(id = int(name)).delete()

def clean_session(request):

	if 'proj_name_filter' in request.session:
		del request.session['proj_name_filter']
	if 'active_filter_yes' in request.session:
		del request.session['active_filter_yes']
	if 'active_filter_no' in request.session:
		del request.session['active_filter_no']
	if 'proj_phone_filter' in request.session:
		del request.session['proj_phone_filter']