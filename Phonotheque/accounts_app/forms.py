from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator

from .models import Profile
from ..common_utilities.FormFieldsFormatMixin import FormFieldsFormatMixin
from ..main_app.models import Collection


class UserRegistrationForm(FormFieldsFormatMixin, forms.ModelForm):
    VALID_NAME_REGEX = r"^([ \u00c0-\u01ffa-zA-Z'\-])+$"  # Jérémie O'Conor-IVANOVäüïöëÿâçéèêîïôčšžñáéíóúü
    INVALID_NAME_ERROR_MESSAGE = "This name format won't work here, buddy."

    first_name = forms.CharField(max_length=35,
                                 validators=(
                                     MinLengthValidator(2),
                                     RegexValidator(regex=VALID_NAME_REGEX, message=INVALID_NAME_ERROR_MESSAGE))
                                 )

    last_name = forms.CharField(max_length=35,
                                validators=(
                                    MinLengthValidator(2),
                                    RegexValidator(regex=VALID_NAME_REGEX, message=INVALID_NAME_ERROR_MESSAGE))
                                )

    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(FormFieldsFormatMixin, forms.ModelForm):
    VALID_NAME_REGEX = r"^([ \u00c0-\u01ffa-zA-Z'\-])+$"  # Jérémie O'Conor-IVANOVäüïöëÿâçéèêîïôčšžñáéíóúü
    INVALID_NAME_ERROR_MESSAGE = "This name format won't work here, buddy."

    first_name = forms.CharField(max_length=35,
                                 validators=(
                                     MinLengthValidator(2),
                                     RegexValidator(regex=VALID_NAME_REGEX, message=INVALID_NAME_ERROR_MESSAGE))
                                 )

    last_name = forms.CharField(max_length=35,
                                validators=(
                                    MinLengthValidator(2),
                                    RegexValidator(regex=VALID_NAME_REGEX, message=INVALID_NAME_ERROR_MESSAGE))
                                )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(FormFieldsFormatMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Profile
        exclude = ('user',)

        widgets = {
            'date_of_birth': forms.SelectDateWidget(
                years=range(datetime.now().year, 1920, -1),
                attrs={'class': "form-control", }
            )
        }


class UserAndProfileDeleteForm(FormFieldsFormatMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        related_profile = Profile.objects.get(pk=self.instance.pk)
        date_of_birth = related_profile.date_of_birth or "Left Empty"
        gender = related_profile.gender or "Left Empty"
        description = related_profile.description or "Left Empty"
        self.fields['date_of_birth'] = forms.CharField(max_length=35, initial=date_of_birth)
        self.fields['gender'] = forms.CharField(max_length=35, initial=gender)
        self.fields['description'] = forms.CharField(max_length=35, initial=description)

        self._init_bootstrap_form_controls()  # format fields

        for (field_name, field) in self.fields.items():
            field.widget.attrs['readonly'] = True
            field.help_text = None

    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_superuser', 'is_active', 'user_permissions', 'groups', 'last_login')

    def save(self, commit=True):
        favourite_albums = Collection.objects.filter(album__collection__user=self.instance)
        favourite_albums.delete()

        linked_profile = User.objects.get(pk=self.instance.pk)
        linked_profile.delete()

        self.instance.delete()  # to remove record from DB
        return self.instance
