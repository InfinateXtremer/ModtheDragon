from django import forms
from django.forms.widgets import MediaDefiningClass
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import *
from mptt.forms import TreeNodeMultipleChoiceField

class ModForm(forms.ModelForm):
	class Media:
		css = { 'all': ('/static/admin/css/widgets.css',) }
		js = ('/jsi18n',)
	
	
	
	class Meta:
		model = Mod
		fields = [
			'game',
			'file',
			'title',
			'thumbnail',
			'description',
			'dependencies',
			'version',
			'tags'
		]

	tags = TreeNodeMultipleChoiceField(queryset=Tag.objects.exclude(admin=True),
                               level_indicator='+--')

	def __init__(self, *args, **kwargs):
		is_staff = kwargs.pop('is_staff')
		
		super(ModForm, self).__init__(*args, **kwargs)

		if is_staff:
			self.fields['tags'].queryset = Tag.objects.all()