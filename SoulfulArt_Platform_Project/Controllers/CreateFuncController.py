from Models_MVC.models import Function
from Models_MVC.models import FunctionLevel
from django.shortcuts import render
from datetime import datetime

def index(request):

	#constants and variables
	func_list = Function.objects.all() #list of all functions on database
	#list of all functions levels on database
	func_levels = FunctionLevel.objects.all()
	number_of_func = len(func_list)
	current_page = 1
	func_showed = []
	max_char_desc = 15 #number of characteres showed on department email
	func_per_page = 5 #number of functions per page
	number_of_pages = int(number_of_func/func_per_page) + 1
	select_all_func = "" #select all functions checkbox
	edit_fields = "hidden" #used to show edit elements
	new_func_fields = "hidden"
	filter_fields = "hidden"
	show_clean_filter = "hidden" #used to show clean applied filters button

	#For used to show only certaing functions per page
	if current_page==1:
		current_func_page = 0

	else:
		current_func_page = (current_page-1)*(func_per_page-1) + (current_page-1)

	for i in range(current_func_page,current_func_page + func_per_page):
		if (i<number_of_func): #test if object exists
			func_showed.append(func_list[i])

	context = {
	'func_list': func_list,
	'func_levels': func_levels,
	'current_page': current_page,
	'number_of_pages': number_of_pages,
	'func_per_page': func_per_page,
	'func_showed': func_showed,
	'select_all_func': select_all_func,
	'edit_fields': edit_fields,
	'new_func_fields': new_func_fields,
	'filter_fields': filter_fields,
	'max_char_desc': max_char_desc,
	'show_clean_filter': show_clean_filter,
	'number_of_func': number_of_func
	}

	return render(request, 'CreateFunc.html', context)

def funcform(request):

	#constants and variables
	func_list = Function.objects.all() #list of all department on database
	#list of all functions levels on database
	func_levels = FunctionLevel.objects.all()
	max_char_desc = 15 #number of characteres showed on department email
	number_of_func = len(func_list)
	func_showed = [] #functions that will be shown
	select_all_func = "" #select all functions checkbox
	edit_fields = "hidden" #used to show edit elements
	new_func_fields = "hidden" #used to show create new department elements
	filter_fields = "hidden" #used to show filter department elements
	show_clean_filter = "hidden" #used to show clean applied filters button
	filter_values = {} #used to keep filter values
	filter_values_view ={} #used to show current filter values on page

	#Creating a session with filter values
	if (request.POST.get('filter_func')=='Filter Apply'):
		clean_session(request)
		request.session['func_name_filter']=\
		request.POST.get('func_name_filter')
		request.session['active_filter_yes']=\
		request.POST.get('active_filter_yes')
		request.session['active_filter_no']=\
		request.POST.get('active_filter_no')
		request.session['func_phone_filter']=\
		request.POST.get('func_phone_filter')

	#Avoid asignment when session is empty
	if 'func_name_filter' in request.session:
		filter_values ={\
		'func_name_filter': request.session['func_name_filter'],\
		'active_filter_yes': request.session['active_filter_yes'],\
		'active_filter_no': request.session['active_filter_no'],\
		'func_phone_filter': request.session['func_phone_filter']
		}
		filter_fields = ''
		show_clean_filter = ''
		func_list = filter_func(filter_values, request)
		number_of_func = len(func_list)
		filter_values_view = filter_to_view(filter_values, request)

	#delete functions
	if (request.POST.get('del_func')=="Delete"):
		delete_func(request)
		func_list = Function.objects.all() #list of all department on database

	#show edit elements
	if (request.POST.get('show_edit_form')=="Edit"):
		edit_fields = ""
		filter_fields = 'hidden'

	#Edit elements
	if (request.POST.get('edit_func')=="Edit"):
		edit_func(request)
		#refresh functions
		func_list = Function.objects.all() #list of all department on database

	#Create department elements
	if (request.POST.get('create_func')=="Create Function"):
		insert_func(request)
		func_list = Function.objects.all() #list of all department on database

	#clean filter
	if (request.POST.get('clean_filter')=='Clean Filter'):
		filter_values = {}
		show_clean_filter = 'hidden'
		filter_fields='hidden'
		clean_session(request)
		func_list = Function.objects.all() #list of all department on database

	if request.method == 'POST':
		func_per_page = int(request.POST.get("func_per_page"))
		current_page = int(request.POST.get("select_current_page"))
		number_of_pages = int(number_of_func/func_per_page) + 1

	#when the current page is greater than the number of pages
	if current_page > number_of_pages:
		current_page = number_of_pages

	#For used to show only certaing functions per page
	if current_page==1:
		current_func_page = 0

	else:
		current_func_page = (current_page-1)*(func_per_page-1) + (current_page-1)

	for i in range(current_func_page,current_func_page + func_per_page):
		if (i<number_of_func): #test if object exists
			func_showed.append(func_list[i])

	#select all department checkbox
	if (request.POST.get('select-all-department')=='on'):
		select_all_func = "checked"

	#show new department elements
	if (request.POST.get('create_func_form')=="Create New Function"):
		new_func_fields = ""
		filter_fields = 'hidden'

	#Filter department elements
	if (request.POST.get('filter_func_form')=="Filter Functions"):
		filter_fields = ""

	context = {
	'func_list': func_list,
	'func_levels': func_levels,
	'max_char_desc': max_char_desc,
	'current_page': current_page,
	'number_of_pages': number_of_pages,
	'func_per_page': func_per_page,
	'select_all_func': select_all_func,
	'edit_fields': edit_fields,
	'new_func_fields': new_func_fields,
	'filter_fields': filter_fields,
	'func_showed': func_showed,
	'show_clean_filter': show_clean_filter,
	'filter_values_view': filter_values_view,
	'number_of_func': number_of_func
	}

	return render(request, 'CreateFunc.html', context)

