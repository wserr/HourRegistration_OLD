import math

class DayView:
    def __init__(self,date,minutes):
        self.Date = date
        self.Minutes = minutes

    def __str__(self):
        hours = math.floor(self.Minutes/60)
        minutes = self.Minutes - hours*60

        hourString = "%02d" % (hours,)
        minutesString = "%02d" % (minutes,)
        timeString = hourString + ":" + minutesString
        return self.Date + '    ' + timeString