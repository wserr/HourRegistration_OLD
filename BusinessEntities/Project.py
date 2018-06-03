class Project:
    def __init__(self,Id,description,externeId,active=None):
        self.ID = Id
        self.Description = description
        self.ExterneId = externeId
        self.Active = active
  
    def __str__(self):
        return self.Description
