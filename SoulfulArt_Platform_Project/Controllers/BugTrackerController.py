from Models_MVC.models import Bug
from Models_MVC.models import User
from os import remove
from Models_MVC.models import Project
from django.shortcuts import render
from datetime import datetime
from django.template.response import TemplateResponse
from django.http.response import HttpResponse
import boto3 #aws services

def index(request):

	#user data used for change bug former accoringly to user type
	user_data = User.objects.all()
	user = request.user
	user_session = user_data.filter(user_username__exact=user.username)

	bugs_list = Bug.objects.all() #list of all bug on database

	form_fields = FormFields(user_session[0].user_type)

	bugs_list = filter_bug_user_type(user_session[0].user_type, user_session) 

	#constants and variables
	project_list = Project.objects.all() #list of all projects on database
	max_char_desc = 15 #number of characteres showed on bug description
	number_of_bugs = len(bugs_list)
	current_page = 1
	bugs_showed = []
	bugs_select_box = [] #name for the checkbox that will select the bug
	bugs_per_page = 5 #number of bugs per page
	number_of_pages = int(number_of_bugs/bugs_per_page) + 1
	select_all_bug = "" #select all bugs checkbox
	edit_fields = "hidden" #used to show edit elements
	new_bug_fields = "hidden"
	filter_fields = "hidden"
	show_clean_filter = "hidden" #used to show clean applied filters button
	file_local = request.FILES

	#For used to show only certaing bugs per page
	if current_page==1:
		current_bug_page = 0

	else:
		current_bug_page = (current_page-1)*(bugs_per_page-1) + (current_page-1)

	for i in range(current_bug_page,current_bug_page + bugs_per_page):
		if (i<number_of_bugs): #test if object exists
			bugs_showed.append(bugs_list[i])
			bugs_select_box.append('bug_check_'+str(bugs_list[i].id))

	bugs_showed = bug_priority_transform(bugs_showed)

	context = {
	'bugs_list': bugs_list,
	'max_char_desc': max_char_desc,
	'current_page': current_page,
	'number_of_pages': number_of_pages,
	'bugs_per_page': bugs_per_page,
	'bugs_showed': bugs_showed,
	'project_list': project_list,
	'bugs_select_box': bugs_select_box,
	'select_all_bug': select_all_bug,
	'edit_fields': edit_fields,
	'new_bug_fields': new_bug_fields,
	'filter_fields': filter_fields,
	'show_clean_filter': show_clean_filter,
	'number_of_bugs': number_of_bugs,
	'file_local': file_local,
	'user_data': user_data,
	'form_fields': form_fields
	}

	if user.is_authenticated:
			return render(request, 'BugTracker.html', context)
	else:
		return render(request, 'SignIn.html', context)

