from django.http import HttpResponse
from django.views.generic import TemplateView

class UserSignupView(TemplateView):
    template_name = 'ttadmin/signup.html'

    def post(self, request):
        return HttpResponse('LOLOLOLOL')
