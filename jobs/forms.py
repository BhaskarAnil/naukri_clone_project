from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the job role, requirements, etc.'}),
            'title': forms.TextInput(attrs={'placeholder': 'Job Title', 'required': True}),
            'location': forms.TextInput(attrs={'placeholder': 'Location (e.g. Bangalore, India)', 'required': True}),
            'salary': forms.TextInput(attrs={'placeholder': 'Salary (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['location'].required = True
        self.fields['salary'].required = False
