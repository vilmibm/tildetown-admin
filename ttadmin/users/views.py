import re

from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailField, Textarea, ChoiceField, BooleanField
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import TownieForm
from .models import Townie

class SignupView(FormView):
    form_class = TownieForm
    template_name = 'users/signup.html'

    def form_valid(self, form):

        # TODO
        #t = Townie(
        #    username=username,
        #    displayname=displayname,
        #    pubkey=pubkey,
        #    email=email,
        #)

        #t.set_unusable_password()
        #t.save()
        return redirect('users:thanks')


# TODO actually fill in this template
class ThanksView(TemplateView):
    template_name = 'users/thanks.html'
