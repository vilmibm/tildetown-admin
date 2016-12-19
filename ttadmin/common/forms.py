from random import shuffle

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
