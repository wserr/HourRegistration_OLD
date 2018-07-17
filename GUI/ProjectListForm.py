from tkinter import *
from tkinter import ttk,messagebox
from BusinessLogic import BLProject,BLRecordType,BLTimeRecordView,BLTimeRecord,TimeRecordValidation,BLDayView, Cache, Globals
from BusinessEntities import TimeRecord,TimeRecordStatusEnum,DayView
import time
from GUI.ProjectEditForm import *


class ProjectListForm:
    def __init__(self,Cache,conn):
        self.Cache = Cache
        self.Connection = conn

        master = Tk()
        self.Master = master
        master.protocol('WM_DELETE_WINDOW', self.Quit)
        self.Master.title("Projects")

        self.AddButton = Button(master,text='Add',command=self.Add)
        self.AddButton.grid(row=0,column=0,sticky='NSEW')

        self.EditButton = Button(master,text='Edit',command =self.Edit)
        self.EditButton.grid(row=0,column=1,sticky='NSEW')

        self.DeleteButton = Button(master,text='Delete',command=self.Delete)
        self.DeleteButton.grid(row=0,column=2,sticky='NSEW')

        self.ActivationButton = Button(master,text='(De)Activate',command=self.ToggleActivation)
        self.ActivationButton.grid(row=0,column=3,sticky='NSEW')

        self.ShowOnlyActive = False
        self.ShowActiveOnlyButton = Button(master,text='Show Only Active',command=self.ToggleActiveProjects)
        self.ShowActiveOnlyButton.grid(row=0,column=4,sticky='NSEW')

        self.ProjectsListBox = Listbox(master,width=80)
        self.ProjectsListBox.grid(row=1,column=0,columnspan=10,sticky='NSEW')

        self.FillProjects()

        self.ProjectsListBox.bind('<Double-1>', lambda x: self.Edit())

    # def CloseWindow(self):
    #     self.Master.quit()

    def Quit(self):
        self.Master.quit()

    def Show(self):
        self.Master.mainloop()

    def ToggleActivation(self):
        sel = self.ProjectsListBox.curselection()[0]
        project = self.Cache.AllProjects[sel]
        if project.Active==0:
            project.Active=1
        else:
            project.Active=0
            project.Button = None
        bl = BLProject.BLProject(self.Connection)
        bl.Update(project)
        self.Cache.RefreshProjects()
        self.FillProjects()

    def ToggleActiveProjects(self):
        self.ShowOnlyActive = not self.ShowOnlyActive
        self.FillProjects()



    def FillProjects(self):
        self.ProjectsListBox.delete(0,END)
        if self.ShowOnlyActive:
            projects = self.Cache.ActiveProjects
        else:
            projects = self.Cache.AllProjects
        for item in projects:     
            self.ProjectsListBox.insert(END,item)
        for i in range(0,self.ProjectsListBox.size()):
            item = projects[i]
            active = item.Active
            if active == 0:
                self.ProjectsListBox.itemconfig(i,{'bg':'red'})

        
    def Add(self):
        pr = ProjectEditForm(self.Connection)
        pr.Show()
        self.Cache.RefreshProjects()
        self.FillProjects()
        pr.Master.destroy()


    def Edit(self):
        sel = self.ProjectsListBox.curselection()[0]
        project = self.GetProject(sel)
        pr = ProjectEditForm(self.Connection,project)
        pr.Show()
        self.Cache.RefreshProjects()
        self.FillProjects()
        pr.Master.destroy()

    def Delete(self):
        sel = self.ProjectsListBox.curselection()[0]
        project = self.GetProject(sel)
        bl = BLProject.BLProject(self.Connection)
        bl.DeleteByID(project.ID)
        self.Cache.RefreshProjects()
        self.FillProjects()

    def GetProject(self,ID):
        if self.ShowActiveOnlyButton:
            return self.Cache.ActiveProjects[ID]
        else:
            return self.Cache.AllProjects[ID]




        
