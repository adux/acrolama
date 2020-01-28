from django.core.exceptions import MultipleObjectsReturned, EmptyResultSet

from .models import Book, Attendance
from project.models import Event
from .utils import datelistgenerator


def updateSwitchCheckAttendance(id, position):
    attendance = Attendance.objects.get(pk=id)
    attendance.attendance_check[position] = not attendance.attendance_check[position]
    attendance.save()


def createAttendance(instance):
    start = instance.event.event_startdate
    end = instance.event.event_enddate
    times = instance.times.all()
    obj = Attendance()
    date = []
    check = []
    obj.book_id = instance.id
    print("Attendance Variables Loaded")
    for to in times:
        num = to.regular_days.day
        li = datelistgenerator(start, end, int(num))
        print(li)
        date.extend(li)
        print(date)
        for time in li:
            check.append("False")
            print(check)
    obj.attendance_date = date
    obj.attendance_check = check
    obj.save()
    print("Save Attendance")


def createAmountBookingAttendance(instance, status, amount):
    """
    Creates a Booking from a instance of the form in booking system
    """
    obj = Book()
    obj.user = instance.user
    obj.price = instance.price
    obj.status = status
    old_event = instance.event
    times = instance.times.all()
    times_pk = []
    for to in times:
        times_pk.append(to.pk)
    obj.comment = "Automatic created booking, please report if error"
    for x in range(1, amount):
        if old_event.cycle + x > 12: #all the cycles should go from 1 to 12
            x = x - 12
            print("12 Cycles over getting to 1")
        obj.id = None
        obj.pk = None
        try:
            obj.event = Event.objects.filter(
                level=old_event.level,
                category=old_event.category,
                event_startdate__gt=old_event.event_enddate,
            ).get(cycle=old_event.cycle + x)
        except (EmptyResultSet, MultipleObjectsReturned) as e:
            print("Either None or Multiple Objects Found")
        try:
            obj.save()
            for x in times_pk:
                obj.times.add(x)
        except:
            print("Save extra booking error")
        instance.event = obj.event
        instance.id = obj.id
        instance.pk = obj.pk
        try:
            createAttendance(instance)
        except:
            print("Error creating Attendance")
