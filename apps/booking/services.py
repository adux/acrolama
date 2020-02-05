import datetime
from django.core.exceptions import MultipleObjectsReturned, EmptyResultSet

from .models import Book, Attendance
from project.models import Event
from accounting.models import Invoice
from .utils import datelistgenerator


def updateSwitchCheckAttendance(id, position):
    attendance = Attendance.objects.get(pk=id)
    attendance.attendance_check[position] = not attendance.attendance_check[
        position
    ]
    attendance.save()


def get_book(book):
    print(type(book))

    # If its str or int treat it as id
    if isinstance(book, (str, int)):
        print("its a string ?")
        book_pk = int(book)
    else:
        print("its a book")
        return book

    if book_pk:
        print("here")
        try:
            print("here")
            book = Book.objects.get(pk=book_pk)
        except:
            print("Booking doesn't exist")

    return book

def createInvoiceFromBook(book):
    book = get_book(book)

    obj = Invoice()
    obj.balance = "CR"
    obj.book = book
    #TODO create a smart referral code
    obj.status = "PE"
    obj.to_pay = int(book.price.price_chf)
    obj.pay_till = datetime.datetime.now().date() + datetime.timedelta(days = 10)
    obj.notes = "\n Automatic created Invoice"
    obj.save()


def createAttendance(book):
    """
    Creates an Attendance to a particular booking
    """
    # Get a book
    book = get_book(book)

    # Get time infos
    start = book.event.event_startdate
    end = book.event.event_enddate
    times = book.times.all()

    # Create Attendance
    obj = Attendance()
    obj.book_id = book.id
    obj.attendance_date = []
    obj.attendance_check = []
    # For each TimeOption we get the dates and for dates check as False
    for to in times:
        num = to.regular_days.day
        li = datelistgenerator(start, end, int(num))
        obj.attendance_date.extend(li)
        for time in li:
            obj.attendance_check.append("False")
    obj.save()
    print("Save Attendance")


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
    except (EmptyResultSet) as e:
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