def bugtrackerform(request):

	#user section data
	user_data = User.objects.all()
	user = request.user
	user_session = user_data.filter(user_username__exact=user.username)

	#constants and variables
	bugs_list = filter_bug_user_type(user_session[0].user_type, user_session)
	project_list = Project.objects.all() #list of all projects on database
	max_char_desc = 15 #number of characteres showed on bug description
	number_of_bugs = len(bugs_list)
	bugs_showed = [] #bugs that will be shown
	bugs_select_box = [] #name for the checkbox that will select the bug
	create_bug = False #verify if create bug button was clicked
	select_all_bug = "" #select all bugs checkbox
	edit_fields = "hidden" #used to show edit elements
	new_bug_fields = "hidden" #used to show create new bug elements
	filter_fields = "hidden" #used to show filter bug elements
	show_clean_filter = "hidden" #used to show clean applied filters button
	filter_values = {} #used to keep filter values
	filter_values_view ={\
		'bug_name_filter': 'Bug Name',\
		'bug_duration_filter': None,\
		'duration_criteria_durationis': 'selected',\
		'duration_criteria_equal': '',\
		'duration_criteria_lte': '',\
		'duration_criteria_lt': '',\
		'duration_criteria_gte': '',\
		'duration_criteria_gt': '',\
		'project_id_filter': None,\
		'bug_description_filter': 'Bug Owner Description',\
		'impact_filter_yes': '',\
		'impact_filter_no': '',\
		'bug_status_filter_n': '',\
		'bug_status_filter_w': '',\
		'bug_status_filter_c': '',\
		'bug_priority_filter_low': '',\
		'bug_priority_filter_normal': '',\
		'bug_priority_filter_high': '',\
		'selected_project':'None'
		}

	s3 = boto3.resource('s3') #new aws s3 instance
	file_local = request.FILES

	#hidde or show editable fields accoringly to user type
	form_fields = FormFields(user_session[0].user_type)

	#Creating a session with filter values
	if (request.POST.get('filter_bug')=='Filter Apply'):
		clean_session(request)
		request.session['bug_name_filter']=\
		request.POST.get('bug_name_filter')
		request.session['bug_duration_filter']=\
		request.POST.get('bug_duration_filter')
		request.session['project_id_filter']=\
		request.POST.get('project_id_filter')
		request.session['bug_priority_filter']=\
		request.POST.get('bug_priority_filter')
		request.session['bug_status_filter']=\
		request.POST.get('bug_status_filter')
		request.session['bug_description_filter']=\
		request.POST.get('bug_description_filter')
		request.session['impact_filter_yes']=\
		request.POST.get('impact_filter_yes')
		request.session['impact_filter_no']=\
		request.POST.get('impact_filter_no')
		request.session['bug_status_filter_n']=\
		request.POST.get('bug_status_filter_n')
		request.session['bug_status_filter_w']=\
		request.POST.get('bug_status_filter_w')
		request.session['bug_status_filter_c']=\
		request.POST.get('bug_status_filter_c')
		request.session['bug_priority_filter_low']=\
		request.POST.get('bug_priority_filter_low')
		request.session['bug_priority_filter_normal']=\
		request.POST.get('bug_priority_filter_normal')
		request.session['bug_priority_filter_high']=\
		request.POST.get('bug_priority_filter_high')

	#Avoid asignment when session is empty
	if 'bug_name_filter' in request.session:
		filter_values ={\
		'bug_name_filter': request.session['bug_name_filter'],\
		'bug_duration_filter': request.session['bug_duration_filter'],\
		'project_id_filter': request.session['project_id_filter'],\
		'bug_description_filter': request.session['bug_description_filter'],\
		'impact_filter_yes': request.session['impact_filter_yes'],\
		'impact_filter_no': request.session['impact_filter_no'],\
		'bug_status_filter_n': request.session['bug_status_filter_n'],\
		'bug_status_filter_w': request.session['bug_status_filter_w'],\
		'bug_status_filter_c': request.session['bug_status_filter_c'],\
		'bug_priority_filter_low': request.session['bug_priority_filter_low'],\
		'bug_priority_filter_normal': request.session['bug_priority_filter_normal'],\
		'bug_priority_filter_high': request.session['bug_priority_filter_high']
		}

	#delete bugs
	if (request.POST.get('del_bug')=="Delete"):
		delete_bug(request)
		bugs_list = Bug.objects.all() #list of all bug on database

	#show edit elements
	if (request.POST.get('show_edit_form')=="Edit"):
		edit_fields = ""
		filter_fields = 'hidden'

	#Edit elements
	if (request.POST.get('edit_bug')=="Edit"):
		edit_bug(request)
		#refresh bugs
		bugs_list = Bug.objects.all() #list of all bug on database

	#Create bug elements
	if (request.POST.get('create_bug')=="Create Bug"):
		create_bug = True
		filter_fields = 'hidden'

	#Crate bug action
	if (create_bug):
		insert_bug(request, s3, file_local)
		bugs_list = Bug.objects.all() #list of all bug on database

	#clean filter
	if (request.POST.get('clean_filter')=='Clean Filter'):
		bugs_list = Bug.objects.all() #list of all bug on database
		filter_values = {}
		show_clean_filter = 'hidden'
		clean_session(request)

	#Keep showing filter form while there's a filter available
	if (filter_values):
		filter_fields = ''
		show_clean_filter = ''
		bugs_list = filter_bug(filter_values, request)
		number_of_bugs = len(bugs_list)
		filter_values_view = filter_to_view(filter_values, request)

	if request.method == 'POST':
		bugs_per_page = int(request.POST.get("bugs_per_page"))
		current_page = int(request.POST.get("select_current_page"))
		number_of_pages = int(number_of_bugs/bugs_per_page) + 1

	#when the current page is greater than the number of pages
	if current_page > number_of_pages:
		current_page = number_of_pages

	#For used to show only certaing bugs per page
	if current_page==1:
		current_bug_page = 0

	else:
		current_bug_page = (current_page-1)*(bugs_per_page-1) + (current_page-1)

	for i in range(current_bug_page,current_bug_page + bugs_per_page):
		if (i<number_of_bugs): #test if object exists
			bugs_showed.append(bugs_list[i])
			bugs_select_box.append('bug_check_'+str(bugs_list[i].id))

	#select all bug checkbox
	if (request.POST.get('select-all-bug')=='on'):
		select_all_bug = "checked"

	#show new bug elements
	if (request.POST.get('create_bug_form')=="Create New Bug"):
		new_bug_fields = ""
		filter_fields = 'hidden'

	#Filter bug elements
	if (request.POST.get('filter_bug_form')=="Filter Bugs"):
		filter_fields = ""

	bugs_showed = bug_priority_transform(bugs_showed)

	context = {
	'bugs_list': bugs_list,
	'max_char_desc': max_char_desc,
	'current_page': current_page,
	'number_of_pages': number_of_pages,
	'bugs_per_page': bugs_per_page,
	'bugs_showed': bugs_showed,
	'create_bug': create_bug,
	'project_list': project_list,
	'select_all_bug': select_all_bug,
	'bugs_select_box': bugs_select_box,
	'edit_fields': edit_fields,
	'new_bug_fields': new_bug_fields,
	'filter_fields': filter_fields,
	'show_clean_filter': show_clean_filter,
	'filter_values_view': filter_values_view,
	'number_of_bugs': number_of_bugs,
	'file_local': file_local,
	'user_data': user_data,
	'form_fields': form_fields
	}

	user = request.user
	if user.is_authenticated:
		return TemplateResponse(request, 'BugTracker.html', context)
	else:
		return render(request, 'SignIn.html', context)

