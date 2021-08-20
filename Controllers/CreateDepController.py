from Models_MVC.models import Department
from Models_MVC.models import User
from django.shortcuts import render
from datetime import datetime
from Controllers.CommonModules.authfunc import login_test

def index(request):

	#constants and variables
	dep_list = Department.objects.all() #list of all department on database
	number_of_dep = len(dep_list)
	current_page = 1
	dep_showed = []
	max_char_desc = 15 #number of characteres showed on department email
	dep_per_page = 5 #number of departments per page
	number_of_pages = int(number_of_dep/dep_per_page) + 1
	select_all_dep = "" #select all departments checkbox
	edit_fields = "hidden" #used to show edit elements
	new_dep_fields = "hidden"
	filter_fields = "hidden"
	show_clean_filter = "hidden" #used to show clean applied filters button

	#For used to show only certaing departments per page
	if current_page==1:
		current_dep_page = 0

	else:
		current_dep_page = (current_page-1)*(dep_per_page-1) + (current_page-1)

	for i in range(current_dep_page,current_dep_page + dep_per_page):
		if (i<number_of_dep): #test if object exists
			dep_showed.append(dep_list[i])

	context = {
	'dep_list': dep_list,
	'current_page': current_page,
	'number_of_pages': number_of_pages,
	'dep_per_page': dep_per_page,
	'dep_showed': dep_showed,
	'select_all_dep': select_all_dep,
	'edit_fields': edit_fields,
	'new_dep_fields': new_dep_fields,
	'filter_fields': filter_fields,
	'max_char_desc': max_char_desc,
	'show_clean_filter': show_clean_filter,
	'number_of_dep': number_of_dep
	}

	if login_test(request, User):
	    return render(request, 'CreateDep.html', context)
	else:
	    return render(request, 'SignIn.html', context)


def deptrackerform(request):

	#constants and variables
	dep_list = Department.objects.all() #list of all department on database
	max_char_desc = 15 #number of characteres showed on department email
	number_of_dep = len(dep_list)
	dep_showed = [] #departments that will be shown
	select_all_dep = "" #select all departments checkbox
	edit_fields = "hidden" #used to show edit elements
	new_dep_fields = "hidden" #used to show create new department elements
	filter_fields = "hidden" #used to show filter department elements
	show_clean_filter = "hidden" #used to show clean applied filters button
	filter_values = {} #used to keep filter values
	filter_values_view ={} #used to show current filter values on page

	#Creating a session with filter values
	if (request.POST.get('filter_dep')=='Filter Apply'):
		clean_session(request)
		request.session['dep_name_filter']=\
		request.POST.get('dep_name_filter')
		request.session['active_filter_yes']=\
		request.POST.get('active_filter_yes')
		request.session['active_filter_no']=\
		request.POST.get('active_filter_no')
		request.session['dep_phone_filter']=\
		request.POST.get('dep_phone_filter')

	#Avoid asignment when session is empty
	if 'dep_name_filter' in request.session:
		filter_values ={\
		'dep_name_filter': request.session['dep_name_filter'],\
		'active_filter_yes': request.session['active_filter_yes'],\
		'active_filter_no': request.session['active_filter_no'],\
		'dep_phone_filter': request.session['dep_phone_filter']
		}
		filter_fields = ''
		show_clean_filter = ''
		dep_list = filter_dep(filter_values, request)
		number_of_dep = len(dep_list)
		filter_values_view = filter_to_view(filter_values, request)

	#delete departments
	if (request.POST.get('del_dep')=="Delete"):
		delete_dep(request)
		dep_list = Department.objects.all() #list of all department on database

	#show edit elements
	if (request.POST.get('show_edit_form')=="Edit"):
		edit_fields = ""
		filter_fields = 'hidden'

	#Edit elements
	if (request.POST.get('edit_dep')=="Edit"):
		edit_dep(request)
		#refresh departments
		dep_list = Department.objects.all() #list of all department on database

	#Create department elements
	if (request.POST.get('create_dep')=="Create Department"):
		insert_dep(request)
		dep_list = Department.objects.all() #list of all department on database

	#clean filter
	if (request.POST.get('clean_filter')=='Clean Filter'):
		filter_values = {}
		show_clean_filter = 'hidden'
		filter_fields='hidden'
		clean_session(request)
		dep_list = Department.objects.all() #list of all department on database

	if request.method == 'POST':
		dep_per_page = int(request.POST.get("dep_per_page"))
		current_page = int(request.POST.get("select_current_page"))
		number_of_pages = int(number_of_dep/dep_per_page) + 1

	#when the current page is greater than the number of pages
	if current_page > number_of_pages:
		current_page = number_of_pages

	#For used to show only certaing departments per page
	if current_page==1:
		current_dep_page = 0

	else:
		current_dep_page = (current_page-1)*(dep_per_page-1) + (current_page-1)

	for i in range(current_dep_page,current_dep_page + dep_per_page):
		if (i<number_of_dep): #test if object exists
			dep_showed.append(dep_list[i])

	#select all department checkbox
	if (request.POST.get('select-all-department')=='on'):
		select_all_dep = "checked"

	#show new department elements
	if (request.POST.get('create_dep_form')=="Create New Department"):
		new_dep_fields = ""
		filter_fields = 'hidden'

	#Filter department elements
	if (request.POST.get('filter_dep_form')=="Filter Departments"):
		filter_fields = ""

	context = {
	'dep_list': dep_list,
	'max_char_desc': max_char_desc,
	'current_page': current_page,
	'number_of_pages': number_of_pages,
	'dep_per_page': dep_per_page,
	'select_all_dep': select_all_dep,
	'edit_fields': edit_fields,
	'new_dep_fields': new_dep_fields,
	'filter_fields': filter_fields,
	'dep_showed': dep_showed,
	'show_clean_filter': show_clean_filter,
	'filter_values_view': filter_values_view,
	'number_of_dep': number_of_dep
	}

	if login_test(request, User):
	    return render(request, 'CreateDep.html', context)
	else:
	    return render(request, 'SignIn.html', context)

