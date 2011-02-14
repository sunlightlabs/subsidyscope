import django.forms

class RcsTextFieldFormField(django.forms.Field):
    """docstring for RcsTextFieldFormField"""
    def __init__(self, *args, **kwargs):
        super(RcsTextFieldFormField, self).__init__(*args, **kwargs)
        
        
    def clean(self, value):
        return value