"""Forms."""
from django.forms import ModelForm

from .models import User


class UserDeleteForm(ModelForm[User]):  # pylint:disable=unsubscriptable-object
    """User delete form."""

    class Meta:
        """Meta."""

        model = User
        fields: list[str] = []
