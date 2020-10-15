import os
import requests

import hashlib  # A standard library that does hashes

from mailchimp3 import MailChimp

from booking.models import Book
from users.models import User

ACROLAMA_LIST = 'bf3b2c53fa'

key = os.environ.get("MAILCHIMP_KEY")
user = os.environ.get("MAILCHIMP_USER")

# You are encouraged to specify a User-Agent for requests to the MailChimp
# API. Headers can be specified using the ``request_headers`` parameter.
headers = requests.utils.default_headers()
headers['User-Agent'] = 'Adrian Garate (adrian@acrolama.com)'

client = MailChimp(mc_api=str(key), mc_user=str(user), request_headers=headers)


def get_hash_email(email):
    # The following is in .lower() case because mailchimp forms
    # hashes from lowercase strings.
    # The .encode() method tagged on the end encodes it as a byte literal
    email = email.lower().encode(encoding='utf-8')

    # This uses the hashlib library to make the hash. The .hexdigest()
    # seems to be about equivalent to str()
    hashed_email = hashlib.md5(email).hexdigest()
    return hashed_email


def get_all_mc_email_set():
    mc_members = client.lists.members.all(ACROLAMA_LIST, get_all=True, fields="members.email_address")['members']
    return set(dic['email_address'] for dic in mc_members)


def get_mc_email_tag_set(email):
    tags = client.lists.members.tags.all(list_id=ACROLAMA_LIST, subscriber_hash=get_hash_email(email))['tags']
    return set(dic['name'] for dic in tags)


def tags_from_email_set(email):
    bookings_user = Book.objects.filter(user__email=email)
    tags = set()
    for book in bookings_user:
        if book.event.category in ("CY", "CA", "WS"):
            tags.add(book.event.get_category_display() + ' ' + book.event.level.get_name_display())
        elif book.event.category == "FT":
            tags.add(book.event.title)

    return tags


# def update_missing_tag(email):
#     get_mc_email_tag


def check_email_in_mc(user):
    if user.email in get_all_mc_email_set():
        return True
    else:
        return False


def mc_missing_users_list():
    local_users = User.objects.all()
    local_emails = set(a.email for a in local_users)
    mc_emails = get_all_mc_email_set()
    a = local_emails.difference(mc_emails)
    return list(a)

