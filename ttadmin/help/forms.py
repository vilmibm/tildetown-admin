from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailField, Textarea, ChoiceField

from common.forms import CaptchaField
from .models import ISSUE_TYPE_CHOICES


# this should go in something like redis. I refuse, however, to involve redis
# in all of this until i have 2-3 more usecases.
submission_throttle = {}

def throttle_submission(email):
    last_submission = submission_throttle.get(email)
    now = datetime.now()
    if last_submission is None\
       or now - last_submission > timedelta(minutes=30):
        submission_throttle[email] = datetime.now()
    else:
        raise ValidationError('you have submitted pretty recently. try again in a bit.')

def validate_issue_text(text):
    if len(text) == 0:
        raise ValidationError('please describe yr issue')
    if len(text) > 500:
        raise ValidationError('too long')


class TicketForm(Form):
    name = CharField(label='name',
                     help_text='your tilde.town username if you have one, otherwise just something to address you as'
    )
    email = EmailField(
        help_text='only used to message you about this ticket and nothing else.',
        label='e-mail',
    )
    issue_type = ChoiceField(
        choices=ISSUE_TYPE_CHOICES,
        label='type of issue',
        help_text='the type of issue that best describes your problem'
    )
    issue_text = CharField(
        widget=Textarea,
        label="what's up?",
        help_text='describe your issue (in 500 characters or less)',
        validators=(validate_issue_text,),
    )
    captcha = CaptchaField()

    def clean(self):
        result = super().clean()

        throttle_submission(result['email'])

        if self.errors:
            raise ValidationError('oops, looks like there were some problems below.')

        return result
