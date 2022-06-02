from django.db.models import Q
from pcshop.apps.web.accounts.models import CustomUser


def check_allowed_staff(self):

    staff = {
        'allowed': False,
        'assignee': False,
        'assigner': False,

        'employee': False,
        'supervisor': False,
        'management': False,
        'chief': False,
    }

    user = self.request.user

    if user.is_authenticated:
        if user.user_type == 1:
            staff['allowed']  = 'Y'
            staff['assignee'] = 'Y'

            if user.user_level >= 2:
                staff['employee'] = 'Y'
                staff['supervisor'] = 'Y'

            if user.user_level >= 3:
                staff['assigner'] = 'Y'

                staff['employee'] = 'Y'
                staff['supervisor'] = 'Y'
                staff['management'] = 'Y'
                staff['chief'] = 'Y'

        if user.user_type == 2:
            staff['employee'] = 'Y'

            if user.user_level >= 2:
                staff['supervisor'] = 'Y'

            if user.user_level >= 4:
                staff['management'] = 'Y'

            if user.user_level >= 5:
                staff['chief'] = 'Y'

    return staff


def get_user(username):

    user = CustomUser.objects \
        .filter(
            Q(username = username) |
            Q(email = username) |
            Q(code = username) |
            Q(uuid_code = username)
        ) \
        .exclude(
            Q(bool_deleted = True) |
            Q(is_active = False)
        ) \
        .values(
            'uuid_code', 'token_key', 'code', 'username', 'phone_number', 'country_code', 'fullname', 'id_number','dob',
            'birth_place', 'email', 'profile_pic', 'language', 'user_type', 'user_level', 'last_login', 'is_active',
            'is_staff', 'is_admin', 'is_superuser', 'datetime_created', 'datetime_updated', 'last_updated_by', 'bool_deleted',
        ).first()

    return user