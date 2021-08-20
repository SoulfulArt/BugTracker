"""SoulfulArt_Platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.urls import include
from Controllers import HomeController
from Controllers import CreateDepController
from Controllers import CreateFuncController
from Controllers import ProjectController
from Controllers import BugTrackerController
from Controllers import SignInController
from Controllers import SignOutController
from Controllers import UserPageController
from Controllers import ProfilePageController
from Controllers import ChangePassController
from Controllers import SignUpController

urlpatterns = [
    path('admin', admin.site.urls),
    path('Projects/', ProjectController.index),
    path('SignIn', SignInController.index),
    path('SignIn/', SignInController.index),
    path('SignUp', SignUpController.index),
    path('SignUp/', SignUpController.index),
    path('create_user', SignUpController.create_user),
    path('SignOut', SignOutController.index),
    path('SignOut/', SignOutController.index),
    path('User_Platform/BugTracker/', BugTrackerController.index),
    path('User_Platform/Profile/', ProfilePageController.index),
    path('User_Platform/Profile/ChangePass', ChangePassController.index),
    path('User_Platform/Profile/change_pass', ChangePassController.change_pass),
    path('User_Platform/Profile/update_form', ProfilePageController.update_user),
    path('HomePage/', HomeController.index),
    path('CreateDep/', CreateDepController.index),
    path('CreateFunc/', CreateFuncController.index),
    path('Projects/update_form', ProjectController.funcform),
    path('User_Platform/BugTracker/update_form', BugTrackerController.bugtrackerform),
    re_path(r'User_Platform/BugTracker/download/*/*', BugTrackerController.dowload_bug_file),
    path('CreateDep/update_form', CreateDepController.deptrackerform),
    path('CreateFunc/update_form', CreateFuncController.funcform),
    path('', HomeController.index),
    path('User_Platform/UserPage', UserPageController.index),
]
