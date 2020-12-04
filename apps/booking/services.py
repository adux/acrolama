import datetime
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext as _

# Email
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist

from booking.models import Book, Attendance, AboCounter, BOOKINGSTATUS, Quotation
from project.models import Event, TimeLocation, Irregularity
from accounting.models import Invoice

from booking.utils import get_weekday_dates_for_period


def get_book(book):
    # If its str or int treat it as id
    if isinstance(book, (str, int)):
        book_pk = int(book)
    else:
        return book

    # if its a id get the book
    if book_pk:
        return Book.objects.get(pk=book_pk)


def book_is_paid(book):
    """
    To check if a book is paid we need to differenciate how its price_option works
    For Cycles for example one would need to go to its first booking to see the related invoice there
    """
    book = get_book(book)

    if book.invoice:
        if book.invoice.status == "PY":
            return True
        else:
            return False
    else:
        if check_abocounter(book.id):
            new_book_id = get_first_book_abocounter(book.id)
            book_is_paid(new_book_id)
        else:
            return False


def get_event(event):
    # If its str or int treat it as id
    if isinstance(event, (str, int)):
        event_pk = int(event)
    else:
        return event

    # if its a id get the book
    if event_pk:
        return Event.objects.get(pk=event_pk)


def get_timelocation(tl):
    # If its str or int treat it as id
    if isinstance(tl, (str, int)):
        tl_pk = int(tl)
    else:
        return tl

    # if its a id get the book
    if tl_pk:
        return TimeLocation.objects.get(pk=tl_pk)


def get_location_from_timeoption(timeoptions, event):
    if timeoptions.count() > 1:
        return False
    else:
        event = get_event(event)
        timelocations_qs = event.time_locations.all()
        filteredTimeLocation_qs = timelocations_qs.filter(time_options__in=timeoptions)
        if filteredTimeLocation_qs.count() > 1:
            return False
        else:
            location = filteredTimeLocation_qs.last().location
            if location is not None:
                return location
            else:
                return False


def attendance_toggle_check(id, position):
    attendance = Attendance.objects.get(pk=id)
    attendance.attendance_check[position] = not attendance.attendance_check[position]
    attendance.save()


def update_book_status(book, status):
    book = get_book(book)
    if status in ("PA", "Participant"):
        book.status = "PA"
        book.save()
    elif status in ("CA", "Canceled"):
        book.status = "CA"
        book.save()


def create_invoice_from_book(book):
    book = get_book(book)

    obj = Invoice()
    obj.balance = "CR"  # Credit
    obj.book = book
    obj.status = "PE"   # Pending
    obj.to_pay = int(book.price.price_chf)
    # Default 10 days to pay
    obj.pay_till = datetime.datetime.now().date() + datetime.timedelta(days=book.price.days_till_pay)
    obj.notes = "\n Automatic created Invoice"
    obj.save()


def create_attendance_from_book(book):
    """
    Creates an Attendance to a particular booking
    """
    # Get a book
    book = get_book(book)

    # Create Attendance
    obj = Attendance()
    obj.book_id = book.id
    obj.attendance_date = []
    obj.attendance_check = []

    if not hasattr(book, "bookdateinfo"):
        # Get time infos
        start = book.event.event_startdate
        end = book.event.event_enddate
        times = book.times.all()
        for to in times:
            if to.regular_day is None:
                # If its not a Cycle put first day of Event as Attendance
                obj.attendance_date.append(book.event.event_startdate)
                obj.attendance_check.append("False")
            else:
                # If it's a Cycle get all the dates from start to end and add
                num = to.regular_day
                li = get_weekday_dates_for_period(start, end, int(num))
                obj.attendance_date.extend(li)
                for time in li:
                    obj.attendance_check.append("False")
    else:
        # If a Single Date is selected build the Attendance with it.
        obj.attendance_date.append(book.bookdateinfo.single_date)
        obj.attendance_check.append("False")

    obj.save()


def check_abocounter(bookid):
    return AboCounter.objects.filter(data__last_book=str(bookid)).exists()


def reduce_abocounter(bookid):
    obj = AboCounter.objects.get(data__last_book=str(bookid))
    obj.data['count'] -= 1
    obj.save()


def create_abocounter_from_book(book):
    AboCounter.objects.create(data={'first_book': str(book.id), 'last_book': str(book.id), 'count': book.price.cycles})


