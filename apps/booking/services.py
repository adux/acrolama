from .models import Book, Assistance
from project.models import Event
from .utils import datelistgenerator


def createAssistance(instance):
    start = instance.event.event_startdate
    end = instance.event.event_enddate
    times = instance.times.all()
    obj = Assistance()
    date = []
    check = []
    obj.book_id = instance.id
    for to in times:
        num = to.regular_days.day
        li = datelistgenerator(start, end, int(num))
        date.extend(li)
        for time in li:
            check.append("False")
    obj.assistance_date = date
    obj.assistance_check = check
    obj.save()


def createAmountBookingAssistance(instance, status, amount):
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
    obj.comment = "Automatic created booking still on alpha"
    for x in range(1, amount):
        obj.id = None
        obj.pk = None
        if old_event.cycle + x > 12: #all the cycles should go from 1 to 12
            x = x - 12
        obj.event = Event.objects.filter(
            level=old_event.level,
            category=old_event.category,
            event_startdate__gt=old_event.event_enddate,
        ).get(cycle=old_event.cycle + x)
        try:
            obj.save()
            for x in times_pk:
                obj.times.add(x)
        except:
            print("Save error")
        else:
            print("Saved")
        instance.event = obj.event
        instance.id = obj.id
        instance.pk = obj.pk
        try:
            createAssistance(instance)
        except:
            print("Error creating Assistance")
