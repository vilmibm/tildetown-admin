from datetime import datetime, timedelta
from random import shuffle

from django.core.exceptions import ValidationError
from django.forms import ChoiceField

CAPTCHA_CHOICES = [('two', 'zorp borp'),
                   ('three', 'quop bop'),
                   ('four', 'NO, I AM NOT A ROBOT'),
                   ('five', 'crackle zop'),
                   ('six', '*rusty screech*'),
                   ('seven', 'mother, give me legs')]
shuffle(CAPTCHA_CHOICES)
CAPTCHA_CHOICES.insert(0, ('one', 'beep boop'),)
NOT_A_ROBOT = 'four'

def validate_captcha(captcha):
    if captcha != NOT_A_ROBOT:
        raise ValidationError('Are you sure you are not a robot?')


class CaptchaField(ChoiceField):
    def __init__(self):
        super().__init__(choices=CAPTCHA_CHOICES,
                         label='are you a robot?',
                         help_text='pick the response that indicates whether or not you are a robot.',
                         validators=(validate_captcha,))


# this should go in something like redis. I refuse, however, to involve redis
# in all of this until i have 2-3 more usecases.
def throttler(cache):
    def throttle(key):
        nonlocal cache
        last_submission = cache.get(key)
        now = datetime.now()
        if last_submission is None\
           or now - last_submission > timedelta(minutes=30):
            cache[key] = now
        else:
            raise ValidationError('you have submitted pretty recently. try again in a bit.')

    return throttle
