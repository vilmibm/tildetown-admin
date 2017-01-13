import re

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import TextField, BooleanField, CharField


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
    pubkey = TextField(blank=False, null=False)
    shell = CharField(max_length=50, default="/bin/bash")
    reviewed = BooleanField(default=False)
    reasons = TextField(blank=True, null=False, default='')
    displayname = CharField(max_length=100, blank=False, null=False)
    pubkey_type = CharField(max_length=15,
                            blank=False,
                            null=False,
                            choices=SSH_TYPE_CHOICES)

    # TODO consider a generic ensure method that syncs this model with the
    # system. there will likely be things besides shell that we want to keep
    # track of in the DB.
    def ensure_shell(self):
        """Runs chsh for the user to set their shell to whatever self.shell
        is."""
        raise NotImplementedError()

@receiver(post_save, sender=Townie)
def sync_system_state(sender, instance, created, **kwargs):
    if created:
        print('TODO would create new user on system')
    else:
        print('TODO would update existing user on system')

    return
