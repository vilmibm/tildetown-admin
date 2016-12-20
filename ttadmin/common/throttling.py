from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

def throttler(cache):
    def throttle(key):
        nonlocal cache
        last_submission = cache.get(key)
        if last_submission is None\
           or now - last_submission > timedelta(minutes=30):
            cache[key] = now
        else:
            raise ValidationError('you have submitted pretty recently. try again in a bit.')

    return throttle
