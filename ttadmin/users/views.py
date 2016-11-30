import re

from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailField, Textarea, ChoiceField, BooleanField
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse

from .forms import TownieForm
from .models import Townie

class SignupView(FormView):
    form_class = TownieForm
    template_name = 'users/signup.html'
    # TODO reverse
    success_url = '/thanks'

    def form_valid(self, form):

        #t = Townie(
        #    username=username,
        #    displayname=displayname,
        #    pubkey=pubkey,
        #    email=email,
        #)

        #t.set_unusable_password()
        #t.save()

        return super().form_valid(form)


# TODO add template for this once i've fixed template directories
class ThanksView(TemplateView):
    template_name = 'users/thanks.html'
