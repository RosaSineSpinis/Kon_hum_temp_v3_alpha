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


class MainApplication():
    def __init__(self, top, *args, **kwargs):
        #self.tk.Frame.__init__(self, top, *args, **kwargs)

        self.top = top
        self.top.title("Temperatura i Wilgotność")
        #top.geometry('600x800')
        #canvas = tk.Canvas(top, height = HEIGHT, width = WIDTH)
        #canvas.pack()
        self.cb_list_name = []
        self.cb_list_name_button = []
        self.cb_list_var = []
        self.guiFunction()
        self.df = pandas.DataFrame()
        self.df_temp = pandas.DataFrame()
        self.df_hum = pandas.DataFrame()

    def openFile(self):
        #openFileClass().openFile() used to generate one file
        self.df = openFileClass().openFile(self.cb_list_name_button, self.df)
        if not self.df.empty:
            for ch_button in self.cb_list_name_button:
                ch_button.config(state=tk.NORMAL)

    def openDirectory(self):

        #OpenDirectoryPathClass() open directory class and walk through direcotry
        path = OpenDirectoryPathClass().openFile(self.cb_list_name_button, self.df)
        print(path)
        hum_path_list = []
        hum_filename_list = []
        temp_path_list = []
        temp_filename_list = []

        temp_filename_list, temp_path_list = OpenDirectoryPathClass().walkDirectoryTopDown(path, ".csv", temp_filename_list, "TEMP", temp_path_list)
        hum_filename_list, hum_path_list = OpenDirectoryPathClass().walkDirectoryTopDown(path, ".csv", hum_filename_list, "RH", hum_path_list)

        self.df_temp = PandasDataFrameListToOneData().listToOneDataFrameConcat(self.df_temp, temp_filename_list, temp_path_list)
        self.df_hum = PandasDataFrameListToOneData().listToOneDataFrameConcat(self.df_hum, hum_filename_list, hum_path_list)



        if not (self.df_hum.empty and self.df_temp.empty):
            for ch_button in self.cb_list_name_button:
                ch_button.config(state=tk.NORMAL)


    # def getdate(self):
    #     pass

    def guiFunction(self):
        open_directory_button = tk.Button(self.top, command=self.openDirectory, height=2, width=12, text="Otwórz Folder",
                                     activeforeground="light sky blue", activebackground="steelblue",
                                     bg="light sky blue")

        open_file_button = tk.Button(self.top, command=self.openFile, height=2, width=12, text="Otwórz Plik",
                                     activeforeground="light sky blue", activebackground="steelblue",
                                     bg="light sky blue")


        # self.selected_date = tk.StringVar()
        # entry = tk.Entry(self.top, textvariable=self.selected_date)
        # entry_button = tk.Button(self.top, text="Choose a date", command=self.getdate)

        self.top.grid_columnconfigure(1, minsize=30)
        self.top.grid_columnconfigure(2, minsize=30)
        self.top.grid_columnconfigure(3, minsize=30)


        self.checkVar1 = tk.StringVar()
        self.checkVar1.set(False)  # set check state
        self.check_Strefa1 = tk.Checkbutton(self.top, text='Strefa1', var=self.checkVar1,  onvalue="Strefa1", offvalue=False, height=2, width=5, state=tk.DISABLED)

        self.checkVar2 = tk.StringVar()
        self.checkVar2.set(False)  # set check state
        self.check_Strefa2 = tk.Checkbutton(self.top, text='Strefa2', var=self.checkVar2, onvalue="Strefa2", offvalue=False, height=2, width=5, state=tk.DISABLED)

        self.checkVar3 = tk.StringVar()
        self.checkVar3.set(False)  # set check state
        self.check_Strefa3 = tk.Checkbutton(self.top, text='Strefa3', var=self.checkVar3, onvalue="Strefa3", offvalue=False, height=2, width=5, state=tk.DISABLED)

        self.checkVar4 = tk.StringVar()
        self.checkVar4.set(False)  # set check state
        self.check_Strefa4 = tk.Checkbutton(self.top, text='Strefa4', var=self.checkVar4, onvalue="Strefa4", offvalue=False, height=2, width=5, state=tk.DISABLED)

        self.checkVar5 = tk.StringVar()
        self.checkVar5.set(False)  # set check state
        self.check_Strefa5 = tk.Checkbutton(self.top, text='Strefa5', var=self.checkVar5, onvalue="Strefa5", offvalue=False, height=2, width=5, state=tk.DISABLED)

        self.checkVar6 = tk.StringVar()
        self.checkVar6.set(False)  # set check state
        self.check_Strefa6 = tk.Checkbutton(self.top, text='Strefa6', var=self.checkVar6, onvalue="Strefa6", offvalue=False, height=2, width=5, state=tk.DISABLED)

        self.checkVar7 = tk.StringVar()
        self.checkVar7.set(False)  # set check state
        self.check_Strefa7 = tk.Checkbutton(self.top, text='Strefa7', var=self.checkVar7, onvalue="Strefa7", offvalue=False, height=2, width=5, state=tk.DISABLED)

        self.checkVar8 = tk.StringVar()
        self.checkVar8.set(False)  # set check state
        self.check_Strefa8 = tk.Checkbutton(self.top, text='Strefa8', var=self.checkVar8, onvalue="Strefa8", offvalue=False, height=2, width=5, state=tk.DISABLED)

        self.checkVar9 = tk.StringVar()
        self.checkVar9.set(False)  # set check state
        self.check_Strefa9 = tk.Checkbutton(self.top, text='Strefa9', var=self.checkVar9, onvalue="Strefa9", offvalue=False, height=2, width=5, state=tk.DISABLED)

        self.checkVar10 = tk.StringVar()
        self.checkVar10.set(False)  # set check state
        self.check_Strefa10 = tk.Checkbutton(self.top, text='Strefa10', var=self.checkVar10, onvalue="Strefa10", offvalue=False, height=2, width=5, state=tk.DISABLED)

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

        self.cb_list_name_button = [
        self.check_Strefa1,
        self.check_Strefa2,
        self.check_Strefa3,
        self.check_Strefa4,
        self.check_Strefa5,
        self.check_Strefa6,
        self.check_Strefa7,
        self.check_Strefa8,
        self.check_Strefa9,
        self.check_Strefa10
        ]

        self.cb_list_var = [
        self.checkVar1,
        self.checkVar2,
        self.checkVar3,
        self.checkVar4,
        self.checkVar5,
        self.checkVar6,
        self.checkVar7,
        self.checkVar8,
        self.checkVar9,
        self.checkVar10
        ]

        self.rad_selected = tk.IntVar()
        self.rad_temp = tk.Radiobutton(self.top, value=0, text='Temperatura', variable=self.rad_selected)
        self.rad_hum = tk.Radiobutton(self.top, value=1, text='Wilgotnosc', variable=self.rad_selected)

        self.plotButton = tk.Button(self.top,
                                    command=lambda: self.clicked("one_graph"),
                                    height=2,
                                    width=12,
                                    text="Wykres",
                                    activeforeground="light sky blue",
                                    activebackground="steelblue",
                                    bg="light sky blue")
        self.plotButton2 = tk.Button(self.top,
                                    command=lambda: self.clicked("many_graphs"),
                                    height=2,
                                    width=12,
                                    text="Wykres all in one",
                                    activeforeground="light sky blue",
                                    activebackground="steelblue",
                                    bg="light sky blue")


        #grid data
        open_directory_button .grid(column=1, row=0, columnspan=1, sticky=tk.N + tk.E + tk.W + tk.S)
        open_file_button.grid(column=0, row=0, columnspan=1, sticky=tk.N+tk.E+tk.W+tk.S)
        # entry.grid(column=0, row=1, columnspan=1, sticky=tk.N + tk.E + tk.W + tk.S)
        # entry_button.grid(column=1, row=1, columnspan=1, sticky=tk.N + tk.E + tk.W + tk.S)
        self.check_Strefa1.grid(column=0, row=2, padx=0, pady=0, ipadx=0, ipady=0)
        self.check_Strefa2.grid(column=0, row=3, pady=0, ipadx=0, ipady=0)
        self.check_Strefa3.grid(column=0, row=4, padx=0, pady=0)
        self.check_Strefa4.grid(column=0, row=5, padx=0, pady=0)
        self.check_Strefa5.grid(column=1, row=2, padx=0, pady=0)
        self.check_Strefa6.grid(column=1, row=3, padx=0, pady=0)
        self.check_Strefa7.grid(column=1, row=4, padx=0, pady=0)
        self.check_Strefa8.grid(column=1, row=5, padx=0, pady=0)
        self.check_Strefa9.grid(column=2, row=2, padx=0, pady=0)
        self.check_Strefa10.grid(column=2, row=3, padx=0, pady=0)
        self.rad_temp.grid(column=0, row=6)
        self.rad_hum.grid(column=1, row=6)
        self.plotButton.grid(column=0, row=8)
        self.plotButton2.grid(column=1, row=8)

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
        cb_checked_list = self.cb_checked()
        cb_checked_list_string = []
        for x in cb_checked_list: #here I think we create string list of boxes which are checked
            cb_checked_list_string.append(str(x.get()))

        radio_button_value = self.rad_selected.get()
        if (radio_button_value == 0):
            graph_title_name = "Temperatura"
            if version == "one_graph":
                Plotter().plot(cb_checked_list_string, self.df_temp, graph_title_name)
            elif version == "many_graphs":
                Plotter().plotAllInOne(cb_checked_list_string, self.df_temp, graph_title_name)
        elif (radio_button_value == 1):
            graph_title_name = "Wilgotność"
            if version == "one_graph":
                Plotter().plot(cb_checked_list_string, self.df_hum, graph_title_name)
            elif version == "many_graphs":
                Plotter().plotAllInOne(cb_checked_list_string, self.df_temp, graph_title_name)

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
    tk.Checkbutton(top, text=text, variable=cb_intvar[-1],
                   command=cb_checked).grid(row=this_row,
                   column=0, sticky='w')"""


class Plotter():
    def __init__(self):
        pass

    def autofmt_datetime_axis(self, ax, minor_ticks=False):
        """Should I seperate minor_ticks from minor_tick_labels?
        """
        # Get the xmin and xmax of the axis object
        xmin = mdates.num2date(ax.get_xlim()[0])
        xmax = mdates.num2date(ax.get_xlim()[1])

        # Convert to a datetime object
        dt = xmax - xmin
        print(dt)


        return None


    def plotAllInOne(self, cb_checked_list_string, df, graph_title_name):
        pandas.plotting.register_matplotlib_converters()  # conversion to matlibplot file


        '''
        ax = plt.gca()
        df.plot(kind='line',x='Unnamed: 0',y='Strefa1',ax=ax)
        plt.show()

        '''

        strefa_name = cb_checked_list_string
        number_of_strefa = len(strefa_name)
        # print(number_of_strefa)

        number_of_separate_plots = 1
        fig, ax = plt.subplots(nrows=number_of_separate_plots, ncols=1, squeeze=False, sharex='col',
                               sharey='row')  # squeeze = False, always returns 2x2 matrix
        # plt.suptitle("Temperature")
        n = 0
        # for n in range(len(strefa_name)):
        for row in ax:
            for col in row:
                # ax.plot(df.iloc[:, 0], df.Strefa2)
                ##ax.set_xticklabels= (df.iloc[:, 0])
                for x in range(number_of_strefa):
                    col.plot(df.Date_time, df[strefa_name[x]], label=strefa_name[x])
                ##plt.xticks(df.iloc[:, 0], rotation='vertical')

                plt.xlabel(df.columns[0] + " " + df.columns[1])  # name of x axis
                # plt.ylabel(strefa_name[n]) #name of y axis - with many plots give only one input

                col.set_ylabel(strefa_name[n])
                col.set_yticklabels = (strefa_name[n])

                self.autofmt_datetime_axis(col, False)

                col.minorticks_on()
                # this block works fine give some kind of dynamic legend
                xtick_locator = mdates.AutoDateLocator()
                xtick_formatter = mdates.ConciseDateFormatter(xtick_locator)
                col.xaxis.set_major_locator(xtick_locator)
                col.xaxis.set_major_formatter(xtick_formatter)


                for label in col.xaxis.get_minorticklabels():
                    label.set_color('black')
                    label.set_rotation(45)
                    label.set_fontsize(8)
                    label.set_ha('right')

                for label in col.xaxis.get_ticklabels():
                    # label is a Text instance
                    label.set_color('black')
                    label.set_rotation(45)
                    label.set_fontsize(8)
                    label.set_ha('right')
                n += 1

        fig.subplots_adjust(bottom=0.2)
        # fig.tight_layout()
        fig.suptitle(graph_title_name)
        plt.legend()
        plt.show()
        return


    def plot(self, cb_checked_list_string, df, graph_title_name):
        pandas.plotting.register_matplotlib_converters()  # conversion to matlibplot file

        ####    df = pandas.read_csv('TEMP-20180620.csv', encoding='utf-16', delimiter='\t')
        # df = df[df['EPS'].notnull()]
        # df = df[pandas.notnull(df['EPS'])]
        ####print(df)
        ####    df.to_csv('rewrittenFile.csv')
        #global df

        '''
        ax = plt.gca()
        df.plot(kind='line',x='Unnamed: 0',y='Strefa1',ax=ax)
        plt.show()

        '''
        ####    df.rename(columns={'Unnamed: 0': 'Time'}, inplace=True)
        ####    df.rename(columns={'Unnamed: 1': 'Date'}, inplace=True)
        ####    df['Date_time'] = pandas.to_datetime(df.iloc[:, 0] + ' ' + df.iloc[:, 1]) #merge data data + time
        ####    df.Date_time = pandas.to_datetime(df.Date_time, format='%Y-%m-%d %H:%M:%S')
        # df = df.set_index('Date_time')

        # print(df.Date_time)
        ####print(df)

        # df.Date = pandas.to_datetime(df.Date, format='%d/%m/%Y')
        # df.Time = pandas.to_datetime(df.Time, format='%H:%M:%S')
        ####print(df.dtypes)
        # Date_time = pandas.combine(df.Date, df.Time)
        # print(df.dtypes)

        # date_time = pandas.to_datetime(df.iloc[:, 0] + ' ' + df.iloc[:, 1]) #merge data data + time
        # print(date_time.dtypes)
        # print(date_time)
        # print("next data_time " + str(date_time.dtypes))

        # df.plot(x='Date_time', y='Strefa2')
        # plt.show()

        # date_time = date_time.set_index('Date')
        # print(date_time)
        # uncomment single # to get previous set
        ####    pandas.plotting.register_matplotlib_converters()

        # strefa_name = []
        # strefa_name.append('Strefa1')
        # strefa_name.append('Strefa2')
        # strefa_name.append('Strefa3')
        # number_of_strefa = len(strefa_name)
        strefa_name = cb_checked_list_string
        # print(strefa_name)
        number_of_strefa = len(strefa_name)
        # print(number_of_strefa)

        # fig, ax = plt.subplots(number_of_strefa, 1, sharex='col', sharey='row', nrows=number_of_strefa, ncols=0)
        fig, ax = plt.subplots(nrows=number_of_strefa, ncols=1, squeeze=False, sharex='col', sharey='row') #squeeze = False, always returns 2x2 matrix
        # plt.suptitle("Temperature")
        n = 0
        # for n in range(len(strefa_name)):
        for row in ax:
            for col in row:
                # ax.plot(df.iloc[:, 0], df.Strefa2)
                ##ax.set_xticklabels= (df.iloc[:, 0])
                col.plot(df.Date_time, df[strefa_name[n]])
                ##plt.xticks(df.iloc[:, 0], rotation='vertical')

                plt.xlabel(df.columns[0] + " " + df.columns[1])  # name of x axis
                # plt.ylabel(strefa_name[n]) #name of y axis - with many plots give only one input

                col.set_ylabel(strefa_name[n])
                col.set_yticklabels = (strefa_name[n])

                # time = df.iloc[:, 0]
                # time = date_time
                # length = len(df.iloc[:, 0])
                # length = len(date_time)
                # xs = range(len(df.iloc[:, 0]))
                # xs = range(len(date_time))

                # def format_fn(tick_val, tick_pos):
                #     if int(tick_val) in xs:
                #         print(tick_val)
                #         #return df.iloc[int(tick_val), 0]
                #         return date_time[int(tick_val)]
                #     else:
                #         return ''
                # df.Date_time.to_pydatetime()
                daylist = []
                for x in df.Date_time:
                    if not x in daylist:
                        daylist.append(x.month)
                        # print(str(x.month) + ' ' + str(x.day))

                def format_fn(xx, pos=None):
                    if xx in daylist:
                        print(xx)
                        print(x.month)
                        # return mdates[int(xx)].strftime('%d:%m:%Y  %H:%M:%S')
                        return "if"
                    else:
                        return "else"


                self.autofmt_datetime_axis(col, False)

                # # ax.xaxis.set_major_locator(plt.MaxNLocator(24))
                ##ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
                # ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=24))
                # locator = ax.xaxis.set_major_locator(mdates.AutoDateLocator())
                col.minorticks_on()
                # ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M:%S'))
                # ax.xaxis.set_major_formatter(mdates.DateFormatter('%d:%m:%Y%H:%M:%S'))
                # col.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
                # col.xaxis.set_major_formatter(mdates.DateFormatter('%d:%m:%Y  %H:%M:%S'))

                # this block works fine give some kind of dynamic legend
                xtick_locator = mdates.AutoDateLocator()
                xtick_formatter = mdates.ConciseDateFormatter(xtick_locator)
                col.xaxis.set_major_locator(xtick_locator)
                col.xaxis.set_major_formatter(xtick_formatter)

                # col.xaxis.set_major_locator(matplotlib.ticker.FuncFormatter(format_fn))
                ##ax.set_xticklabels(alph[::int(len(alph)/nticks)])
                ##plt.xticks((df.iloc[:, 0]).to_pydatetime())
                ##ax.locator_params(axis='x', nbins=24)

                for label in col.xaxis.get_minorticklabels():
                    label.set_color('black')
                    label.set_rotation(45)
                    label.set_fontsize(8)
                    label.set_ha('right')

                for label in col.xaxis.get_ticklabels():
                    # label is a Text instance
                    label.set_color('black')
                    label.set_rotation(45)
                    label.set_fontsize(8)
                    label.set_ha('right')
                n += 1

        fig.subplots_adjust(bottom=0.2)
        # fig.tight_layout()
        fig.suptitle(graph_title_name)
        plt.show()
        return

class PandasDataFrameListToOneData():
    def __init__(self):
        pass

    def listToOneDataFrameConcat(self, df, filename_list, path_list):
        frames = []
        try:
            for idx, item in enumerate(path_list):
                df = pandas.read_csv(item, encoding='utf-16', delimiter='\t')
                df.rename(columns={'Unnamed: 0': 'Time'}, inplace=True)  # column without name, rename then
                df.rename(columns={'Unnamed: 1': 'Date'}, inplace=True)  # column without name, rename then
                df.drop(df.columns[[12]], axis=1, inplace=True) #remove columns with null, idk wjy it exists
                df['Date_time'] = pandas.to_datetime(
                    df.iloc[:, 0] + ' ' + df.iloc[:, 1])  # merge data data + time and create new column
                df.Date_time = pandas.to_datetime(df.Date_time, format='%Y-%m-%d %H:%M:%S')
                df.to_csv('rewritten_' + filename_list[idx])  # we save file to csv just in case
                frames.append(df)
                df = pandas.concat(frames, ignore_index=True)
            df.sort_values(by=['Date_time'], inplace=True, ascending=True)
            return df
        except pandas.errors.EmptyDataError:
            pass
        except ValueError:
            pass

class OpenDirectoryPathClass():
    # class made to cooperate with gui
    def __init__(self):
        pass

    def openFile(self, cb_list_name_butto, df):

        directory = tk.filedialog.askdirectory(initialdir="C:/Users/piotr/PycharmProjects/Kon_hum_temp")
        return directory

    def walkDirectoryTopDown(self, path, extension, filename_list, phrase_in_filename, path_list):
        for current_path, subfolders_name, filenames in os.walk(path):
            # pass
            # # print('The current folder is ' + current_path)
            # for subfolder in subfolders_name:
            #     pass
            #     # print('SUBFOLDER OF ' + current_path + ': ' + subfolder)
            for filename in filenames:
                if extension in filename:
                    if phrase_in_filename in filename:
                        print('FILE INSIDE with' + phrase_in_filename + current_path + ': ' + filename)
                        path_list.append(current_path + '/' + filename)
                        filename_list.append(filename)

        print("Check below")
        print(filename_list)
        return filename_list, path_list

class openFileClass():
    # class made to cooperate with gui
    def __init__(self):
        pass

    def openFile(self, cb_list_name_butto, df):
        top.filename = tk.filedialog.askopenfilename(initialdir="C:/Users/piotr/PycharmProjects/Kon_hum_temp",
                                                     title="Select *.CSV file",
                                                     filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        filename = top.filename
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
