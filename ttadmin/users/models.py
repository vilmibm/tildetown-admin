from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import TextField, BooleanField


class Townie(User):
    """Both an almost normal Django User as well as an abstraction over a
    system user."""
    pubkey = TextField(blank=False, null=False)
    shell = TextField(max_length=50, default="/bin/bash")
    pending = BooleanField(default=True)

    @property
    def home_path(self):
        return "/home/{}".format(self.username)

    def accept(self):
        """Sets self.pending to False. Indicates the user has been signed up
        after review."""
        self.pending = False

    def ensure_shell(self):
        """Runs chsh for the user to set their shell to whatever self.shell
        is."""
        raise NotImplementedError()

    def __init__(self):
        self.set_unusable_password()
        super().__init__(self)

@receiver(post_save, sender=Townie)
def sync_system_state(sender, instance, created, **kwargs):
    if created:
        print('TODO would create new user on system')
    else:
        print('TODO would update existing user on system')

    return
