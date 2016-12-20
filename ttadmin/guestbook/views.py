from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import GuestbookForm
from .models import GuestbookMessage


class GuestbookView(FormView):
    form_class = GuestbookForm
    template_name = 'guestbook/guestbook.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['messages'] = GuestbookMessage.objects.order_by('-datetime_created')
        return ctx

    def form_valid(self, form):
        del form.cleaned_data['captcha']
        t = GuestbookMessage.objects.create(**form.cleaned_data)
        return redirect('guestbook:guestbook')
