from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm

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
            return redirect('login')  # Make sure you have this URL pattern named 'login'

        return render(request, self.template_name, {"form": form_instance})
