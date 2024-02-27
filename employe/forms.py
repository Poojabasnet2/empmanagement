from django import forms

from employe.models import EmployeeDetails

class EmployeeForm(forms.ModelForm):
    class Meta:
        model=EmployeeDetails
        fields=['user','empcode','empdept','contact','joiningdate']
        widgets={
            'user':forms.TextInput(attrs={'class':'formcontrol'}),
            'empcode':forms.Textarea(attrs={'class':'formcontrol'}),
            'empdept':forms.Textarea(attrs={'class':'formcontrol'}),
            'contact':forms.Textarea(attrs={'class':'formcontrol'}),
            'joiningdate':forms.Textarea(attrs={'class':'formcontrol'}),
        }