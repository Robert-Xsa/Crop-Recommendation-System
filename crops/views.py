from django.shortcuts import render

# Create your views here.
import pickle
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PredictionForm
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,PasswordResetForm
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm, UserForm
from django.contrib.auth.models import User
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth.views import PasswordChangeDoneView,PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages




@login_required(login_url='/login/')
def predict(request):
    #user = request.user
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
            with open('C:/Users/user/Desktop/Dissertation/ML/crop_recommendation_system/crops/scaler.pkl', 'rb') as s:
                scaler = pickle.load(s)
            #Get the scaler object from the loaded model
            user_data ={'N': [N],'P': [P],'K': [K], 'temperature':[temperature],'humidity':[humidity],'ph': [ph],'rainfall':[rainfall]}
            user_data = pd.DataFrame(user_data)
            user_scaled = scaler.transform(user_data)
            prediction = model.predict(user_scaled)
      
        

            # Make a prediction using the loaded model
            #Without scaling the user input
            #prediction = model.predict([[N, P, K, temperature, humidity, ph, rainfall]])

            # Render the prediction template with the result
            return render(request, 'prediction.html', {'prediction': prediction})
    else:
        form = PredictionForm()

    return render(request, 'form.html', {'form': form})




def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            message = "Invalid username or password."
    else:
        message = ""
    return render(request, 'login.html', {'message': message})

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    return render(request, 'profile.html')
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def update_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})

def user_signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def password_change_done_view(request):
    return render(request, 'password_change_done.html')

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt',
            )
            messages.success(request, 'Password reset email has been sent. Please check your email.')
            return redirect('login') 
    else:
        form = PasswordResetForm()
    
    return render(request, 'forgot_password.html', {'form': form})

@login_required
def base_map(request):
    return render(request, 'base_map.html')


