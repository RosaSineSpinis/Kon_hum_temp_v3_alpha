"""
Simple calendar using ttk Treeview together with calendar and datetime
classes.
"""
import calendar

try:
    import Tkinter
    import tkFont
except ImportError: # py3k
    import tkinter as Tkinter
    import tkinter.font as tkFont

from tkinter import ttk
from datetime import datetime

def get_calendar(locale, fwday):
    # instantiate proper calendar class
    # print("get_calendar function")
    if locale is None:
        # print("we are in if")
        # print(fwday)
        return calendar.TextCalendar(fwday)
    else:
        # print("we are in else")
        # print(fwday)
        # print(locale)
        return calendar.LocaleTextCalendar(fwday, locale) #locale name of days and moths I think Monday...

class Calendar(ttk.Frame):
    # XXX ToDo: cget and configure

    datetime = calendar.datetime.datetime
    timedelta = calendar.datetime.timedelta

    def __init__(self, master=None, **kw):
        """
        WIDGET-SPECIFIC OPTIONS
            locale, firstweekday, year, month, selectbackground,
            selectforeground
        """
        # print("kw is below")
        # print(kw)
        # remove custom options from kw before initializating ttk.Frame
        fwday = kw.pop('firstweekday', calendar.MONDAY)
        year = kw.pop('year', self.datetime.now().year)
        month = kw.pop('month', self.datetime.now().month)
        locale = kw.pop('locale', None) # no idea what it is
        sel_bg = kw.pop('selectbackground', '#ecffc4')
        sel_fg = kw.pop('selectforeground', '#05640e')
        self.beg_date = kw.pop('beg_date', "04/08/2018") #initial parameters - change for testing
        self.end_date = kw.pop('end_date', "08/01/2019") # initial parameters - change for testing

        self._beg_date = datetime.strptime(self.beg_date, '%d/%m/%Y').date()
        self._end_date = datetime.strptime(self.end_date, '%d/%m/%Y').date()


        self._date = self.datetime(self._beg_date.year, self._beg_date.month, 1)
        # print("First self._date below")
        # print(self._date)
        self._selection = None # no date selected # - date to the output

        ttk.Frame.__init__(self, master, **kw)
        # print("just before get_calendar")
        self._cal = get_calendar(locale, fwday)
        # print(self._cal.yeardayscalendar(2019))
        # print("")
        # print(self._cal.yeardatescalendar(2019))
        # print("")
        # print(self._cal.yeardays2calendar(2019))

        self.__setup_styles()       # creates custom styles
        self.__place_widgets()      # pack/grid used widgets
        self.__config_calendar()    # adjust calendar columns and setup tags
        # configure a canvas, and proper bindings, for selecting dates
        self.__setup_selection(sel_bg, sel_fg)

        # store items ids, used for insertion later
        self._items = [self._calendar.insert('', 'end', values='')
                            for _ in range(6)]
        # print("items")
        # print(self._items)

        # insert dates in the currently empty calendar
        self._build_calendar()
        # print("end of initializer")

    def __setitem__(self, item, value):
        if item in ('year', 'month'):
            raise AttributeError("attribute '%s' is not writeable" % item)
        elif item == 'selectbackground':
            self._canvas['background'] = value
        elif item == 'selectforeground':
            self._canvas.itemconfigure(self._canvas.text, item=value)
        else:
            ttk.Frame.__setitem__(self, item, value)

    def __getitem__(self, item):
        if item in ('year', 'month'):
            return getattr(self._date, item)
        elif item == 'selectbackground':
            return self._canvas['background']
        elif item == 'selectforeground':
            return self._canvas.itemcget(self._canvas.text, 'fill')
        else:
            r = ttk.tclobjs_to_py({item: ttk.Frame.__getitem__(self, item)})
            return r[item]

    def __setup_styles(self):
        # custom ttk styles
        style = ttk.Style(self.master)
        arrow_layout = lambda dir: (
            [('Button.focus', {'children': [('Button.%sarrow' % dir, None)]})]
        )
        style.layout('L.TButton', arrow_layout('left'))
        style.layout('R.TButton', arrow_layout('right'))

    def __place_widgets(self):
        # header frame and its widgets
        hframe = ttk.Frame(self)
        lbtn = ttk.Button(hframe, style='L.TButton', command=self._prev_month)
        rbtn = ttk.Button(hframe, style='R.TButton', command=self._next_month)
        self._header = ttk.Label(hframe, width=15, anchor='center')
        # the calendar
        self._calendar = ttk.Treeview(self, show='', selectmode='none', height=7)

        # pack the widgets
        hframe.pack(in_=self, side='top', pady=4, anchor='center')
        lbtn.grid(in_=hframe)
        self._header.grid(in_=hframe, column=1, row=0, padx=12)
        rbtn.grid(in_=hframe, column=2, row=0)
        self._calendar.pack(in_=self, expand=1, fill='both', side='bottom')

    def __config_calendar(self):
        cols = self._cal.formatweekheader(3).split()
        self._calendar['columns'] = cols
        self._calendar.tag_configure('header', background='grey90')
        self._calendar.insert('', 'end', values=cols, tag='header')
        # adjust its columns width
        font = tkFont.Font()
        maxwidth = max(font.measure(col) for col in cols)
        for col in cols:
            self._calendar.column(col, width=maxwidth, minwidth=maxwidth,
                anchor='e')

    def __setup_selection(self, sel_bg, sel_fg):
        self._font = tkFont.Font()
        self._canvas = canvas = Tkinter.Canvas(self._calendar,
            background=sel_bg, borderwidth=0, highlightthickness=0)
        canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')

        canvas.bind('<ButtonPress-1>', lambda evt: canvas.place_forget())
        self._calendar.bind('<Configure>', lambda evt: canvas.place_forget())
        self._calendar.bind('<ButtonPress-1>', self._pressed)

    def __minsize(self, evt):
        width, height = self._calendar.master.geometry().split('x')
        height = height[:height.index('+')]
        self._calendar.master.minsize(width, height)

    # def _build_calendar(self):
    #     year, month = self._date.year, self._date.month #here we replace it with the smallest year and month
    #     header = self._cal.formatmonthname(year, month, 0)
    #     self._header['text'] = header.title()
    #     cal = self._cal.monthdayscalendar(year, month)
    #     for indx, item in enumerate(self._items):
    #         week = cal[indx] if indx < len(cal) else []
    #         fmt_week = [('%02d' % day) if day else '' for day in week]
    #         self._calendar.item(item, values=fmt_week)


    def _build_calendar(self):
        ''' Added function which takes the earliest and latest day from the file and create calendar between them'''
        year, month = self._date.year, self._date.month #here we replace it with the smallest year and month
        # print(self._beg_date)
        # print(self._end_date)

        # update header of the widget text (Month, YEAR)
        header = self._cal.formatmonthname(year, month, 0)
        self._header['text'] = header.title()
        # update calendar shown dates
        cal = self._cal.monthdayscalendar(year, month)

        for indx, item in enumerate(self._items):
            week = cal[indx] if indx < len(cal) else []

            if year > self._beg_date.year and year < self._end_date.year:
                '''one solution'''
                fmt_week = [('%02d' % day) if day else '' for day in week]

            elif year > self._beg_date.year and year == self._end_date.year:
                if month == self._end_date.month:
                    fmt_week = [('%02d' % day) if (day and day <= self._end_date.day) else '' for day in week]
                else:
                    fmt_week = [('%02d' % day) if day else '' for day in week]

            elif year == self._beg_date.year and year < self._end_date.year:
                if month == self._beg_date.month:
                    fmt_week = [('%02d' % day) if (day and day >= self._beg_date.day) else '' for day in week]
                else:
                    fmt_week = [('%02d' % day) if day else '' for day in week]

            elif year == self._beg_date.year and year == self._end_date.year:
                if month > self._beg_date.month and month < self._end_date.month:
                    fmt_week = [('%02d' % day) if day else '' for day in week]
                elif month > self._beg_date.month and month == self._end_date.month:
                    fmt_week = [('%02d' % day) if (day and day <= self._end_date.day) else '' for day in week]
                elif month == self._beg_date.month and month < self._end_date.month:
                    fmt_week = [('%02d' % day) if (day and day >= self._beg_date.day) else '' for day in week]
                elif month == self._beg_date.month and month == self._end_date.month:
                    fmt_week = [('%02d' % day) if (day and day >= self._beg_date.day and day <= self._end_date.day) else '' for day in week]
            self._calendar.item(item, values=fmt_week)

    def _show_selection(self, text, bbox):
        """Configure canvas for a new selection."""
        x, y, width, height = bbox

        textw = self._font.measure(text)

        canvas = self._canvas
        canvas.configure(width=width, height=height)
        canvas.coords(canvas.text, width - textw, height / 2 - 1)
        canvas.itemconfigure(canvas.text, text=text)
        canvas.place(in_=self._calendar, x=x, y=y)

    # Callbacks

    def _pressed(self, evt):
        """Clicked somewhere in the calendar."""
        x, y, widget = evt.x, evt.y, evt.widget
        item = widget.identify_row(y)
        column = widget.identify_column(x)

        if not column or not item in self._items:
            # clicked in the weekdays row or just outside the columns
            return

        item_values = widget.item(item)['values']
        if not len(item_values): # row is empty for this month
            return

        text = item_values[int(column[1]) - 1]
        if not text: # date is empty
            return

        bbox = widget.bbox(item, column)
        if not bbox: # calendar not visible yet
            return

        # update and then show selection
        text = '%02d' % text
        self._selection = (text, item, column) #text is day I think
        self._show_selection(text, bbox)

    def _prev_month(self):
        """Updated calendar to show the previous month."""
        # print("")
        # print("")
        # print("_prev_month function ")
        self._canvas.place_forget() #here we clean canavas probably
        new_date = self._date - self.timedelta(days=1)
        if new_date.year > self._beg_date.year:
            self._date = new_date
        elif new_date.year == self._beg_date.year and new_date.month >= self._beg_date.month:
            self._date = new_date
        else:
            pass
        # self._date = self._date - self.timedelta(days=1) #here from 1.month - 1 day = 31.(month-1)
        self._date = self.datetime(self._date.year, self._date.month, 1) #here change 31.(month-1) to 1.(month-1)
        self._build_calendar() # reconstuct calendar


    def _next_month(self):
        """Update calendar to show the next month."""
        # print("")
        # print("")
        # print("_next_month function ")

        self._canvas.place_forget()
        year, month = self._date.year, self._date.month # get year and month of the previous canvas
        new_date = self._date + self.timedelta(days=calendar.monthrange(year, month)[1] + 1) # 1 month + 30 + 1 day = new month
        if new_date.year < self._end_date.year:
            self._date = new_date
        elif new_date.year == self._end_date.year and new_date.month <= self._end_date.month:
            self._date = new_date
        else:
            pass
        self._date = self.datetime(self._date.year, self._date.month, 1) #reset to be sure there is 1.(month+1)
        self._build_calendar() # reconstruct calendar

    # Properties

    @property
    def selection(self):
        """Return a datetime representing the current selected date."""
        if not self._selection:
            return None

        year, month = self._date.year, self._date.month
        return self.datetime(year, month, int(self._selection[0])) #take what is clicked + add month and year

def test():
    import sys
    root = Tkinter.Tk()
    root.title('Ttk Calendar')
    ttkcal = Calendar(firstweekday=calendar.SUNDAY)
    ttkcal.pack(expand=1, fill='both')

    if 'win' not in sys.platform:
        style = ttk.Style()
        style.theme_use('clam')

    root.mainloop()

if __name__ == '__main__':
    test()