"""import matplotlib.pyplot as plt"""

#import csv
import matplotlib.pyplot as plt
#import numpy as np
import pandas
import matplotlib
#import math
import matplotlib.dates as mdates
#from matplotlib.ticker import FuncFormatter, MaxNLocator
#import codecs
from Tools.scripts.objgraph import ignore
from pandas.plotting import register_matplotlib_converters
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import glob
import os
import ttkcalendar
import CalendarFrame
from datetime import datetime
import Plotter
import PandasDataMerge
import OpenDirectoryPath

'''
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')
'''


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # self.top = top
        self.parent.title("Temperatura i Wilgotność")
        #top.geometry('600x800')
        #canvas = tk.Canvas(top, height = HEIGHT, width = WIDTH)
        #canvas.pack()
        self.cb_list_name = []
        self.cb_list_name_button = []
        self.cb_list_var = []
        self.df = pandas.DataFrame()
        self.df_temp = pandas.DataFrame()
        self.df_hum = pandas.DataFrame()
        self.beg_date_temp = "a"
        self.end_date_temp = "b"
        self.beg_date_hum = "c"
        self.end_date_hum = "d"
        self.guiFunction()

    def openFile(self):
        #openFileClass().openFile() used to generate one file
        self.df = openFileClass().openFile(self.cb_list_name_button, self.df)
        if not self.df.empty:
            for ch_button in self.cb_list_name_button:
                ch_button.config(state=tk.NORMAL)

    def openDirectory(self):

        #OpenDirectoryPathClass() open directory class and walk through direcotry
        path = OpenDirectoryPath.OpenDirectoryPathClass().openFile(self.cb_list_name_button, self.df)
        print(path)
        hum_path_list = []
        hum_filename_list = []
        temp_path_list = []
        temp_filename_list = []

        ''' Get directories and filenames, creates lists'''
        temp_filename_list, temp_path_list = OpenDirectoryPath.OpenDirectoryPathClass().walkDirectoryTopDown(path, ".csv", temp_filename_list, "TEMP", temp_path_list)
        hum_filename_list, hum_path_list = OpenDirectoryPath.OpenDirectoryPathClass().walkDirectoryTopDown(path, ".csv", hum_filename_list, "RH", hum_path_list)

        ''' Open files and merge csv. files together'''
        self.df_temp = PandasDataMerge.PandasDataFrameListToOneData().listToOneDataFrameConcat(self.df_temp, temp_filename_list, temp_path_list)
        self.df_hum = PandasDataMerge.PandasDataFrameListToOneData().listToOneDataFrameConcat(self.df_hum, hum_filename_list, hum_path_list)

        self.df_temp.to_csv("whole_temp.csv")
        self.df_hum.to_csv("whole_hum.csv")

        '''Get beginng and ending date'''
        self.beg_date_temp = PandasDataMerge.PandasDataFrameListToOneData().obtainBeginningDate(self.df_temp).date().strftime('%d/%m/%Y')
        self.end_date_temp = PandasDataMerge.PandasDataFrameListToOneData().obtainEndingDate(self.df_temp).date().strftime('%d/%m/%Y')
        self.beg_date_hum = PandasDataMerge.PandasDataFrameListToOneData().obtainBeginningDate(self.df_hum).date().strftime('%d/%m/%Y')
        self.end_date_hum = PandasDataMerge.PandasDataFrameListToOneData().obtainEndingDate(self.df_hum).date().strftime('%d/%m/%Y')

        print(type(self.beg_date_temp))
        print(type(self.end_date_temp))
        print(self.beg_date_temp)
        print(self.end_date_temp)
        print(self.beg_date_hum)
        print(self.end_date_hum)

        #'{:%d/%m/%Y}'.datetime.format(
        # s.dt.strftime('%Y/%m/%d')
        '''Compare data between temp and hum - choose earliest and latest'''
        #ToDo function here


        # print(self.beg_date_temp)
        # print(self.end_date_temp)


        if not (self.df_hum.empty and self.df_temp.empty):
            for ch_button in self.cb_list_name_button:
                ch_button.config(state=tk.NORMAL)

        # self.parent.calendar_frame_begin.config(self, beg_date=self.beg_date_temp, end_date=self.end_date_temp)
        # self.parent.calendar_frame_end = CalendarFrame.CalendarFrame(self, "Data koncowa", beg_date=self.beg_date_temp, end_date=self.end_date_temp)

        self.parent.calendar_frame_begin.beg_date = self.beg_date_temp
        self.parent.calendar_frame_begin.end_date = self.end_date_temp
        self.parent.calendar_frame_end.beg_date = self.beg_date_temp
        self.parent.calendar_frame_end.end_date = self.end_date_temp

    # def getdate(self):
    #     pass




    def guiFunction(self):
        self.parent.open_directory_button = tk.Button(self.parent, command=self.openDirectory, height=2, width=12, text="Otwórz Folder",
                                          activeforeground="light sky blue", activebackground="steelblue",
                                          bg="light sky blue")

        self.parent.open_file_button = tk.Button(self.parent, command=self.openFile, height=2, width=12, text="Otwórz Plik",
                                     activeforeground="light sky blue", activebackground="steelblue",
                                     bg="light sky blue")

        print("check date in gui")
        print(self.beg_date_temp)
        # self.parent.selected_date = tk.StringVar()

        self.parent.calendar_frame_begin = CalendarFrame.CalendarFrame(self.parent, "Data poczatakowa", beg_date=self.beg_date_temp, end_date=self.end_date_temp)
        self.parent.calendar_frame_end = CalendarFrame.CalendarFrame(self.parent, "Data koncowa", beg_date=self.beg_date_temp, end_date=self.end_date_temp)

        # self.selected_date = CalendarFrame.CalendarFrame.getEntry()
        # print(self.selected_date)



        self.cb_list_name = [
            'Strefa1',
            'Strefa2',
            'Strefa3',
            'Strefa4',
            'Strefa5',
            'Strefa6',
            'Strefa7',
            'Strefa8',
            'Strefa9',
            'Strefa10'
        ]
        self.cb_list_var = []
        self.cb_list_name_button = []


        for idx, value_label_name in enumerate(self.cb_list_name):
            self.cb_list_var.append(tk.StringVar())
            self.cb_list_var[idx].set(False)
            x = tk.Checkbutton(self.parent, text = value_label_name, var = self.cb_list_var[idx],  onvalue = value_label_name, offvalue=False, height=2, width=5, state=tk.DISABLED)
            self.cb_list_name_button.append(x)




        self.parent.rad_selected = tk.IntVar()
        self.parent.rad_temp = tk.Radiobutton(self.parent, value=0, text='Temperatura', variable=self.parent.rad_selected)
        self.parent.rad_hum = tk.Radiobutton(self.parent, value=1, text='Wilgotnosc', variable=self.parent.rad_selected)

        self.parent.plotButton = tk.Button(self.parent,
                                    command=lambda: self.clicked("one_graph"),
                                    height=2,
                                    width=12,
                                    text="Wykres",
                                    activeforeground="light sky blue",
                                    activebackground="steelblue",
                                    bg="light sky blue")
        self.parent.plotButton2 = tk.Button(self.parent,
                                     command=lambda: self.clicked("many_graphs"),
                                     height=2,
                                     width=12,
                                     text="Wykres all in one",
                                     activeforeground="light sky blue",
                                     activebackground="steelblue",
                                     bg="light sky blue")


        #grid data
        self.parent.grid_columnconfigure(1, minsize=30)
        self.parent.grid_columnconfigure(2, minsize=30)
        self.parent.grid_columnconfigure(3, minsize=30)

        self.parent.open_directory_button .grid(column=1, row=0, columnspan=1, sticky=tk.N + tk.E + tk.W + tk.S)
        self.parent.open_file_button.grid(column=0, row=0, columnspan=1, sticky=tk.N+tk.E+tk.W+tk.S)
        self.parent.calendar_frame_begin.grid(column=0, row=1, columnspan=3, sticky=tk.N + tk.E + tk.W + tk.S)
        self.parent.calendar_frame_end.grid(column=0, row=2, columnspan=3, sticky=tk.N + tk.E + tk.W + tk.S)

        column_int = 0;
        row_int = 3;
        end_row_int =6;
        for button in self.cb_list_name_button:
            button.grid(column = column_int, row = row_int, padx=0, pady=0, ipadx=0, ipady=0)
            row_int = row_int + 1
            if(row_int == (end_row_int+1)): #one more than is int number
                column_int = column_int + 1
                row_int = 3
        self.parent.rad_temp.grid(column=0, row=7)
        self.parent.rad_hum.grid(column=1, row=7)
        self.parent.plotButton.grid(column=0, row=9)
        self.parent.plotButton2.grid(column=1, row=9)

        return None


    def cb_checked(self):
        # remove text from label
        checked_list = []
        checked_list.clear()
        # print("We are in the function cb_checked")
        # for x in self.cb_list_var:
        #     print(x.get())
        # print('\n')
        for x in self.cb_list_var:
            if str(x.get()) != str(0):  ## IntVar not zero==checked
                checked_list.append(x)
        # print(checked_list)
        # print("leaving cb_checked_function")
        return checked_list


    def clicked(self, version):

        def selectDataRange(df):
            #ToDo doulbe check this function with wider range of dates
            '''beginning_date and ending date are DataFrame() in pandas, for loop search beg and ending index'''
            beginning_date = self.parent.calendar_frame_begin.selected_date.get()#begging determined by users choice in Entry
            ending_date = self.parent.calendar_frame_end.selected_date.get()#end determined by users choice in Entry
            '''find index of row where to cut at the beg and end'''
            print('Checking for in clicked')
            idx_beg = 0
            idx_end = 0
            for idx, x in enumerate(df.loc[:,'Date']):
                if x == pandas.to_datetime(beginning_date, format='%d/%m/%Y'):
                    # print("x= " + str(x) + " beg_date= " + str(pandas.to_datetime(beginning_date, format='%d/%m/%Y')))
                    idx_beg = idx
                    # print(idx)
                    break
            for idx, x in enumerate(df.loc[:, 'Date']):
                if x == pandas.to_datetime(ending_date, format='%d/%m/%Y'):
                    idx_end = idx
                    # print(x.date())
            print(idx_end)

            dfRange = (idx_beg, idx_end)
            print(dfRange)
            return dfRange

        def selectData(df):
            '''function return cut version of data frame, cut alongside the row'''
            dfRange = selectDataRange(df)

            df = df.iloc[dfRange[0]:dfRange[1], :]
            print(df)
            return(df)
            pass


        print("Entry below ")
        print(self.parent.calendar_frame_begin.getEntry())
        print(self.parent.calendar_frame_end.getEntry())
        cb_checked_list = self.cb_checked()
        cb_checked_list_string = []
        for x in cb_checked_list: #here I think we create string list of boxes which are checked
            cb_checked_list_string.append(str(x.get()))

        radio_button_value = self.parent.rad_selected.get()

        if (radio_button_value == 0):
            selectData(self.df_temp)
        elif (radio_button_value == 1):
            selectData(self.df_hum)

        if (radio_button_value == 0):
            graph_title_name = "Temperatura"
            if version == "one_graph":
                Plotter.Plotter().plot(cb_checked_list_string, self.df_temp, graph_title_name)
            elif version == "many_graphs":
                Plotter.Plotter().plotAllInOne(cb_checked_list_string, self.df_temp, graph_title_name)
        elif (radio_button_value == 1):
            graph_title_name = "Wilgotność"
            if version == "one_graph":
                Plotter.Plotter().plot(cb_checked_list_string, self.df_hum, graph_title_name)
            elif version == "many_graphs":
                Plotter.Plotter().plotAllInOne(cb_checked_list_string, self.df_temp, graph_title_name)

        # else:
        #     print("something wrong with radio_button")

        # print("for after function ")
        #uncomment if you want to check wich check button are checked
        # for x in self.cb_list_var:
        #     if str(x.get()) != str(0):  ## IntVar not zero==checked
        #         print(x.get())

        # for x in cb_checked_list:
        #     print(str(x.get()))


        # for x in cb_checked_list_string:
        #     print(x)


    """for this_row, text in enumerate(cb_list):
    cb_intvar.append(tk.IntVar())
    tk.Checkbutton(parent, text=text, variable=cb_intvar[-1],
                   command=cb_checked).grid(row=this_row,
                   column=0, sticky='w')"""


