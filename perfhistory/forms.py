from django import forms 
from django.forms import Textarea, TextInput, CheckboxInput
from .models import Project, Tag, Result


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

class EditProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        name='name'
        description = 'description'

        fields = (name, description,)
        widgets = {
            name: TextInput(attrs={'required':True, 'class':'form-control'}),
            description: Textarea(attrs={'rows': 2, 'class':'form-control'}),
        }

class TagForm(forms.ModelForm):

	class Meta:
		model = Tag
		# project_id = 'project_id'
		name='name'
		description='description'

		fields=(name, description,)
		widgets = {
            name: TextInput(attrs={'required':True, 'placeholder':  'Tag '+name.capitalize(), 'class':'form-control'}),
            description: Textarea(attrs={'placeholder': 'Tag '+description.capitalize(),'rows': 1, 'class':'form-control'}),
        }

class EditResultForm(forms.ModelForm):

    class Meta:
        model = Result
        name='name'
        description = 'description'
        version = 'version'
        baseline = 'baseline'
        numberofusers = 'numberofusers'

        fields = (name, description, version, baseline, numberofusers)
        widgets = {
            name: TextInput(attrs={'required':True, 'class':'form-control'}),
            description: Textarea(attrs={'rows': 1, 'class':'form-control'}),
            version: TextInput(attrs={'required':True, 'class':'form-control'}),
            baseline: CheckboxInput(attrs={ 'class':'form-control'}),
            numberofusers : TextInput(attrs={ 'class':'form-control'}),
        }