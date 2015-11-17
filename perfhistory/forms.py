from django import forms 
from django.forms import Textarea, TextInput
from .models import Project, Tag


class ProjectForm(forms.ModelForm):

    class Meta:
    	model = Project
    	name='name'
    	description = 'description'

    	fields = (name, description,)
    	widgets = {
            name: TextInput(attrs={'required':True, 'placeholder': 'Project '+name.capitalize()}),
            description: Textarea(attrs={'placeholder': 'Project '+description.capitalize(),'rows': 2}),
        }

class TagForm(forms.ModelForm):

	class Meta:
		model = Tag
		# project_id = 'project_id'
		name='name'
		description='description'

		fields=(name, description,)
		widgets = {
            name: TextInput(attrs={'required':True, 'placeholder':  'Tag '+name.capitalize()}),
            description: Textarea(attrs={'placeholder': 'Tag '+description.capitalize(),'rows': 1}),
        }

