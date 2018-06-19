class TimeRecordView:
    def __init__(self,ID,startHour,endHour,description,project,recordType,status,date,oneNoteLink,km):
        self.ID = ID
        self.StartHour = startHour
        self.EndHour = endHour
        self.Project = project
        self.RecordType = recordType
        self.Description = description
        self.Status = status
        self.Date = date
        self.OneNoteLink = oneNoteLink
        self.Km = km


    def __str__(self):
        return str(self.StartHour) + '     ' + str(self.EndHour) + '       ' + self.Project + '    ' + self.RecordType + '    ' + self.Description + '    ' + self.Status