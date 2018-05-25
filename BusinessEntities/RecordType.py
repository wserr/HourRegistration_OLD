class RecordType:
    def __init__(self,Id,description,externeId):
        self.ID = Id
        self.Description = description
        self.ExterneId = externeId
    def __str__(self):
        return self.Description