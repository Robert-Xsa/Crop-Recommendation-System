from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

class MainForm(forms.Form):
    def __init__(self,  *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.required = True


class PredictionForm(MainForm):
    N = forms.FloatField(label='Nitrogen')
    P = forms.FloatField(label='Phosphorus')
    K = forms.FloatField(label='Potassium')
    temperature = forms.FloatField(label='Temperature')
    humidity = forms.FloatField(label='Humidity')
    ph = forms.FloatField(label='pH')
    rainfall = forms.FloatField(label='Rainfall')
    

#new
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'phone_number', 'address', 'region', 'country','first_name','last_name']
        



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email','password')