def insert_bug(request, s3, file_local):

	bucket_name = 'soulfulplatform'

	#get bool option if bug may impact other projects
	if request.POST.get('impact_project')=='on':
		impact = True
	else:
		impact = False

	bug_project_id = int(request.POST.get('project-id'))

	if bug_project_id == 0: #in case a project was not choosen
		bug_project_id = None
	else:
		bug_project_id = Project.objects.get(id = bug_project_id)

	new_bug = Bug.objects.create(
	bug_name = request.POST.get('bug_name'),\
	bug_description = request.POST.get('bug_description'),\
	bug_files = None,\
	bug_creation_date = datetime.now(),\
	bug_conclusion_date = None,\
	bug_time_execution = None,\
	bug_priority = int(request.POST.get('bug-priority')),\
	bug_impact_other_projects = impact,\
	bug_conclusion_description = None,\
	bug_status = 'New',\
	bug_project = bug_project_id,\
	bug_collaborator_creator = None,\
	bug_owner = None,\
	bug_user_creator = None
	)

	new_bug.save()

	data = file_local['file-bug-new']
	key_file = 'BugsFiles/'+str(new_bug.id)+'/'+str(data)

	s3.Bucket(bucket_name).put_object(Key=key_file, Body=data)

	new_bug.bug_files = str(file_local['file-bug-new'])
	new_bug.save()