def update_lastbook_abocounter(bookid, newbookid):
    obj = AboCounter.objects.get(data__last_book=str(bookid))
    obj.data['last_book'] = str(newbookid)
    obj.save()


def get_count_abocounter_of_book(bookid):
    return AboCounter.objects.get(data__last_book=str(bookid)).data['count']


def get_first_book_abocounter(bookid):
    counter = AboCounter.objects.get(data__last_book=str(bookid))
    return counter.data['first_book']


def inform_book(request, instance, book):

    # If the Price Option is an Single Cycle Abo
    if book.price.cycles < 2:
        # Create the Invoice
        try:
            create_invoice_from_book(instance)
        except Exception as e:
            messages.add_message(
                request, messages.WARNING, _("Error creating Invoice: " + str(e)),
            )
        else:
            messages.add_message(request, messages.SUCCESS, _("Invoice Created"))

        # Create the attendance list
        try:
            create_attendance_from_book(instance)
        except Exception as e:
            messages.add_message(
                request, messages.WARNING, _("Error creating Attendance: " + str(e)),
            )
        else:
            messages.add_message(request, messages.SUCCESS, _("Attendance created"))

        # Send the Informed Email
        if book.informed_at is None:
            try:
                book_send_informed(instance)
            except Exception as e:
                messages.add_message(request, messages.ERROR, _("Error Email: " + str(e)))
            else:
                messages.add_message(request, messages.SUCCESS, _("Informed email sent."))
                instance.informed_at = datetime.datetime.now()

        # If the email was already sent
        else:
            messages.add_message(request, messages.INFO, _("Email sent: " + str(book.informed_at)))

    # If its a Multi Cycle Abo
    else:

        # Check if it has doesn't have a counter
        if not check_abocounter(book.id):

            # Create the Counter for Abos
            create_abocounter_from_book(book)
            reduce_abocounter(book.id)

            # Create the Invoice
            try:
                create_invoice_from_book(instance)
            except Exception as e:
                messages.add_message(
                    request, messages.WARNING, _("Error creating Invoice: " + str(e)),
                )
            else:
                messages.add_message(request, messages.SUCCESS, _("Invoice Created"))

            # Create the Attendance
            try:
                create_attendance_from_book(instance)
            except Exception as e:
                messages.add_message(
                    request, messages.WARNING, _("Error creating Attendance: " + str(e)),
                )
            else:
                messages.add_message(request, messages.SUCCESS, _("Attendance created"))

            # Send New Book Email
            if book.informed_at is None:
                try:
                    book_send_informed(instance)
                except Exception as e:
                    messages.add_message(request, messages.ERROR, _("Error Email: " + str(e)))
                else:
                    messages.add_message(request, messages.SUCCESS, _("Informed email sent."))
                    # If email send correctly register
                    instance.informed_at = datetime.datetime.now()
            else:
                messages.add_message(request, messages.INFO, _("Email sent: " + str(book.informed_at)))

        # If it has a counter
        else:
            # Reduce the Counter
            reduce_abocounter(book.id)

            # Send a Reminder
            if book.informed_at is None:
                try:
                    book_send_reminder(instance)
                except Exception as e:
                    messages.add_message(request, messages.ERROR, _("Error Email: " + str(e)))
                else:
                    messages.add_message(request, messages.SUCCESS, _("Reminder email sent."))
                    instance.informed_at = datetime.datetime.now()
            else:
                messages.add_message(request, messages.INFO, _("Email sent: " + str(book.informed_at)))

            # Create the attendance list
            try:
                create_attendance_from_book(instance)
            except Exception as e:
                messages.add_message(
                    request, messages.WARNING, _("Error creating Attendance: " + str(e)),
                )
            else:
                messages.add_message(request, messages.SUCCESS, _("Attendance created"))

            # If the Invoice of the First Book is paid then set as Participant

            first_book_id = get_first_book_abocounter(book.id)
            invoice_first_book = Invoice.objects.get(book=first_book_id)
            if invoice_first_book.status == "PY":
                update_book_status(book.id, "PA")
            else:
                messages.add_message(
                    request, messages.WARNING, _("First Booking not paid.")
                )


