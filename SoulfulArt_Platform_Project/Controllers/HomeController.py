from django.shortcuts import render
from django.template import loader

def index(request):

	pagelabels = PageFields(request.user.is_authenticated)

	context = {
		'pagelabels': pagelabels
	}

	return render(request, 'HomePage.html', context)

class PageFields():

	def __init__(self, authtest):

		if authtest:
			self.signin = 'hidden'
			self.signout = ''
			self.userpage = ''
			self.signinbutton = 'hidden'
			self.yourpagebutton = ''

		if not authtest:
			self.signin = ''
			self.signout = 'hidden'
			self.userpage = 'hidden'
			self.signinbutton = ''
			self.yourpagebutton = 'hidden'
