from django.db.models import Model, TextField, EmailField, CharField

ISSUE_TYPE_CHOICES = (
    ('logging_in', 'help logging in'),
    ('concern_site', 'concern about the site'),
    ('concern_user', 'concern about another user'),
    ('package', 'install a package'),
    ('question', 'just a question',),
    ('other', 'something else'),
)

ISSUE_STATUS_CHOICES = (
    ('triage', 'to triage'),
    ('acked', 'acknowledged'),
    ('waiting', 'waiting to hear from submitter'),
    ('completed', 'nothing more to do'),
)

class Ticket(Model):
    name = TextField(blank=False, null=False)
    email = EmailField(blank=False, null=False)
    issue_type = CharField(choices=ISSUE_TYPE_CHOICES,
                           blank=False,
                           null=False,
                           max_length=50)
    issue_text = TextField(blank=False, null=False)
    issue_status = CharField(choices=ISSUE_STATUS_CHOICES,
                             blank=False,
                             null=False,
                             max_length=50,
                             default=ISSUE_STATUS_CHOICES[0][0])

    def cycle_state(self):
        current_state = self.issue_status
        current_index = (i for i,v
                         in enumerate(ISSUE_STATUS_CHOICES)
                         if v[0] == self.issue_status).__next__()
        next_index = current_index + 1
        if next_index > len(ISSUE_STATE_CHOICES) - 1:
            next_index = 0
        self.issue_status = ISSUE_STATUS_CHOICES[next_index][0]


    def __str__(self):
        return '{} from {}'.format(self.issue_type, self.name)
