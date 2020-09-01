import datetime
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from booking.models import Book, Attendance
from project.models import Event, TimeLocation
from accounting.models import Invoice

from .utils import datelistgenerator


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
            print("Time Location doesn't exist")

    return tl


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
    obj.pay_till = datetime.datetime.now().date() + datetime.timedelta(days=10)  # Give 10 Days to pay
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
                obj.attendance_date.append(book.event.event_startdate)
                obj.attendance_check.append("False")
            else:
                num = to.regular_day.day
                li = datelistgenerator(start, end, int(num))
                obj.attendance_date.extend(li)
                for time in li:
                    obj.attendance_check.append("False")
    else:
        obj.attendance_date.append(book.bookdateinfo.single_date)
        obj.attendance_check.append("False")

    obj.save()


def createNextBook(book, status):
    """
    Gets and Workshop Booking and creates the next based on cycle
    """
    book = get_book(book)
    print("in function book")
    print(type(book))

    obj = Book()
    obj.pk = None
    obj.id = None
    # Event resolved below
    obj.user = book.user
    obj.price = book.price
    # Times resolved below
    obj.note = "\nAutomatic created booking, please report if error."

    # Resolve Status
    try:
        obj.status = status
    except:
        obj.status = "PE"

    # Resolve Event
    old_event = book.event

    # Reset cycle num if needed
    try:
        new_event = Event.objects.filter(
            project=old_event.project,
            level=old_event.level,
            category=old_event.category,
            event_startdate__gt=old_event.event_enddate,
        ).get(cycle=old_event.cycle + 1)
    except (ObjectDoesNotExist) as e:
        new_event = Event.objects.filter(
            project=old_event.project,
            level=old_event.level,
            category=old_event.category,
            event_startdate__gt=old_event.event_enddate,
        ).get(cycle=1)
    except (MultipleObjectsReturned) as e:
        print("MultipleObjectes")
    except:
        print("Error with new_event. Doesn't have a next event?")

    else:
        print("New Event success")

    obj.event = new_event

    # Resolve Times
    times_pk = []
    for to in book.times.all():
        times_pk.append(to.pk)

    obj.save()
    try:
        for x in times_pk:
            obj.times.add(x)
    except:
        print("Times adding error")

    return obj


def createNextBookAttendance(book):
    """
    This function should be called only to create
    future Books and Attendance at the same time
    """
    book = get_book(book)

    # For Abos > 1
    for x in range(1, book.price.cycles):
        book = createNextBook(book, "PA")
        createAttendance(book)
