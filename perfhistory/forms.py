from django import forms 
from django.forms import Textarea, TextInput, CheckboxInput, NumberInput
from .models import Project, Tag, Result, Transaction
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

class ResultModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name

class TransactionForm(forms.ModelForm):    
    def __init__(self,*args,**kwargs):
        # self.result_id = kwargs.pop('result_id')
        # self.tag_id = kwargs.pop('tag_id') if kwargs.get('tag_id') else None
        # self.result_id = kwargs.pop('result_id') if kwargs.get('result_id') else None
        self.result_qs = kwargs.pop('result_qs')
        super(TransactionForm,self).__init__(*args,**kwargs)
        self.fields['result'].queryset = self.result_qs
        # print 'self.tag_id:',Result.objects.filter(tag_id=self.tag_id)
        # for r in Result.objects.filter(tag_id=self.tag_id):
        #     print r.name
        # if self.tag_id:
        # self.fields['result'] = ResultModelChoiceField(queryset=Result.objects.filter(tag_id=self.tag_id), empty_label=None)#, to_field_name='id')
        self.fields['result'] = ResultModelChoiceField(queryset=self.result_qs, empty_label=None)
        # if self.result_id:
        #     self.fields['result'] = Result.objects.get(id=self.result_id)


    # result = ResultModelChoiceField(queryset=self.result_qs, empty_label=None)

    class Meta:
        model = Transaction
        name='name'
        description = 'description'
        success_count = 'success_count'
        success_qps = 'success_qps'
        failure_count = 'failure_count'
        failure_qps = 'failure_qps'
        responsetime_average = 'responsetime_average'
        responsetime_median = 'responsetime_median'
        responsetime_minimum = 'responsetime_minimum'
        responsetime_maximum = 'responsetime_maximum'
        responsetime_stddev = 'responsetime_stddev'
        responsetime_p90 = 'responsetime_p90'
        responsetime_p95 = 'responsetime_p95'
        responsetime_p99 = 'responsetime_p99'
        responsetime_p99_99 = 'responsetime_p99_99'
        latency_average = 'latency_average'
        latency_median = 'latency_median'
        latency_minimum = 'latency_minimum'
        latency_maximum = 'latency_maximum'
        latency_stddev = 'latency_stddev'
        latency_p90 = 'latency_p90'
        latency_p95 = 'latency_p95'
        latency_p99 = 'latency_p99'
        latency_p99_99 = 'latency_p99_99'

        fields = (name, description, 'result', success_count, success_qps, failure_count, failure_qps, responsetime_average, responsetime_median, responsetime_minimum, responsetime_maximum, responsetime_stddev, responsetime_p90, responsetime_p95, responsetime_p99, responsetime_p99_99, latency_average, latency_median, latency_minimum, latency_maximum, latency_stddev, latency_p90, latency_p95, latency_p99, latency_p99_99)
        widgets = {
            name: TextInput(attrs={'required':True, 'class':'form-control', 'placeholder': 'Transaction '+name.capitalize()}),
            description: Textarea(attrs={'rows': 1, 'class':'form-control', 'placeholder': description.capitalize()}),
            
            # forms.ModelChoiceField(queryset=Result.objects.filter(user=user))
            success_count : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': success_count.capitalize(), 'rows': 2}),
            success_qps : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': success_qps.capitalize(), 'rows': 2}),
            failure_count : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': failure_count.capitalize(), 'rows': 2}),
            failure_qps : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': failure_qps.capitalize(), 'rows': 2}),
            responsetime_average : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': responsetime_average.capitalize(), 'rows': 2}),
            responsetime_median : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': responsetime_median.capitalize(), 'rows': 2}),
            responsetime_minimum : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': responsetime_minimum.capitalize(), 'rows': 2}),
            responsetime_maximum : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': responsetime_maximum.capitalize(), 'rows': 2}),
            responsetime_stddev : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': responsetime_stddev.capitalize(), 'rows': 2}),
            responsetime_p90 : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': responsetime_p90.capitalize(), 'rows': 2}),
            responsetime_p95 : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': responsetime_p95.capitalize(), 'rows': 2}),
            responsetime_p99 : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': responsetime_p99.capitalize(), 'rows': 2}),
            responsetime_p99_99 : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': responsetime_p99_99.capitalize(), 'rows': 2}),
            latency_average : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': latency_average.capitalize(), 'rows': 2}),
            latency_median : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': latency_median.capitalize(), 'rows': 2}),
            latency_minimum : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': latency_minimum.capitalize(), 'rows': 2}),
            latency_maximum : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': latency_maximum.capitalize(), 'rows': 2}),
            latency_stddev : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': latency_stddev.capitalize(), 'rows': 2}),
            latency_p90 : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': latency_p90.capitalize(), 'rows': 2}),
            latency_p95 : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': latency_p95.capitalize(), 'rows': 2}),
            latency_p99 : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': latency_p99.capitalize(), 'rows': 2}),
            latency_p99_99 : NumberInput(attrs={ 'class':'form-control small-input', 'placeholder': latency_p99_99.capitalize(), 'rows': 2}),
        }