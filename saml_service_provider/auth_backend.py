from django.contrib.auth import get_user_model


class SAMLServiceProviderBackend(object):

    def authenticate(self, saml_authentication=None):
        User = get_user_model()
        if not saml_authentication:  # Using another authentication method
            return None

        if saml_authentication.is_authenticated():
            attributes = saml_authentication.get_attributes()
            try:
                user = User.objects.get(username=saml_authentication.get_nameid())
            except User.DoesNotExist:
                user = User(username=saml_authentication.get_nameid())
                user.set_unusable_password()
                user.first_name = attributes['First name'][0]
                user.last_name = attributes['Last name'][0]
                user.save()
            return user
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