def create_next_book(book, status):
    """
    Gets and Workshop Booking and creates the next based on cycle
    """
    obj = Book()
    obj.pk = None
    obj.id = None
    # Event resolved below
    obj.user = book.user
    obj.price = book.price
    # Times resolved below
    obj.note = "\nAutomatic created booking, please report if error."

    # Resolve Status
    if status in BOOKINGSTATUS:
        obj.status = status
    else:
        obj.status = "PE"

    # Reset cycle num if needed
    if (book.event.cycle + 1) > 12:
        cycle = 1
    else:
        cycle = book.event.cycle + 1

    # Resolve Event
    # Exceptions like Multile or Not exist can raise
    # https://docs.python.org/3/glossary.html#term-eafp
    old_event = book.event
    new_event = Event.objects.filter(
        project=old_event.project,
        level=old_event.level,
        category=old_event.category,
        event_startdate__gt=old_event.event_enddate,
    ).get(cycle=cycle)

    obj.event = new_event

    # Resolve Times
    times_pk = []
    for to in book.times.all():
        times_pk.append(to.pk)

    # Need to Save before adding the m2m times
    obj.save()

    for x in times_pk:
        obj.times.add(x)

    return obj


def create_quotation(form, count):

    obj = Quotation()  # gets new object
    obj.event = form.cleaned_data["event"]
    obj.time_location = form.cleaned_data["time_location"]

    # Costs
    obj.related_rent = form.cleaned_data["related_rent"]

    # Revenue
    obj.total_attendees = count
    obj.direct_revenue = form.cleaned_data["direct_revenue"]

    # Profit
    obj.fix_profit = form.cleaned_data["fix_profit"]
    obj.admin_profit = form.cleaned_data["admin_profit"]
    obj.partner_profit = form.cleaned_data["partner_profit"]

    obj.save()

    teachers = form.cleaned_data["teachers"]
    obj.teachers.add(*teachers)

    direct_costs = form.cleaned_data["direct_costs"]
    dc = []

    for descriptor in direct_costs:
        descriptor.split(" ")
        dc.append(descriptor[0])

    obj.direct_costs.add(*dc)

    obj.save()


def book_send_registered(book):
    sender = "notmonkeys@acrolama.com"
    bcc = ["acrolama@acrolama.com"]
    subject = "Acrolama - Booking received - " + str(book.event.title)
    to = [book.user.email]

    p = {
        "event": book.event,
        "user": book.user,
    }

    msg_plain = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_registration.txt", p,)
    msg_html = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_registration.html", p,)

    msg = EmailMultiAlternatives(subject, msg_plain, sender, to, bcc)
    msg.attach_alternative(msg_html, "text/html")
    msg.send()


def book_send_informed(book):
    """
    Signals could give Error cause you can call them from wherever.
    Save slows down.
    https://stackoverflow.com/questions/2809547/creating-email-templates-with-django
    Theres another Method with Multi wich helps for headers if needed
    """
    sender = "notmonkeys@acrolama.com"
    bcc = ["acrolama@acrolama.com"]
    subject = "Acrolama - Confirmation - " + str(book.event.title)
    to = [book.user.email]

    irregularities = Irregularity.objects.filter(event__slug=book.event.slug)

    times = book.times.all()
    location = get_location_from_timeoption(times, book.event)

    p = {
        "book": book,
        "event": book.event,
        "user": book.user,
        "price": book.price,
        "referenznum": book.invoice.referral_code,
        "pay_till": book.invoice.pay_till,
        "times": times,
        "location": location,
        "irregularities": irregularities,
    }

    msg_plain = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_informed.txt", p,)
    msg_html = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_informed.html", p,)

    msg = EmailMultiAlternatives(subject, msg_plain, sender, to, bcc)
    msg.attach_alternative(msg_html, "text/html")
    msg.send()


def book_send_reminder(book):
    sender = "notmonkeys@acrolama.com"
    bcc = ["acrolama@acrolama.com"]
    subject = "Acrolama - Reminder - " + str(book.event.title)
    to = [book.user.email]

    irregularities = Irregularity.objects.filter(event__slug=book.event.slug)
    times = book.times.all()
    location = get_location_from_timeoption(times, book.event)

    try:
        abocount = get_count_abocounter_of_book(book.id)
    except ObjectDoesNotExist:
        abocount = False

    p = {
        "event": book.event,
        "user": book.user,
        "times": times,
        "location": location,
        "abocount": abocount,
        "irregularities": irregularities,
    }

    msg_plain = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_reminder.txt", p,)
    msg_html = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_reminder.html", p,)

    msg = EmailMultiAlternatives(subject, msg_plain, sender, to, bcc)
    msg.attach_alternative(msg_html, "text/html")
    msg.send()
