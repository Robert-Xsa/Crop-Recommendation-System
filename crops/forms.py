from django import forms

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
