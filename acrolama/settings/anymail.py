import os

# Anymail (Mailgun)
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get('MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": os.environ.get('MAILGUN_DOMAIN'),
    "MAILGUN_API_URL": os.environ.get('MAILGUN_API_URL', default='https://api.mailgun.net/v3'),
}
