from django.views.generic.edit import FormView

from .forms import TicketForm
from .models import Ticket

class TicketView(FormView):
    form_class = TicketForm
    template_name = 'help/tickets.html'

    def form_valid(self, form):
        # TODO
        pass
