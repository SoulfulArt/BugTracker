from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate
from django.shortcuts import render
from Models_MVC.models import Bug
from Models_MVC.models import Project

def index(request):

	#constants and variables
	bugs_list = Bug.objects.all() #list of all bug on database
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
	'file_local': file_local
	}

	if request.user.is_authenticated:
	    return render(request, 'BugTracker.html', context)

	else:
		context = {'error_message': 'Please, sign in!'}
		return render(request, 'SignIn.html', context)

def bug_priority_transform(bugs_showed):

	for i in range (len(bugs_showed)):
		if bugs_showed[i].bug_priority == 1:
			bugs_showed[i].bug_priority = 'Low'
		if bugs_showed[i].bug_priority == 2:
			bugs_showed[i].bug_priority = 'Normal'
		if bugs_showed[i].bug_priority == 3:
			bugs_showed[i].bug_priority = 'High'

	return bugs_showed
