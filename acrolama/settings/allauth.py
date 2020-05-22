from .base import *

# Authentication allauth "allauth.socialaccount"
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

# Config https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = os.environ.get("ACCOUNT_AUTHENTICATION_METHOD", default="email")
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = int(os.environ.get("ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS", default=3))
ACCOUNT_EMAIL_REQUIRED = os.environ.get("ACCOUNT_EMAIL_REQUIRED", default=True)
ACCOUNT_EMAIL_VERIFICATION = os.environ.get("ACCOUNT_EMAIL_VERIFICATION", default=True)
ACCOUNT_UNIQUE_EMAIL = os.environ.get("ACCOUNT_UNIQUE_EMAIL", default=True)
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = int(os.environ.get("ACCOUNT_LOGIN_ATTEMPTS_LIMIT", default=5))
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = os.environ.get("ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION", default=True)
ACCOUNT_SESSION_REMEMBER = os.environ.get("ACCOUNT_SESSION_REMEMBER", default=True)
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = os.environ.get("ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE", default=False)
ACCOUNT_SIGNUP_FORM_CLASS = os.environ.get("ACCOUNT_SIGNUP_FORM_CLASS")
ACCOUNT_USERNAME_REQUIRED = os.environ.get("ACCOUNT_USERNAME_REQUIRED", default=False)
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_FORMS = {
    "signup": "users.forms.CustomSignupForm",
}

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
