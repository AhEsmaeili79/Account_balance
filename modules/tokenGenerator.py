from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone

class ExpiringTokenGenerator(PasswordResetTokenGenerator):
    def __init__(self, expiry_time=300):  # Token expires in 5 minutes (300 seconds)
        self.expiry_time = expiry_time
        super().__init__()

    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.password)  # Custom hash value

    def check_token(self, user, token):
        """
        Check whether the token is valid and not expired.
        """
        try:
            timestamp = self._get_timestamp(token)
        except (TypeError, ValueError):
            return False

        # Check if the token is expired
        if (timezone.now() - timezone.datetime.fromtimestamp(timestamp, timezone.utc)).total_seconds() > self.expiry_time:
            return False

        return super().check_token(user, token)

    def _get_timestamp(self, token):
        """
        Extract the timestamp from the token.
        """
        try:
            parts = token.split('-')
            timestamp = int(parts[1])
        except (IndexError, ValueError):
            raise ValueError('Invalid token')
        return timestamp

# Instantiate the custom token generator with a 5-minute expiry time
expiring_token_generator = ExpiringTokenGenerator(expiry_time=60)
