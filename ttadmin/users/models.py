import os
import re
from subprocess import run, CalledProcessError, PIPE
from tempfile import TemporaryFile

from django.db.models import Model
from django.db.models.signals import pre_save, post_save, post_delete
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

KEYFILE_HEADER = """Hi! This file is automatically managed by tilde.town. You
probably shouldn't change it. If you want to add more public keys that's
totally fine: you can put them in ~/.ssh/authorized_keys"""
TMP_PATH = '/tmp/ttadmin'

ENSURE_PRESENT = 'present'
ENSURE_ABSENT = 'absent'

def user_in_passwd(username):
    """Given a username, returns either the user's line in passwd or None.
    Opens and reads passwd every time. Memoize or something if this becomes an
    issue."""
    with open('/etc/passwd') as passwd:
        for line in passwd:
            if username == line.split(':')[0]:
                return line.rstrip()


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

    # managing concrete system state

    def reconcile(self, ensure):
        assert(self.reviewed)
        dot_ssh_path = '/home/{}/.ssh'.format(self.username)
        if ensure == ENSURE_ABSENT:
            # TODO delete
            # This is manual for now because it very rarely comes up and I want
            # the present case to work.
            pass

        if ensure == ENSURE_PRESENT:
            # TODO handle rename case either with update fields or a rename action
            # Add the user
            result = run(['sudo',
                          'adduser',
                          '--quiet',
                          '--shell={}'.format(self.shell),
                          '--gecos="{}"'.format(self.displayname),
                          '--disabled-password',
                          self.username,],
                         check=True,
            )

            # Create .ssh
            run(['sudo', '--user={}'.format(self.username), 'mkdir', dot_ssh_path])

            # Write out authorized_keys file
            with TemporaryFile(dir="/tmp") as fp:
                fp.write(self.generate_authorized_keys().encode('utf-8'))
                fp.seek(0)
                run(['sudo',
                     '--user={}'.format(self.username),
                     '/opt/bin/create_keyfile.py',
                     self.username],
                    stdin=fp
                )

    def generate_authorized_keys(self):
        """returns a string suitable for writing out to an authorized_keys
        file"""
        content = KEYFILE_HEADER
        pubkeys = Pubkey.objects.filter(townie=self)
        for key in pubkeys:
            if key.startswith('ssh-'):
                content += '\n {}'.format(key.key)
            else:
                content += '\n{} {}'.format(key.key_type, key.key)

        return content


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

@receiver(post_save, sender=Townie)
def post_save_reconcile(sender, instance, **kwargs):
    if not instance.reviewed:
        return
    instance.reconcile(ENSURE_PRESENT)

@receiver(post_delete, sender=Townie)
def post_delete_reconcile(sender, instance, **kwargs):
    if not instance.reviewed:
        # TODO should i actually do this check?
        # I might want to make it such that users can never become un-reviewed.
        return
    instance.reconcile(ENSURE_ABSENT)

# what the puppet module does:
# * creates user account
# * creates home directory
# * creates authorized_keys2
# * adds user to group 'tilde' (why?)
# * sets shell
# * creates .ssh directory
# * creates .irssi directory
# * creates templatized .irssi config file (irssi isn't even default anymore...)
# * creates hardcoded .twurlrc file (why not skel?)
#
# some of this stuff is pointless and the actually required stuff is:
# * create user account (useradd)
# * create home dir (useradd)
# * create .ssh/authorized_keys2 (need functions for this
# * set shell (chsh)
# * create .twurlrc (just use /etc/skel)

# other things to consider:
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
#
# how should this code be structured?
# * within the Townie model, hardcoded
# * outside the Townie model, procedurally
# * within an abstract class
#
# for now my gut says to implement stuff hardcoded in the Townie class but with
# an eye towards generalizing the pattern in some base class for other
# resources as needed.
