class Project:
    def __init__(self,Id,description,externeId,button,active):
        self.ID = Id
        self.Description = description
        self.ExterneId = externeId
        self.Active = active
        self.Button = button
  
    def __str__(self):
        addString = ''
        if not str(self.Button) == 'None':
            addString = '       ' + str(self.Button)
        return self.Description + addString
