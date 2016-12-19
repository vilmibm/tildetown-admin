from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import TicketForm
from .models import Ticket

class TicketView(FormView):
    form_class = TicketForm
    template_name = 'help/tickets.html'

    def form_valid(self, form):
        del form.cleaned_data['captcha']
        t = Ticket.objects.create(**form.cleaned_data)
        return redirect('help:ticket_submitted')

class TicketSubmittedView(TemplateView):
    template_name = 'help/ticket_submitted.html'