def edit_bug(request):

	bug_conclusion_date_edit = None #default conclusion date
	date_format_input = "%Y-%m-%d"

	#convert impact value from POST to bool options (on=True)
	impact = \
	impact_projects_bool(request.POST.get('impact_project_edit'))

	bug_project_id = int(request.POST.get('project_id_edit'))

	bug_project_id = get_project(bug_project_id)

	bug_status_edit =\
	status_value_transform(request.POST.get('bug_status_edit')) 

	#set conclusion date if bug was concluded
	if bug_status_edit == 'Concluded':
		bug_conclusion_date_edit = datetime.now()

	for name, value in request.POST.items():
		if value=='on' and name.isnumeric():
			bug_current = Bug.objects.get(id = int(name))

			#setting conclusion date
			bug_current.bug_conclusion_date = bug_conclusion_date_edit

			#ifs to don't edit empty values on form
			if(request.POST.get('bug_name_edit')!=''):
				bug_current.bug_name = request.POST.get('bug_name_edit')

			if(request.POST.get('bug_duration_edit')!=''):
				bug_current.bug_time_execution = request.POST.get('bug_duration_edit')

			if(request.POST.get('bug_priority_edit')!=None):
				bug_current.bug_priority = int(request.POST.get('bug_priority_edit'))

			if(request.POST.get('bug_description_edit')!=None):
				bug_current.bug_description = request.POST.get('bug_description_edit')

			if(request.POST.get('bug_conclusion_edit')!=None):
				bug_current.bug_conclusion_description = request.POST.get('bug_conclusion_edit')

			if (bug_project_id!='All' and bug_project_id!=None):
				bug_current.bug_project = bug_project_id

			if(bug_status_edit!=None):
				bug_current.bug_status = bug_status_edit

			if(request.POST.get('bug_creation_date')!=None and\
			request.POST.get('bug_creation_date')!=""):
				bug_current.bug_creation_date = \
				datetime.strptime(request.POST.get('bug_creation_date'),date_format_input)

			if(request.POST.get('bug_conclusion_date')!=None and\
			request.POST.get('bug_conclusion_date')!=""):
				bug_current.bug_conclusion_date = \
				datetime.strptime(request.POST.get('bug_conclusion_date'),date_format_input)

			if(request.POST.get('bug_owner_edit')!="0" and\
			request.POST.get('bug_owner_edit')!=None):
				if(request.POST.get('bug_owner_edit')=="-1"):
					bug_current.bug_owner = None
				else:
					bug_current.bug_owner =\
					User.objects.get(id=int(request.POST.get('bug_owner_edit')))

			if(request.POST.get('bug_creator_edit')!="0" and\
			request.POST.get('bug_creator_edit')!=None):
				if(request.POST.get('bug_creator_edit')=="-1"):
					bug_current.bug_creator = None
				else:
					bug_current.bug_creator =\
					User.objects.get(id=int(request.POST.get('bug_creator_edit'))) 

			bug_current.bug_files = None
			bug_current.bug_impact_other_projects = impact
			bug_current.bug_collaborator_creator = None
			bug_current.bug_owner = None
			bug_current.bug_user_creator = None

			bug_current.save()

