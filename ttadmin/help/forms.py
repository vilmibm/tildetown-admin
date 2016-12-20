from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailField, Textarea, ChoiceField

from common.forms import CaptchaField, throttler
from .models import ISSUE_TYPE_CHOICES


submission_throttle = {}
throttle_submission = throttler(submission_throttle)


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

        if self.errors:
            raise ValidationError('oops, looks like there were some problems below.')

        throttle_submission(result['email'])

        return result
