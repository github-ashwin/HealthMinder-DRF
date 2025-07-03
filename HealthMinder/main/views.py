from django.shortcuts import render
from django.views.generic import View
from main.forms import SignUpForm
# Create your views here.


from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User  # Replace if you're using a custom user model
from .forms import SignUpForm  # Your custom form

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

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
                return render(request, self.template_name, {"form": form_instance})

            # Proceed to create the user
            username = data.get('username')
            password = data.get('password')

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            messages.success(request, "Registration successful. Please login.")
            return redirect('login')  # Replace 'login' with your login URL name

        return render(request, self.template_name, {"form": form_instance})


