from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class tokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestimp):
        return (
            text_type(user.pk) + text_type(timestimp)
        )



generate_token = tokenGenerator()