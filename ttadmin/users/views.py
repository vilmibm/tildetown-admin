from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import Townie

# TODO validation functions for final request validation and live js validation
# I refuse to duplicate the logic for validation on the front-end and am going
# to accept round-trip validation costs with long-term caching.

class UserSignupView(TemplateView):
    template_name = 'ttadmin/signup.html'

    def post(self, request):
        print(request.POST)
        # TODO validate
        username = request.POST.get('username')

        displayname = request.POST.get('displayname')

        if displayname is None:
            displayname = username
        else:
            # TODO validate
            pass

        # TODO validate
        pubkey = request.POST.get('pubkey')

        # TODO validate
        email = request.POST.get('email')

        t = Townie(
            username=username,
            displayname=displayname,
            pubkey=pubkey,
            email=email,
        )

        t.set_unusable_password()
        t.save()


        return HttpResponse('LOLOLOLOL')
