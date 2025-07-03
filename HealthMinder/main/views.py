from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm,LoginForm


def HomeView(request):
    return render(request,'Home.html')

class SignUpView(View):
    template_name = "Signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form_instance = self.form_class(request.POST)

        if form_instance.is_valid():
            data = form_instance.cleaned_data
            email = data.get('email')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
                return render(request, self.template_name, {"form": form_instance})

            username = data.get('username')
            password = data.get('password')

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            messages.success(request, "Registration successful. Please login.")
            return redirect('login')  

        return render(request, self.template_name, {"form": form_instance})
    
class LoginView(View):
    template_name = "Login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form_instance = self.form_class(request.POST)

        if form_instance.is_valid():
            username = form_instance.cleaned_data.get('username')
            password = form_instance.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('home') 
            else:
                messages.error(request, "Invalid username or password.")
        
        return render(request, self.template_name, {"form": form_instance})
    
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')
