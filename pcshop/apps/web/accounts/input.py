def input_get_input(self):
    
    _i = self.request.GET
    user = self.request.user

    i = {
        'user': user,
    }
    if user.is_authenticated:
        i['user_fullname'] = user.fullname
        
    return i


def input_post_input(self):

    _i = self.request.POST

    i = {
        'next': _i.get('next'),
        'fullname': _i.get('fullname'),
        'email': _i.get('email'),
        'password': _i.get('password'),
        'password1': _i.get('password1'),
    }

    return i