import datetime


def get_weekday_dates_for_period(startdate, enddate, weekday):
    """
    @param startdate date obj
    @param enddate date obj
    @param weekday int 0 Monday till 6 Sunday
    @return a list of dates
    """
    dates = []
    delta = enddate - startdate + datetime.timedelta(days=1)

    for x in range(delta.days):
        checkdate = startdate + datetime.timedelta(days=x)
        if checkdate.weekday() == weekday:
            dates.append(checkdate)

    return dates
