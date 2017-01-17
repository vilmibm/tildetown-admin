import re

from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import Form, CharField, EmailField, Textarea, ChoiceField, BooleanField
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import TownieForm
from .models import Townie, Pubkey

class SignupView(FormView):
    form_class = TownieForm
    template_name = 'users/signup.html'

    @transaction.atomic
    def form_valid(self, form):
        del form.cleaned_data['captcha']
        del form.cleaned_data['aup']
        pubkey = Pubkey(key=form.cleaned_data.pop('pubkey'),
                        key_type=form.cleaned_data.pop('pubkey_type'))

        t = Townie(**form.cleaned_data)
        if not getattr(t, 'displayname'):
            t.displayname = t.username
        t.set_unusable_password()
        t.save()
        pubkey.townie = t
        pubkey.save()
        return redirect('users:thanks')


class ThanksView(TemplateView):
    template_name = 'users/thanks.html'
