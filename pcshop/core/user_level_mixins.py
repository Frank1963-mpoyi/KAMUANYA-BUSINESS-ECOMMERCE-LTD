from django.contrib.auth import get_user_model


User = get_user_model()

class UserLevelMixin(object):

    def dispatch(self, request, *args, **kwargs):

        user_type = self.request.user.user_type

        btk_user_type = 'MTC'   # Mpoyi Tshibuyi Company STAFF
        srb_user_type = 'HPT'   # Tshibuyi Hospital Company  STAFF
        cus_user_type = 'CUS'   # CUSTOMERS  - 'CUS-GEN-1' ==> GENERIC CUSTOMER

        cus_level = self.request.user.user_level         # CUSTOMER LEVEL OR CLIENT
        ret_level = self.request.user.user_level         # RETAILER LEVEL - SEE LIST BUT CAN'T EDIT
        emp_type = self.request.user.user_level         # EMPLOYEE / STORE ATTENDANT / AGENT / REPORT LEVEL
        mgn_type = self.request.user.user_level         # MANAGEMENT LEVEL
        top_type = self.request.user.user_level         # OWNER / TOP MANAGEMENT LEVEL

        user_type_check = (self.permission_needed[0:3])
        user_depart_check = (self.permission_needed[4:7])
        user_level_check = int(self.permission_needed[8:9])

        user_authorised = 'N'

        allowed_user_type = None

        if user_type == 1:
            allowed_user_type = [btk_user_type, srb_user_type, cus_user_type]

        if user_type == 2:
            allowed_user_type = [srb_user_type, cus_user_type]

        if user_type == 3:
            allowed_user_type = [cus_user_type]

        # MTC STAFF - CHECKS
        if user_type_check in allowed_user_type:
            if cus_level >= user_level_check:
                user_authorised = 'Y'

            if ret_level >= user_level_check:
                user_authorised = 'Y'

            if emp_type >= user_level_check:
                user_authorised = 'Y'

            if mgn_type >= user_level_check:
                user_authorised = 'Y'

            if top_type >= user_level_check:
                user_authorised = 'Y'

        #  Tshibuyi Hospital Company STAFF - CHECKS
        if user_type_check in allowed_user_type:
            if cus_level >= user_level_check:
                user_authorised = 'Y'

            if ret_level >= user_level_check:
                user_authorised = 'Y'

            if emp_type >= user_level_check:
                user_authorised = 'Y'

            if mgn_type >= user_level_check:
                user_authorised = 'Y'

            if top_type >= user_level_check:
                user_authorised = 'Y'

        # CUSTOMERS - CHECKS
        if user_type_check in allowed_user_type:
            if cus_level >= user_level_check:
                user_authorised = 'Y'

        if not self.permission_needed:
            raise NotImplementedError(
                '{0} is missing the implementation of the user_level_check() method.'.format(self.__class__.__name__)
                )

        if user_authorised != 'Y':
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)