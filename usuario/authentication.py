from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

class UsuarioBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            if user.date_deleted is not None:
                raise ValidationError("This user has been deleted and cannot log in.")
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None