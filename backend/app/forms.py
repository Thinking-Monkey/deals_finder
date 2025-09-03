from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CCUser


class CCUserCreationForm(UserCreationForm):

    class Meta:
        model = CCUser


class CCUserChangeForm(UserChangeForm):

    class Meta:
        model = CCUser