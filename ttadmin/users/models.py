import logging
import os
from subprocess import run, CalledProcessError
from tempfile import TemporaryFile

from django.db.models import Model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import TextField, BooleanField, CharField, ForeignKey
from django.template.loader import get_template

from common.mailing import send_email
from help.models import Ticket

logger = logging.getLogger()

SSH_TYPE_CHOICES = (
    ('ssh-rsa', 'ssh-rsa',),
    ('ssh-dss', 'ssh-dss',),
    ('ecdsa-sha2-nistp256', 'ecdsa-sha2-nistp256'),
)

DEFAULT_INDEX_PATH = '/etc/skel/public_html/index.html'

if os.path.exists(DEFAULT_INDEX_PATH):
    DEFAULT_INDEX_PAGE = open(DEFAULT_INDEX_PATH).read().rstrip()
else:
    logger.warning('No default html page found in skel. using empty string.')
    DEFAULT_INDEX_PAGE = ''


KEYFILE_HEADER = """########## GREETINGS! ##########
# Hi! This file is automatically managed by tilde.town. You
# seriously shouldn't change it. If you want to add more public keys that's
# totally fine: you can put them in ~/.ssh/authorized_keys"""


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

    @property
    def home(self):
        return os.path.join('/home', self.username)

    def send_welcome_email(self, admin_name='vilmibm'):
        welcome_tmpl = get_template('users/welcome_email.txt')
        context = {
            'username': self.username,
            'admin_name': admin_name,
        }
        text = welcome_tmpl.render(context)
        from_address = '{}@tilde.town'.format(admin_name)
        success = send_email(self.email, text, subject='tilde.town!',
                             frum=from_address)
        if not success:
            Ticket.objects.create(name='system',
                                  email='root@tilde.town',
                                  issue_type='other',
                                  issue_text='was not able to send welcome email to {} ({})'.format(
                                      self.username,
                                      self.email))

    # managing concrete system state
    def has_modified_page(self):
        """Returns whether or not the user has modified index.html. If they
        don't have one, returns False."""
        index_path = os.path.join(self.home, 'public_html/index.html')
        if not os.path.exists(index_path):
            return False

        index_page = open(index_path).read().rstrip()
        return index_page != DEFAULT_INDEX_PAGE

    def create_on_disk(self):
        """A VERY NOT IDEMPOTENT create function. Originally, I had ambitions
        to have this be idempotent and able to incrementally update a user as
        needed, but decided that was overkill for now."""
        assert(self.reviewed)
        dot_ssh_path = '/home/{}/.ssh'.format(self.username)

        error = _guarded_run(['sudo',
                              'adduser',
                              '--quiet',
                              '--shell={}'.format(self.shell),
                              '--gecos="{}"'.format(self.displayname),
                              '--disabled-password',
                              self.username])
        if error:
            logging.error(error)
            return

        error = _guarded_run(['sudo',
                              'usermod',
                              '-a',
                              '-Gtown',
                              self.username])

        if error:
            logging.error(error)
            return

        # Create .ssh
        error = _guarded_run(['sudo',
                              '--user={}'.format(self.username),
                              'mkdir',
                              dot_ssh_path])
        if error:
            logging.error(error)
            return

    def write_authorized_keys(self):
        # Write out authorized_keys file
        # Why is this a call out to a python script? There's no secure way with
        # sudoers to allow this code to write to a file; if this code was to be
        # compromised, the ability to write arbitrary files with sudo is a TKO.
        # By putting the ssh key file creation into its own script, we can just
        # give sudo access for that one command to this code.
        #
        # We could put the other stuff from here into that script and then only
        # grant sudo for the script, but then we're moving code out of this
        # virtual-env contained, maintainable thing into a script. it's my
        # preference to have the script be as minimal as possible.
        with TemporaryFile(dir="/tmp") as fp:
            fp.write(self.generate_authorized_keys().encode('utf-8'))
            fp.seek(0)
            error = _guarded_run(['sudo',
                                  '--user={}'.format(self.username),
                                  '/opt/bin/create_keyfile.py',
                                  self.username],
                                 stdin=fp)
            if error:
                logging.error(error)

    def generate_authorized_keys(self):
        """returns a string suitable for writing out to an authorized_keys
        file"""
        content = KEYFILE_HEADER
        for pubkey in self.pubkey_set.all():
            if pubkey.key.startswith('ssh-'):
                content += '\n{}'.format(pubkey.key)
            else:
                content += '\n{} {}'.format(pubkey.key_type, pubkey.key)

        return content


class Pubkey(Model):
    key_type = CharField(max_length=50,
                         blank=False,
                         null=False,
                         choices=SSH_TYPE_CHOICES,
    )
    key = TextField(blank=False, null=False)
    townie = ForeignKey(Townie)


@receiver(post_save, sender=Pubkey)
def on_pubkey_post_save(sender, instance, **kwargs):
    instance.townie.write_authorized_keys()


@receiver(pre_save, sender=Townie)
def on_townie_pre_save(sender, instance, **kwargs):
    existing = Townie.objects.filter(username=instance.username)
    if not existing:
        # we're making a new Townie; this means someone just signed up. We
        # don't care at all about their state on disk.
        return

    existing = existing[0]

    if not existing.reviewed and instance.reviewed == True:
        instance.create_on_disk()
        instance.send_welcome_email()
        instance.write_authorized_keys()


def _guarded_run(cmd_args, **run_args):
    """Given a list of args representing a command invocation as well as var
    args to pass onto subprocess.run, run the command and check for an error.
    if there is one, files a helpdesk ticket and returns it. Returns None on
    success."""
    try:
        run(cmd_args,
            check=True,
            **run_args)
    except CalledProcessError as e:
        Ticket.objects.create(name='system',
                              email='root@tilde.town',
                              issue_type='other',
                              issue_text='error while running {}: {}'.format(
                                  cmd_args, e))
        return e


# things to consider:
# * what happens when a user wants their name changed?
#  * it looks like usermod -l and a mv of the home dir can change a user's username.
#  * would hook this into the pre_save signal to note a username change
# * what happens when a user is marked as not reviewed?
#  * does this signal user deletion? Or does literal Townie deletion signal
#    "needs to be removed from disk"? I think it makes the most sense for the
#    latter to imply full user deletion.
#  * I honestly can't even think of a reason to revert a user to "not reviewed"
#    and perhaps it's best to just not make that possible. for now, though, I
#    think I can ignore it.
# * what happens when a user needs to be banned?
#  * the Townie should be deleted via post_delete signal
# * what are things about a user that might change in django and require changes on disk?
#  * username
#  * displayname (only if i start using this?)
#  * ssh key
