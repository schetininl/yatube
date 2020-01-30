# позволяет узнать ссылку на URL по его имени, параметр name функции path
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
        form_class = CreationForm
        success_url = "/auth/login/"
        template_name = "signup.html"