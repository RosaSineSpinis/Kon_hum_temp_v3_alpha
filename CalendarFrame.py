import tkinter as Tkinter

import ttkcalendar
import tkSimpleDialog

class CalendarDialog(tkSimpleDialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    """ take beg_date and and end_date essential to limit size of calendar options"""
    def __init__(self, parent, **kw):
        self.beg_date = kw.pop('beg_date', "01/01/2017")
        self.end_date = kw.pop('end_date', "01/01/2017")
        tkSimpleDialog.Dialog.__init__(self, parent, title=None) ##another constructor because inheritance

        # print("in init CF")
        # print(self.beg_date)
        # print(self.end_date)

    # print("we are in class CalendarDialog")
    def body(self, master):
        # print("we are in body")
        self.calendar = ttkcalendar.Calendar(master, year=2017, month=1, beg_date=self.beg_date, end_date=self.end_date)
        self.calendar.pack()

    def apply(self):
        # print("we are in apply")
        self.result = self.calendar.selection


class CalendarFrame(Tkinter.LabelFrame):
    # print("we are in CalendarFrame before init")

    def __init__(self, master, text = "", **kw):
        Tkinter.LabelFrame.__init__(self, master, text=text)

        self.beg_date = kw.pop('beg_date', "01/01/2017")  # ToDo in constructor send 'year' = 2019 or other minimal
        self.end_date = kw.pop('end_date', "01/01/2017")  # ToDo in constructor send 'month' = 2018 or other minimal

        # print("we are in CalendarFrame")


        self.selected_date = Tkinter.StringVar()

        self.my_entry = Tkinter.Entry(self, textvariable=self.selected_date)
        self.my_entry.pack(side=Tkinter.LEFT)
        self.my_button = Tkinter.Button(self, text="Choose a date", command=lambda: self.getdate(self.beg_date, self.end_date))
        self.my_button.pack(side=Tkinter.LEFT)

    def getdate(self, beg_date, end_date):
        # print("we are in getdate")
        # print(beg_date, end_date)
        cd = CalendarDialog(self, beg_date=beg_date, end_date=end_date) #create new calendar HERE WE CREATE NEW OBJECT, there is wait option inside
        # print("get date after creating object")
        result = cd.result #pickup result from calendar
        # print("get date after result")
        self.selected_date.set(result.strftime("%d/%m/%Y")) #result converted into date/month/year
        # print("get date after conversion - end -getEntryBelow")
        # print(self.getEntry())

    def getEntry(self):
        if self.selected_date:
            x = self.selected_date.get()
            return x
        else:
            return None


def main():
    root = Tkinter.Tk()
    root.wm_title("CalendarDialog Demo")
    CalendarFrame(root).pack()
    root.mainloop()

if __name__ == "__main__":
    main()