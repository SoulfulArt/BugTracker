# Generated by Django 3.1.7 on 2021-06-18 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep_name', models.CharField(max_length=50)),
                ('dep_mail_1', models.CharField(max_length=200)),
                ('dep_phone', models.CharField(max_length=20)),
                ('dep_creation_date', models.DateTimeField(blank=True, null=True)),
                ('dep_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('func_name', models.CharField(max_length=50)),
                ('func_level', models.CharField(max_length=25, null=True)),
                ('func_creation_date', models.DateTimeField(blank=True, null=True)),
                ('func_active', models.BooleanField(default=True)),
                ('func_manage_department', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FunctionLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('func_level', models.CharField(max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('user_username', models.CharField(default='', max_length=200)),
                ('user_mail_1', models.CharField(max_length=200, null=True)),
                ('user_mail_2', models.CharField(max_length=200, null=True)),
                ('user_phone', models.CharField(max_length=20, null=True)),
                ('user_creation_date', models.DateTimeField(blank=True, null=True)),
                ('user_last_login', models.DateTimeField(blank=True, null=True)),
                ('user_active', models.BooleanField(default=True, null=True)),
                ('user_wants_news', models.BooleanField(default=True, null=True)),
                ('user_document_1', models.CharField(max_length=30, null=True)),
                ('user_document_2', models.CharField(max_length=30, null=True)),
                ('user_country', models.CharField(max_length=30, null=True)),
                ('user_district', models.CharField(max_length=30, null=True)),
                ('user_street', models.CharField(max_length=50, null=True)),
                ('user_state', models.CharField(max_length=30, null=True)),
                ('user_zip_code', models.CharField(max_length=30, null=True)),
                ('user_type', models.CharField(default='Customer', max_length=20)),
                ('user_department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Models_MVC.department')),
                ('user_functions', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Models_MVC.function')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
                ('project_link', models.CharField(max_length=100)),
                ('project_creation_date', models.DateTimeField(blank=True, null=True)),
                ('project_last_Update', models.DateTimeField(blank=True, null=True)),
                ('project_description', models.CharField(max_length=1024)),
                ('project_collaborator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Models_MVC.user')),
            ],
        ),
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bug_name', models.CharField(max_length=200)),
                ('bug_description', models.CharField(max_length=1024, null=True)),
                ('bug_files', models.CharField(max_length=50, null=True)),
                ('bug_creation_date', models.DateTimeField(blank=True, null=True)),
                ('bug_conclusion_date', models.DateTimeField(blank=True, null=True)),
                ('bug_time_execution', models.IntegerField(default=0, null=True)),
                ('bug_priority', models.IntegerField(default=0, null=True)),
                ('bug_impact_other_projects', models.BooleanField(default=True)),
                ('bug_conclusion_description', models.CharField(max_length=1024, null=True)),
                ('bug_status', models.CharField(max_length=30, null=True)),
                ('bug_creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Models_MVC.user')),
                ('bug_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_owner_id', to='Models_MVC.user')),
                ('bug_project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Models_MVC.project')),
            ],
        ),
    ]
