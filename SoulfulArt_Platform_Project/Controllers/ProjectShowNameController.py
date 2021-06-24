from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from Models_MVC.models import Project

def index(request):

    return HttpResponse(template.render(context, request))
