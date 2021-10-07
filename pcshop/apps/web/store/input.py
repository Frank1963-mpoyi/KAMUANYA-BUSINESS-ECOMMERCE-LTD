def input_get_input(self):
    
    _i = self.request.GET

    i = {
        'user' : self.request.user,
    }

    return i


def input_post_input(self):

    _i = self.request.POST

    i = {
        'user' : self.request.user,

        "fullname"          : _i.get("fullname", ''),
        "phone_number"      : _i.get("phone_number", ''),
        "email"             : _i.get("email", ''),
        "date"              : _i.get("date", ''),
        "message"           : _i.get("message", ''),
        "specialisation"    : _i.get("specialisation", ''),
    }

    return i