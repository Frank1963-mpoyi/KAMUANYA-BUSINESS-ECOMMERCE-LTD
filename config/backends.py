from django.db.models                                   import Q
from django.contrib.auth                                import get_user_model


User = get_user_model()

class AuthBackend(object):

    supports_object_permissions = True
    supports_anonymous_user     = False
    supports_inactive_user      = False

    def authenticate(self, request, username=None, password=None):

        try:

            user = User.objects \
                .get(
                    (
                        Q(username      = username) |
                        Q(email         = username) |
                        Q(phone_number  = username)
                    ) &
                    (
                        Q(is_active     = True) |
                        Q(bool_deleted  = False)
                    )
                )

        except User.DoesNotExist:

            return None

        return user if user.check_password(str(password)) else None

    def get_user(self, uuid_code):

        try:

            return User.objects \
                .get(
                    Q(pk = uuid_code) &
                    (
                        Q(is_active     = True) &
                        Q(bool_deleted  = False)
                    )
                )

        except User.DoesNotExist:

            return None
