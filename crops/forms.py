from django import forms

class MainForm(forms.Form):
    pass

class PredictionForm(forms.Form):
    N = forms.FloatField(label='Nitrogen')
    P = forms.FloatField(label='Phosphorus')
    K = forms.FloatField(label='Potassium')
    temperature = forms.FloatField(label='Temperature')
    humidity = forms.FloatField(label='Humidity')
    ph = forms.FloatField(label='pH')
    rainfall = forms.FloatField(label='Rainfall')
