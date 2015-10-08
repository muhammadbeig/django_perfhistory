from django import forms 
from django.forms import Textarea, TextInput
from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
    	model = Project
    	name='name'
    	description = 'description'

    	fields = (name, description,)
    	widgets = {
            name: TextInput(attrs={'placeholder': name.capitalize()}),
            description: Textarea(attrs={'placeholder': description.capitalize(),'rows': 2}),
        }