def insert_dep(request):

	#get bool option if department may impact other projects
	if request.POST.get('active_dep')=='on':
		active = True
	else:
		active = False

	new_dep = Department.objects.create(
	dep_name = request.POST.get('dep_name'),
	dep_mail_1 = create_email(request.POST.get('dep_name')),
	dep_phone = request.POST.get('dep_phone'),
	dep_creation_date = datetime.now(),
	dep_active = active 
	)

	new_dep.save()

def edit_dep(request):

	for name, value in request.POST.items():
		if value=='on' and name.isnumeric():
			dep_current = Department.objects.get(id = int(name))

			#ifs to don't edit empty values on form
			if(request.POST.get('dep_name_edit')!=''):
				dep_current.dep_name = request.POST.get('dep_name_edit')
				dep_current.dep_mail_1 =\
				create_email(request.POST.get('dep_name_edit'))

			if(request.POST.get('dep_phone_edit')!=''):
				dep_current.dep_phone = request.POST.get('dep_phone_edit')

			if(request.POST.get('active_dep_edit')=="Yes"):
				dep_current.dep_active = True

			if(request.POST.get('active_dep_edit')=="No"):
				dep_current.dep_active = False

			dep_current.save()

def filter_dep(filter_values, request):

	dep_list_filter = Department.objects.all()

	if filter_values['dep_name_filter']=='':
		dep_list_filter = Department.objects.all()
	else:
		dep_list_filter = Department.objects.all().filter(\
		dep_name__icontains = filter_values['dep_name_filter'])

	if filter_values['dep_phone_filter']!='':
		dep_list_filter = Department.objects.all().filter(\
		dep_phone__icontains = filter_values['dep_phone_filter'])

	if (filter_values['active_filter_no']=='on' and\
	filter_values['active_filter_yes']!='on'):
		dep_list_filter = dep_list_filter.filter(\
		dep_active = False)

	if (filter_values['active_filter_no']!='on' and\
	filter_values['active_filter_yes']=='on'):
		dep_list_filter = dep_list_filter.filter(\
		dep_active = True)

	return dep_list_filter

def delete_dep(request):
	dep_all = Department.objects.all()
	for name, value in request.POST.items():
		if value=='on' and name.isnumeric():
			dep_all.filter(id = int(name)).delete()

def impact_projects_bool(impact_post):
		if impact_post=='on':
			return True
		else:
			return False

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

	if 'dep_name_filter' in request.session:
		del request.session['dep_name_filter']
	if 'active_filter_yes' in request.session:
		del request.session['active_filter_yes']
	if 'active_filter_no' in request.session:
		del request.session['active_filter_no']
	if 'dep_phone_filter' in request.session:
		del request.session['dep_phone_filter']

def create_email(name_dep):
	return name_dep.replace(" ","").casefold()+'@soulfulart.com'
