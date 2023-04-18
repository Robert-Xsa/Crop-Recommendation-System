from django.shortcuts import render

# Create your views here.
import pickle
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PredictionForm
import pandas as pd

def predict(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            # Load the saved model
            with open('C:/Users/user/Desktop/Dissertation/ML/crop_recommendation_system/crops/recommender_model.pkl', 'rb') as f:
                model = pickle.load(f)

            # Get the input values from the form
            N = form.cleaned_data['N']
            P = form.cleaned_data['P']
            K = form.cleaned_data['K']
            temperature = form.cleaned_data['temperature']
            humidity = form.cleaned_data['humidity']
            ph = form.cleaned_data['ph']
            rainfall = form.cleaned_data['rainfall']
            #Scaling the Input data
            ################################################################Not completed
            #Get the scaler object from the loaded model
            '''scaler = model.scaler
            user ={'N': [N],'P': [P],'K': [K], 'temperature':[temperature],'humidity':[humidity],'ph': [ph],'rainfall':[rainfall],}
            user = pd.DataFrame(user)
            user_scaled = scaler.transform(user)
            predictedion = model.predict(user_scaled)'''
            #####################################################################################
      
        

            # Make a prediction using the loaded model
            prediction = model.predict([[N, P, K, temperature, humidity, ph, rainfall]])

            # Render the prediction template with the result
            return render(request, 'prediction.html', {'prediction': prediction})
    else:
        form = PredictionForm()

    return render(request, 'form.html', {'form': form})
