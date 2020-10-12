# importing django modules
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
"""
    Six is a python library that makes the difference between the python versions smooth.
"""

# function to generate token for email verification link
class TokenGenerator(PasswordResetTokenGenerator):
    """
        Here we will generate a unique token to be sent as part of URL.
    """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(user.email) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()