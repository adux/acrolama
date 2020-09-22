import datetime
from django.contrib import messages
from django.utils.translation import gettext as _

from booking.models import Book, Attendance, AboCounter, BOOKINGSTATUS
from project.models import Event, TimeLocation
from accounting.models import Invoice

import booking.utils


def get_book(book):
    # If its str or int treat it as id
    if isinstance(book, (str, int)):
        book_pk = int(book)
    else:
        return book

    # if its a id get the book
    if book_pk:
        try:
            book = Book.objects.get(pk=book_pk)
        except Book.DoesNotExist:
            # TODO: Raise Error to log or to Sentry somehow ?
            print("Booking doesn't exist")

    return book


def get_event(event):
    # If its str or int treat it as id
    if isinstance(event, (str, int)):
        event_pk = int(event)
    else:
        return event

    # if its a id get the book
    if event_pk:
        try:
            event = Event.objects.get(pk=event_pk)
        except Event.DoesNotExist:
            # TODO: Raise Error to log or to Sentry somehow ?
            print("Event doesn't exist")

    return event


def get_timelocation(tl):
    # If its str or int treat it as id
    if isinstance(tl, (str, int)):
        tl_pk = int(tl)
    else:
        return tl

    # if its a id get the book
    if tl_pk:
        try:
            tl = TimeLocation.objects.get(pk=tl_pk)
        except TimeLocation.DoesNotExist:
            # TODO: Raise Error to log or to Sentry somehow ?
            print("Time Location doesn't exist")

    return tl


def getLocationFromTimeOption(timeoptions, event):
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


def updateSwitchCheckAttendance(id, position):
    attendance = Attendance.objects.get(pk=id)
    attendance.attendance_check[position] = not attendance.attendance_check[position]
    attendance.save()


def updateBookStatus(book, status):
    book = get_book(book)
    if status in ("PA", "Participant"):
        book.status = "PA"
        book.save()
    elif status in ("CA", "Canceled"):
        book.status = "CA"
        book.save()


def createInvoiceFromBook(book):
    book = get_book(book)

    obj = Invoice()
    obj.balance = "CR"  # Credit
    obj.book = book
    # TODO create a smart referral code
    # Code created in Email Send ...
    obj.status = "PE"   # Pending
    obj.to_pay = int(book.price.price_chf)
    # Default 10 days to pay
    obj.pay_till = datetime.datetime.now().date() + datetime.timedelta(days=book.price.days_till_pay)
    obj.notes = "\n Automatic created Invoice"
    obj.save()


def createAttendance(book):
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
                li = booking.utils.datelistgenerator(start, end, int(num))
                obj.attendance_date.extend(li)
                for time in li:
                    obj.attendance_check.append("False")
    else:
        # If a Single Date is selected build the Attendance with it.
        obj.attendance_date.append(book.bookdateinfo.single_date)
        obj.attendance_check.append("False")

    obj.save()


def checkAboCounter(bookid):
    return AboCounter.objects.filter(data__last_book=str(bookid)).exists()


def reduceAboCounter(bookid):
    obj = AboCounter.objects.get(data__last_book=str(bookid))
    obj.data['count'] -= 1
    obj.save()


def createAboCounter(book):
    AboCounter.objects.create(data={'first_book': str(book.id), 'last_book': str(book.id), 'count': book.price.cycles})


def updateAboCounter(bookid, newbookid):
    obj = AboCounter.objects.get(data__last_book=str(bookid))
    obj.data['last_book'] = str(newbookid)
    obj.save()


def getAboCounterCount(bookid):
    return AboCounter.objects.get(data__last_book=str(bookid)).data['count']


def newInformedBook(request, instance, book):
    # If Abo Create Counter

    if book.price.cycles < 2:
        # Invoice
        try:
            createInvoiceFromBook(instance)
        except Exception as e:
            messages.add_message(
                request, messages.WARNING, _("Error creating Invoice: " + str(e)),
            )
        else:
            messages.add_message(request, messages.SUCCESS, _("Invoice Created"))

        # Send New Book Email
        if book.informed_at is None:
            try:
                booking.utils.email_sender(instance, "Informed")
            except Exception as e:
                messages.add_message(request, messages.ERROR, _("Error Email: " + str(e)))
            else:
                messages.add_message(request, messages.SUCCESS, _("Informed email sent."))
                instance.informed_at = datetime.datetime.now()
        else:
            messages.add_message(request, messages.INFO, _("Email sent: " + str(book.informed_at)))

    else:

        if not checkAboCounter(book.id):
            # Create the Counter for Abos
            createAboCounter(book)
            reduceAboCounter(book.id)

            # Invoice
            try:
                createInvoiceFromBook(instance)
            except Exception as e:
                messages.add_message(
                    request, messages.WARNING, _("Error creating Invoice: " + str(e)),
                )
            else:
                messages.add_message(request, messages.SUCCESS, _("Invoice Created"))

            # Send New Book Email
            if book.informed_at is None:
                try:
                    booking.utils.email_sender(instance, "Informed")
                except Exception as e:
                    messages.add_message(request, messages.ERROR, _("Error Email: " + str(e)))
                else:
                    messages.add_message(request, messages.SUCCESS, _("Informed email sent."))
                    instance.informed_at = datetime.datetime.now()
            else:
                messages.add_message(request, messages.INFO, _("Email sent: " + str(book.informed_at)))

        else:
            reduceAboCounter(book.id)

            # Send New Book Email
            if book.informed_at is None:
                try:
                    booking.utils.email_sender(instance, "Reminder")
                except Exception as e:
                    messages.add_message(request, messages.ERROR, _("Error Email: " + str(e)))
                else:
                    messages.add_message(request, messages.SUCCESS, _("Reminder email sent."))
                    instance.informed_at = datetime.datetime.now()
            else:
                messages.add_message(request, messages.INFO, _("Email sent: " + str(book.informed_at)))

    try:
        createAttendance(instance)
    except Exception as e:
        messages.add_message(
            request, messages.WARNING, _("Error creating Attendance: " + str(e)),
        )
    else:
        messages.add_message(request, messages.SUCCESS, _("Attendance created"))


def createNextBook(book, status):
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
    # Hope i understood this right:
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
