from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate
from django.shortcuts import render
from Models_MVC.models import User
from Models_MVC.models import Project

def index(request):

    page_path = 'HomePageUser.html'

    user_data = User.objects.all()
    user = request.user
    user_session = user_data.filter(user_username__exact=user.username)

    context={
        'user_session': user_session
    }

    if request.user.is_authenticated:
        return render(request, page_path, context)

    else:
        context = {'error_message': 'Sign In Failed!'}
        return render(request, 'SignIn.html', context)