def filter_bug(filter_values, request):

	filter_values['project_id_filter'] =\
	get_project(filter_values['project_id_filter'])

	filter_values['impact_filter_yes'] =\
	impact_projects_bool(filter_values['impact_filter_yes'])

	filter_values['impact_filter_no'] =\
	impact_projects_bool(filter_values['impact_filter_no'])

	if filter_values['bug_duration_filter']=='':
		filter_values['bug_duration_filter'] = None

	if filter_values['bug_name_filter']=='':
		bugs_list_filter = Bug.objects.all()
	else:
		bugs_list_filter = Bug.objects.all().filter(\
		bug_name__icontains = filter_values['bug_name_filter'])

	#get duration criteria
	duration_criteria = request.POST.get("filter_duration_criteria")

	if filter_values['bug_duration_filter']!=None:
		if duration_criteria=='0':
			bugs_list_filter = bugs_list_filter.filter(\
			bug_time_execution = filter_values['bug_duration_filter'])

		if duration_criteria=='1':
			bugs_list_filter = bugs_list_filter.filter(\
			bug_time_execution__lte = filter_values['bug_duration_filter'])

		if duration_criteria=='2':
			bugs_list_filter = bugs_list_filter.filter(\
			bug_time_execution__lt = filter_values['bug_duration_filter'])

		if duration_criteria=='3':
			bugs_list_filter = bugs_list_filter.filter(\
			bug_time_execution__gte = filter_values['bug_duration_filter'])

		if duration_criteria=='4':
			bugs_list_filter = bugs_list_filter.filter(\
			bug_time_execution__gt = filter_values['bug_duration_filter'])

	if filter_values['project_id_filter']!='All':
		bugs_list_filter = bugs_list_filter.filter(\
		bug_project_id = filter_values['project_id_filter'])

	if filter_values['bug_description_filter']!='':
		bugs_list_filter = bugs_list_filter.filter(\
		bug_description__icontains = filter_values['bug_description_filter'])

	if (filter_values['impact_filter_yes'] and\
	not filter_values['impact_filter_no']):
		bugs_list_filter = bugs_list_filter.filter(\
		bug_impact_other_projects = True)

	if (filter_values['impact_filter_no'] and\
	not filter_values['impact_filter_yes']):
		bugs_list_filter = bugs_list_filter.filter(\
		bug_impact_other_projects = False)

	#filter by bug status
	#when just New bugs will be shown
	if (filter_values['bug_status_filter_n']!=None and\
	filter_values['bug_status_filter_w']==None and\
	filter_values['bug_status_filter_c']==None):
		bugs_list_filter = bugs_list_filter.filter(\
		bug_status = filter_values['bug_status_filter_n'])

	#when just Working bugs will be shown
	if (filter_values['bug_status_filter_w']!=None and\
	filter_values['bug_status_filter_n']==None and\
	filter_values['bug_status_filter_c']==None):
		bugs_list_filter = bugs_list_filter.filter(\
		bug_status = filter_values['bug_status_filter_w'])

	#when just Concluded bugs will be shown
	if (filter_values['bug_status_filter_c']!=None and\
	filter_values['bug_status_filter_w']==None and\
	filter_values['bug_status_filter_n']==None):
		print(filter_values['bug_status_filter_c'])
		bugs_list_filter = bugs_list_filter.filter(\
		bug_status = filter_values['bug_status_filter_c'])

	#when New and working bugs will be shown
	if (filter_values['bug_status_filter_n']!=None and\
	filter_values['bug_status_filter_w']!=None and\
	filter_values['bug_status_filter_c']==None):
		bugs_list_filter = bugs_list_filter.filter(\
		bug_status__in = (filter_values['bug_status_filter_n'],\
		filter_values['bug_status_filter_w']))

	#when New and concluded bugs will be shown
	if (filter_values['bug_status_filter_n']!=None and\
	filter_values['bug_status_filter_w']==None and\
	filter_values['bug_status_filter_c']!=None):
		bugs_list_filter = bugs_list_filter.filter(\
		bug_status__in = (filter_values['bug_status_filter_n'],\
		filter_values['bug_status_filter_c']))

	#when Working and concluded bugs will be shown
	if (filter_values['bug_status_filter_n']==None and\
	filter_values['bug_status_filter_w']!=None and\
	filter_values['bug_status_filter_c']!=None):
		bugs_list_filter = bugs_list_filter.filter(\
		bug_status__in = (filter_values['bug_status_filter_w'],\
		filter_values['bug_status_filter_c']))

	#filter by bug priority
	#when just Low priority bugs will be shown
	if (filter_values['bug_priority_filter_low']!=None and\
	filter_values['bug_priority_filter_normal']==None and\
	filter_values['bug_priority_filter_high']==None):
		bugs_list_filter = bugs_list_filter.filter(\
		bug_priority__contains = int(filter_values['bug_priority_filter_low']))

	#when just Normal priority bugs will be shown
	if (filter_values['bug_priority_filter_normal']!=None and\
	filter_values['bug_priority_filter_low']==None and\
	filter_values['bug_priority_filter_high']==None):
		bugs_list_filter = bugs_list_filter.filter(\
		bug_priority = int(filter_values['bug_priority_filter_normal']))

	#when just High priority bugs will be shown
	if (filter_values['bug_priority_filter_normal']==None and\
	filter_values['bug_priority_filter_low']==None and\
	filter_values['bug_priority_filter_high']!=None):
		bugs_list_filter = bugs_list_filter.filter(\
		bug_priority = int(filter_values['bug_priority_filter_high']))

	#when low and normal priority bugs will be shown
	if (filter_values['bug_priority_filter_normal']!=None and\
	filter_values['bug_priority_filter_high']==None and\
	filter_values['bug_priority_filter_low']!=None):
		bugs_list_filter = bugs_list_filter.filter(\
		bug_priority__in = (filter_values['bug_priority_filter_low'],\
		filter_values['bug_priority_filter_normal']))

	#when low and high priority bugs will be shown
	if (filter_values['bug_priority_filter_normal']==None and\
	filter_values['bug_priority_filter_high']!=None and\
	filter_values['bug_priority_filter_low']!=None):
		bugs_list_filter = bugs_list_filter.filter(\
		bug_priority__in = (filter_values['bug_priority_filter_low'],\
		filter_values['bug_priority_filter_high']))

	#when normal and high priority bugs will be shown
	if (filter_values['bug_priority_filter_normal']!=None and\
	filter_values['bug_priority_filter_high']!=None and\
	filter_values['bug_priority_filter_low']==None):
		bugs_list_filter = bugs_list_filter.filter(\
		bug_priority__in = (filter_values['bug_priority_filter_normal'],\
		filter_values['bug_priority_filter_high']))

	return bugs_list_filter

