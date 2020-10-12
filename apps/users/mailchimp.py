import os
from mailchimp3 import MailChimp

from .models import User


ACROLAMA_LIST = 'bf3b2c53fa'

key = os.environ.get("MAILCHIMP_KEY")
user = os.environ.get("MAILCHIMP_USER")

client = MailChimp(mc_api=str(key), mc_user=str(user))


def mc_email_list():
    mc_members = client.lists.members.all(ACROLAMA_LIST, get_all=True, fields="members.email_address")['members']
    email_list = [e['email_address'] for e in mc_members]

    return email_list


def mc_missing_users():
    local_users = User.objects.all()
    local_emails = set(a.email for a in local_users)
    mc_emails = set(mc_email_list())
    a = local_emails.difference(mc_emails)
    print(a)

