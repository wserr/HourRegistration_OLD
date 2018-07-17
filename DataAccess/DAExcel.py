import xlsxwriter

class DAExcel:
    def __init__(self,conn):
        self.Cursor = conn.Connection.cursor()
    
    def ExportToExcel(self,timeRecordViews,path):
        path = path.replace("-","") + ".xlsx"
        book = xlsxwriter.Workbook(path)
        sheet1 = book.add_worksheet("Sheet 1")
        rowIndex = 0
        sheet1.write(rowIndex,0,"ID")
        sheet1.write(rowIndex,1,"Date")
        sheet1.write(rowIndex,2,"StartTime")
        sheet1.write(rowIndex,3,"EndTime")
        sheet1.write(rowIndex,4,"Description")
        sheet1.write(rowIndex,5,"Project")
        sheet1.write(rowIndex,6,"RecordType")
        rowIndex = rowIndex+1
   
        for record in timeRecordViews:
            sheet1.write(rowIndex,0,record.ID)
            sheet1.write(rowIndex,1,record.Date)
            sheet1.write(rowIndex,2,record.StartHour)
            sheet1.write(rowIndex,3,record.EndHour)
            sheet1.write(rowIndex,4,record.Description)
            sheet1.write(rowIndex,5,record.Project)
            sheet1.write(rowIndex,6,record.RecordType)
            rowIndex = rowIndex+1
    
        book.close()

        
