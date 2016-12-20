from django.db.models import Model, TextField, CharField, DateTimeField


class GuestbookMessage(Model):
    name = CharField(blank=False, null=False, max_length=50)
    msg = TextField(blank=False, null=False, max_length=500)
    datetime_created = DateTimeField(auto_now_add=True)
