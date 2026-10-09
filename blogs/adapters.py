from urllib.parse import urljoin

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.urls import reverse


class SiteAccountAdapter(DefaultAccountAdapter):
    """Build account action links from the configured canonical site origin."""

    def _build_site_url(self, path):
        """Build an absolute URL using the configured SITE_URL."""
        site_url = f"{settings.SITE_URL.rstrip('/')}/"
        return urljoin(site_url, path.lstrip("/"))

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Generate the email confirmation URL."""
        path = reverse(
            "account_confirm_email",
            args=[emailconfirmation.key],
        )
        return self._build_site_url(path)

    def get_reset_password_from_key_url(self, key):
        """Generate the password reset URL from the combined allauth key."""
        uidb36, separator, token = key.partition("-")

        if not separator or not uidb36 or not token:
            raise ValueError("Invalid password reset key format.")

        path = reverse(
            "account_reset_password_from_key",
            kwargs={
                "uidb36": uidb36,
                "key": token,
            },
        )

        return self._build_site_url(path)