def insert_func(request):

	#get bool option if function is active
	if request.POST.get('active_func')=='on':
		active = True
	else:
		active = False

	#get bool option if function can manage departments
	if request.POST.get('manager_func')=='on':
		manager = True
	else:
		manager = False

	new_func = Function.objects.create(
	func_name = request.POST.get('func_name'),
	func_level = request.POST.get('func_level_new'),
	func_creation_date = datetime.now(),
	func_active = active,
	func_manage_department = manager 
	)

	new_func.save()

def edit_func(request):

	for name, value in request.POST.items():
		if value=='on' and name.isnumeric():
			func_current = Function.objects.get(id = int(name))

			#ifs to don't edit empty values on form
			if(request.POST.get('func_name_edit')!=''):
				func_current.func_name =\
				request.POST.get('func_name_edit')

			if(request.POST.get('func_level_edit')!='-'):
				func_current.func_level =\
				request.POST.get('func_level_edit')

			if(request.POST.get('active_func_edit')=="Yes"):
				func_current.func_active = True

			if(request.POST.get('active_func_edit')=="No"):
				func_current.func_active = False

			if(request.POST.get('manager_func_edit')=="Yes"):
				func_current.func_manage_department = True

			if(request.POST.get('manager_func_edit')=="No"):
				func_current.func_manage_department = False

			func_current.save()

def filter_func(filter_values, request):

	func_list_filter = Function.objects.all()

	if filter_values['func_name_filter']=='':
		func_list_filter = Function.objects.all()
	else:
		func_list_filter = Function.objects.all().filter(\
		func_name__icontains = filter_values['func_name_filter'])

	if filter_values['func_phone_filter']!='':
		func_list_filter = Function.objects.all().filter(\
		func_phone__icontains = filter_values['func_phone_filter'])

	if (filter_values['active_filter_no']=='on' and\
	filter_values['active_filter_yes']!='on'):
		func_list_filter = func_list_filter.filter(\
		func_active = False)

	if (filter_values['active_filter_no']!='on' and\
	filter_values['active_filter_yes']=='on'):
		func_list_filter = func_list_filter.filter(\
		func_active = True)

	return func_list_filter

def delete_func(request):
	func_all = Function.objects.all()
	for name, value in request.POST.items():
		if value=='on' and name.isnumeric():
			func_all.filter(id = int(name)).delete()

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

	if 'func_name_filter' in request.session:
		del request.session['func_name_filter']
	if 'active_filter_yes' in request.session:
		del request.session['active_filter_yes']
	if 'active_filter_no' in request.session:
		del request.session['active_filter_no']
	if 'func_phone_filter' in request.session:
		del request.session['func_phone_filter']

def create_email(name_func):
	return name_func.replace(" ","").casefold()+'@soulfulart.com'
