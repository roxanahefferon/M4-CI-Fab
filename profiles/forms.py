from django import forms
from .models import UserProfile


class MyProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Adds placeholders and classes, removes
        labels and sets autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postcode',
            'default_town': 'Town',
            'default_street_address_1': 'Street Address 1',
            'default_street_address_2': 'Street Address 2',
            'default_county': 'County',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] =\
            True
        for field in self.fields:
            if field != 'name':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] =\
                    placeholder
            self.fields[field].widget.attrs['class'] =\
                'profile-form-input'
            self.fields[field].label = False
