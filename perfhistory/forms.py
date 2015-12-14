from django import forms 
from django.forms import Textarea, TextInput, CheckboxInput
from .models import Project, Tag, Result
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'password',)
        widgets = {
            'username': TextInput(attrs={'required':True, 'placeholder': 'Username ', 'class':'form-control'}),
            'password': TextInput(attrs={'required':True, 'placeholder': 'Password ', 'class':'form-control', 'type':'password'}),
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class ProjectForm(forms.ModelForm):

    class Meta:
    	model = Project
    	name='name'
    	description = 'description'

    	fields = (name, description,)
    	widgets = {
            name: TextInput(attrs={'required':True, 'placeholder': 'Project '+name.capitalize()}),
            description: TextInput(attrs={'placeholder': 'Project '+description.capitalize(),'rows': 2}),
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