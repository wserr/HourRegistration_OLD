from BusinessEntities import TimeRecord

class TimeRecordValidation:
    def ValidateOnCreation(self,timeRecord):
        validationMessage = []
        if timeRecord.ProjectID is None:
            validationMessage.append('Please select Project')
        if timeRecord.RecordTypeID is None:
            validationMessage.append('Please select Record Type')
        if timeRecord.Description == '':
            validationMessage.append('Please fill in description')
        return validationMessage
        