def delete_bug(request):
	bugs_all = Bug.objects.all()
	for name, value in request.POST.items():
		if value=='on' and name.isnumeric():
			bugs_all.filter(id = int(name)).delete()

def impact_projects_bool(impact_post):
		if impact_post=='on':
			return True
		else:
			return False

def status_value_transform(status_value):

	if (status_value):
		status_value = int(status_value)

	#transform status value in names
	if status_value==1:
		return 'New'
	elif status_value==2:
		return 'Working'
	elif status_value==3:
		return 'Concluded'
	else:
		return None

def get_project(project_id):

	#if to avoid transform empty project_id into int
	if project_id:
		project_id = int(project_id)
	else:
		project_id = 0

	if project_id == 0: #in case a project was not choosen
		return None
	elif project_id == -1:
		return 'All'
	else:
		return Project.objects.get(id = project_id)

def filter_to_view(filter_values_view, request):

	duration_criteria =\
	request.POST.get('filter_duration_criteria') 

	if (duration_criteria == '0'):
		filter_values_view['duration_criteria_equal'] =\
		'selected'

	if (duration_criteria == '1'):
		filter_values_view['duration_criteria_lte'] =\
		'selected'

	if (duration_criteria == '2'):
		filter_values_view['duration_criteria_lt'] =\
		'selected'

	if (duration_criteria == '3'):
		filter_values_view['duration_criteria_gte'] =\
		'selected'

	if (duration_criteria == '4'):
		filter_values_view['duration_criteria_gt'] =\
		'selected'

	#keep bug name placeholder when this field is empty
	if (filter_values_view['bug_name_filter']!=''):
		filter_values_view['bug_name_filter'] =\
		filter_values_view['bug_name_filter']
	else:
		filter_values_view['bug_name_filter'] = 'None'

	#keep bug description placeholder when this field is empty
	if (filter_values_view['bug_description_filter']!=''):
		filter_values_view['bug_description_filter'] =\
		filter_values_view['bug_description_filter']
	else:
		filter_values_view['bug_description_filter'] = 'None'

	#showing status applied in filter
	if (filter_values_view['bug_status_filter_n']!=None):
		filter_values_view['bug_status_filter_n'] = 'checked'
	else:
		filter_values_view['bug_status_filter_n'] = ''

	if (filter_values_view['bug_status_filter_w']!=None):
		filter_values_view['bug_status_filter_w'] = 'checked'
	else:
		filter_values_view['bug_status_filter_w'] = ''

	if (filter_values_view['bug_status_filter_c']!=None):
		filter_values_view['bug_status_filter_c'] = 'checked'
	else:
		filter_values_view['bug_status_filter_c'] = ''

	#showing priorty applied filters
	if (filter_values_view['bug_priority_filter_low']!=None):
		filter_values_view['bug_priority_filter_low'] = 'checked'
	else:
		filter_values_view['bug_priority_filter_low'] = ''

	if (filter_values_view['bug_priority_filter_normal']!=None):
		filter_values_view['bug_priority_filter_normal'] = 'checked'
	else:
		filter_values_view['bug_priority_filter_normal'] = ''

	if (filter_values_view['bug_priority_filter_high']!=None):
		filter_values_view['bug_priority_filter_high'] = 'checked'
	else:
		filter_values_view['bug_priority_filter_high'] = ''

	#keep impact project choosen checkbox
	if (filter_values_view['impact_filter_yes']):
		filter_values_view['impact_filter_yes'] = 'checked'
	else:
		filter_values_view['impact_filter_yes'] = ''

	if (filter_values_view['impact_filter_no']):
		filter_values_view['impact_filter_no'] = 'checked'
	else:
		filter_values_view['impact_filter_no'] = ''

	#show selected project
	if (request.POST.get('project_id_filter')=='-1'):
		filter_values_view['selected_project']='All'	
	elif (request.POST.get('project_id_filter')==None or\
	request.POST.get('project_id_filter')=='0'):
		filter_values_view['selected_project']='No Project'
	else:
		selected_project = request.POST.get('project_id_filter')
		selected_project = get_project(selected_project)
		filter_values_view['selected_project']=\
		selected_project.project_name

	return filter_values_view

