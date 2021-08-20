#This class will save all labels used to show or hide forms
class ShowFields:

	def __init__(self, request):

		if 'edit_fields' in request.session:
			self.edit_fields = request.session['edit_fields']
		else: self.edit_fields = "hidden" #used to show edit elements

		if 'new_proj_fields' in request.session:
			self.new_proj_fields = request.session['new_proj_fields']
		else: self.new_proj_fields = "hidden" #used to show new project elements

		if 'filter_fields' in request.session:
			self.filter_fields = request.session['filter_fields']
		else: self.filter_fields = "hidden" #used to show filter elements

		if 'show_clean_filter' in request.session:
			self.show_clean_filter = request.session['show_clean_filter']
		else: self.show_clean_filter = "hidden" #used to show clean filter button

		#go to elements (edit, new, delete) when loading page
		if 'fields_elements' in request.session:
			self.fields_elements = request.session['fields_elements']
		else: self.fields_elements = "#top" #used to show clean filter button

		#go to elements (edit, new, delete) when loading page
		if 'show_clean_filter' in request.session:
			self.show_clean_filter = request.session['show_clean_filter']
		else: self.show_clean_filter = "hidden" #used to show clean filter button