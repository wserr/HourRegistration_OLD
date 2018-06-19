class TimeRecord:
    def __init__(self,ID,startHour,endHour,projectID,recordTypeID,description,statusID,minutes,oneNoteLink,km):
        self.ID = ID
        self.StartHour = startHour
        self.EndHour = endHour
        self.ProjectID = projectID
        self.RecordTypeID = recordTypeID 
        self.Description = description
        self.StatusID = statusID
        self.Minutes = minutes
        self.OneNoteLink = oneNoteLink
        self.Km = km


    def __str__(self):
        return self.Description