def clean_session(request):
	if 'bug_name_filter' in request.session:
		del request.session['bug_name_filter']
	if 'bug_duration_filter' in request.session:
		del request.session['bug_duration_filter']
	if 'project_id_filter' in request.session:
		del request.session['project_id_filter']
	if 'bug_description_filter' in request.session:
		del request.session['bug_description_filter']
	if 'impact_filter_yes' in request.session:
		del request.session['impact_filter_yes']
	if 'impact_filter_no' in request.session:
		del request.session['impact_filter_no']
	if 'bug_status_filter_n' in request.session:
		del request.session['bug_status_filter_n']
	if 'bug_status_filter_w' in request.session:
		del request.session['bug_status_filter_w']
	if 'bug_status_filter_c' in request.session:
		del request.session['bug_status_filter_c']
	if 'bug_priority_filter_low' in request.session:
		del request.session['bug_priority_filter_low']
	if 'bug_priority_filter_normal' in request.session:
		del request.session['bug_priority_filter_normal']
	if 'bug_priority_filter_high' in request.session:
		del request.session['bug_priority_filter_high']

def bug_priority_transform(bugs_showed):

	for i in range (len(bugs_showed)):
		if bugs_showed[i].bug_priority == 1:
			bugs_showed[i].bug_priority = 'Low'
		if bugs_showed[i].bug_priority == 2:
			bugs_showed[i].bug_priority = 'Normal'
		if bugs_showed[i].bug_priority == 3:
			bugs_showed[i].bug_priority = 'High'

	return bugs_showed

def dowload_bug_file(request):

	bucket_name = 'soulfulplatform'

	path_file = str(request.path).replace('User_Platform/BugTracker/download/','')
	path_file = 'BugsFiles'+path_file

	file_name = path_file[path_file.rfind('/')+1:len(path_file)]
	file_name = 'Downloads/BugFiles/'+file_name #saving file on correct folder
	s3 = boto3.client('s3')
	s3.download_file(bucket_name, path_file, file_name)

	my_data = open(file_name,'rb')

	file_name_short = file_name.replace('Downloads/BugFiles/','')

	response = HttpResponse(my_data)
	response['Content-Disposition'] =\
	"attachment; filename=%s" % file_name_short

	remove(file_name)

	return response

class FormFields:

	def __init__(self, user_type):

		self.creation_date_label = ''
		self.creation_date_input = ''
		self.conclusion_date_label = ''
		self.conclusion_date_input = ''
		self.bug_description_edit = ''
		self.bug_owner_edit = ''
		self.bug_creator_edit = ''
		self.execution_edit = ''
		self.priority_options_edit = ''
		self.priority_label_edit = ''
		self.status_options_edit = ''
		self.status_label_edit = ''
		self.impact_edit = ''

		if (user_type=='Collab'):
			self.creation_date_label = 'hidden'
			self.creation_date_input = 'hidden'
			self.conclusion_date_label = 'hidden'
			self.conclusion_date_input = 'hidden'
			self.bug_description_edit = 'display:none;'
			self.bug_owner_edit = 'hidden'
			self.bug_creator_edit = 'hidden'

		if (user_type=='Customer'):
			self.creation_date_label = 'hidden'
			self.creation_date_input = 'hidden'
			self.conclusion_date_label = 'hidden'
			self.conclusion_date_input = 'hidden'
			self.bug_description_edit = 'display:none;'
			self.bug_owner_edit = 'hidden'
			self.bug_creator_edit = 'hidden'
			self.execution_edit = 'hidden'
			self.priority_options_edit = 'hidden'
			self.priority_label_edit = 'hidden'
			self.status_options_edit = 'hidden'
			self.status_label_edit = 'hidden'
			self.impact_edit = 'hidden'
			self.bug_description_edit = ''
			self.bug_conclusion_edit = 'display:none;'

def filter_bug_user_type(user_type, user_session):

	bugs_list = Bug.objects.all() #list of all bug on database 

	if user_type=='Collab':
		bugs_list = bugs_list.filter(bug_owner=user_session[0])

	if user_type=='Customer':
		bugs_list = bugs_list.filter(bug_creator=user_session[0])

	return bugs_list
