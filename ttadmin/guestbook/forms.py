from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailField, Textarea, ChoiceField

from common.forms import CaptchaField


# this should go in something like redis. I refuse, however, to involve redis
# in all of this until i have 2-3 more usecases.
# TODO generalize
submission_throttle = {}

def throttle_submission(name):
    last_submission = submission_throttle.get(name)
    now = datetime.now()
    if last_submission is None\
       or now - last_submission > timedelta(minutes=30):
        submission_throttle[name] = datetime.now()
    else:
        raise ValidationError('you have submitted pretty recently. try again in a bit.')

def validate_msg_text(msg):
    if len(msg) == 0:
        raise ValidationError('message cannot be empty')
    if len(msg) > 500:
        raise ValidationError('too long')


class GuestbookForm(Form):
    name = CharField(label='name!')
    msg = CharField(
        widget=Textarea,
        label="message!",
        validators=(validate_msg_text,),
    )
    captcha = CaptchaField()

    def clean(self):
        result = super().clean()

        throttle_submission(result['name'])

        if self.errors:
            raise ValidationError('oops, looks like there were some problems below.')

        return result
