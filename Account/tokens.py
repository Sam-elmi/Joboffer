from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{user.password}{user.last_login}{user.is_active}{timestamp}"


account_activation_token = EmailVerificationTokenGenerator()
