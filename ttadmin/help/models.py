from django.db.models import Model, TextField, EmailField, CharField

ISSUE_TYPE_CHOICES = (
    ('logging_in', 'help logging in'),
    ('concern_site', 'concern about the site'),
    ('concern_user', 'concern about another user'),
    ('package', 'install a package'),
    ('question', 'just a question',),
    ('other', 'something else'),
)


class Ticket(Model):
    name = TextField(blank=False, null=False)
    email = EmailField(blank=False, null=False)
    issue_type = CharField(choices=ISSUE_TYPE_CHOICES,
                           blank=False,
                           null=False,
                           max_length=50)
    issue_text = TextField(blank=False, null=False)

    def __str__(self):
        return '{} from {}'.format(self.issue_type, self.name)