class openFileClass():
    # class made to cooperate with gui
    def __init__(self):
        pass

    def openFile(self, cb_list_name_butto, df):
        parent.filename = tk.filedialog.askopenfilename(initialdir="C:/Users/piotr/PycharmProjects/Kon_hum_temp",
                                                     title="Select *.CSV file",
                                                     filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        filename = parent.filename
        if not filename:
            return df
        # print(filename)
        try:
            df = pandas.read_csv(filename, encoding='utf-16', delimiter='\t')
            df.rename(columns={'Unnamed: 0': 'Time'}, inplace=True)  # column without name, rename then
            df.rename(columns={'Unnamed: 1': 'Date'}, inplace=True)  # column without name, rename then
            df['Date_time'] = pandas.to_datetime(
                df.iloc[:, 0] + ' ' + df.iloc[:, 1])  # merge data data + time and create new column
            df.Date_time = pandas.to_datetime(df.Date_time, format='%Y-%m-%d %H:%M:%S')
            df.to_csv('rewrittenFile.csv')  # we save file to csv just in case
            pandas.plotting.register_matplotlib_converters()  # conversion to matlibplot file
            # print(df)
            return df
        except pandas.errors.EmptyDataError:
            tk.messagebox.showerror("Error", "Empty File")
            return df
        except:
            tk.messagebox.showerror("Error", "Could not load the file")
            return df



    """
    temp_file = open('TEMP-20180620.csv')
    temp_file_reader = csv.reader(temp_file)
    temp_file_data = list(temp_file_reader)    """


if __name__ == "__main__":

    top = tk.Tk()
    plotter = MainApplication(top)
    top.mainloop()
