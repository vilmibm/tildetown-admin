from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailField, Textarea, ChoiceField

from common.forms import CaptchaField, throttler


submission_throttle = {}
throttle_submission = throttler(submission_throttle)


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

        if self.errors:
            raise ValidationError('oops, looks like there were some problems below.')

        throttle_submission(result['name'])

        return result
