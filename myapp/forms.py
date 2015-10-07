from django import forms


class ProjectForm(forms.Form):
    InputName = forms.CharField()
    InputDescription = forms.CharField()