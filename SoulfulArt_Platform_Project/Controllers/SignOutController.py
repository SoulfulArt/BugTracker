from django.http import HttpResponseRedirect 
from django.contrib.auth import logout

def index(request):

	logout(request)

	return HttpResponseRedirect('SignIn')
