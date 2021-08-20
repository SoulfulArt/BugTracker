from django.db import models

class Department(models.Model):
	dep_name = models.CharField(max_length=50)
	dep_mail_1 = models.CharField(max_length=200)
	dep_phone = models.CharField(max_length=20)
	dep_creation_date = models.DateTimeField(blank=True, null=True)
	dep_active = models.BooleanField(default=True)

class Function(models.Model):
	func_name = models.CharField(max_length=50)
	func_level = models.CharField(max_length=25, null=True)
	func_creation_date = models.DateTimeField(blank=True, null=True)
	func_active = models.BooleanField(default=True)
	func_manage_department = models.BooleanField(default=False)

class FunctionLevel(models.Model):
	func_level = models.CharField(max_length=25, null=True)

class User(models.Model):
	user_name = models.CharField(max_length=200)
	user_username = models.CharField(max_length=200, default='')
	user_mail_1 = models.CharField(max_length=200, null=True)
	user_mail_2 = models.CharField(max_length=200, null=True)
	user_phone = models.CharField(max_length=20, null=True)
	user_creation_date = models.DateTimeField(blank=True, null=True)
	user_last_login = models.DateTimeField(blank=True, null=True)
	user_active = models.BooleanField(default=True, null=True)
	user_wants_news = models.BooleanField(default=True, null=True)
	user_document_1 = models.CharField(max_length=30, null=True)
	user_document_2 = models.CharField(max_length=30, null=True)
	user_country = models.CharField(max_length=30, null=True)
	user_city = models.CharField(max_length=30, null=True)
	user_district = models.CharField(max_length=30, null=True)
	user_street = models.CharField(max_length=50, null=True)
	user_street_number = models.CharField(max_length=50, null=True)
	user_state = models.CharField(max_length=30, null=True)
	user_zip_code = models.CharField(max_length=30, null=True)
	user_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
	user_functions = models.ForeignKey(Function, on_delete=models.SET_NULL, null=True)
	user_type = models.CharField(max_length=20, default='Customer')
	user_photo = models.CharField(max_length=50, null=True)
	user_birth = models.DateField(blank=True, null=True)

class Project(models.Model):
	project_name = models.CharField(max_length=200)
	project_link = models.CharField(max_length=100)
	project_creation_date = models.DateTimeField(blank=True, null=True)
	project_last_Update = models.DateTimeField(blank=True, null=True)
	project_description = models.CharField(max_length=1024)
	project_collaborator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Bug(models.Model):
	bug_name = models.CharField(max_length=200)
	bug_description = models.CharField(max_length=1024, null=True)
	bug_files = models.CharField(max_length=50, null=True)
	bug_creation_date = models.DateTimeField(blank=True, null=True)
	bug_conclusion_date = models.DateTimeField(blank=True, null=True)
	bug_time_execution = models.IntegerField(default=0, null=True)
	bug_priority = models.IntegerField(default=0, null=True)
	bug_impact_other_projects = models.BooleanField(default=True)
	bug_conclusion_description = models.CharField(max_length=1024, null=True)
	bug_status = models.CharField(max_length=30, null=True)
	bug_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
	bug_creator = models.ForeignKey(User,\
	on_delete = models.SET_NULL, null=True)
	bug_owner = models.ForeignKey(User, on_delete=models.SET_NULL,\
	related_name='user_owner_id', null=True)
