from project.models import TimeLocation, Event, PriceOption


def timelocation_get(tl):

    # If its str or int treat it as id
    if isinstance(tl, (str, int)):
        tl_pk = int(tl)
    else:
        return tl

    # if its a id get the book
    if tl_pk:
        return TimeLocation.objects.get(pk=tl_pk)


def event_get(event):
    # If its str or int treat it as id
    if isinstance(event, (str, int)):
        event_pk = int(event)
    else:
        return event

    # if its a id get the book
    if event_pk:
        return Event.objects.get(pk=event_pk)


def priceoption_get(po):
    # If its str or int treat it as id
    if isinstance(po, (str, int)):
        event_pk = int(po)
    else:
        return po

    # if its a id get the book
    if event_pk:
        return PriceOption.objects.get(pk=po)
