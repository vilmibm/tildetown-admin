import re

from django.db.models import Model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import TextField, BooleanField, CharField, ForeignKey
from django.template.loader import get_template

from common.mailing import send_email
from help.models import Ticket

SSH_TYPE_CHOICES = (
    ('ssh-rsa', 'ssh-rsa',),
    ('ssh-dss', 'ssh-dss',),
)


class Townie(User):
    """Both an almost normal Django User as well as an abstraction over a
    system user."""
    class Meta:
        verbose_name = 'Townie'
        verbose_name_plural = 'Townies'
    shell = CharField(max_length=50, default="/bin/bash")
    reviewed = BooleanField(default=False)
    reasons = TextField(blank=True, null=False, default='')
    displayname = CharField(max_length=100, blank=False, null=False)

    def send_welcome_email(self, admin_name='vilmibm'):
        welcome_tmpl = get_template('users/welcome_email.txt')
        context = {
            'username': self.username,
            'admin_name': admin_name,
        }
        text = welcome_tmpl.render(context)
        from_address = '{}@tilde.town'.format(admin_name)
        success = send_email(self.email, text, subject='tilde.town!', frum=from_address)
        if not success:
            Ticket.objects.create(name='system',
                                  email='root@tilde.town',
                                  issue_type='other',
                                  issue_text='was not able to send welcome email to {} ({})'.format(
                                      self.username,
                                  self.email))

class Pubkey(Model):
    key_type = CharField(max_length=50,
                         blank=False,
                         null=False,
                         choices=SSH_TYPE_CHOICES,
    )
    key = TextField(blank=False, null=False)
    townie = ForeignKey(Townie)


@receiver(pre_save, sender=Townie)
def on_townie_pre_save(sender, instance, **kwargs):
    existing = Townie.objects.filter(username=instance.username)
    if not existing: # we're making a new user
        return

    if not existing[0].reviewed and instance.reviewed == True:
        instance.send_welcome_email()
