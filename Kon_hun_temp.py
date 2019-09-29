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
import ftplib
from ftplib import FTP


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
        self.root_frame = tk.Frame.__init__(self, parent, *args, **kwargs)
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
        self.parent.rad_selected = tk.IntVar()
        self.parent.rad_selected.set(None)

        self.cb_list_name = []

        # self.cb_list_name = [
        #     'Strefa1',
        #     'Strefa2',
        #     'Strefa3',
        #     'Strefa4',
        #     'Strefa5',
        #     'Strefa6',
        #     'Strefa7',
        #     'Strefa8',
        #     'Strefa9',
        #     'Strefa10'
        # ]

        # self.ftp_download()
        self.guiFunction()

        self.parent.rad_temp.config(state=tk.DISABLED)
        self.parent.rad_hum.config(state=tk.DISABLED)
        for child in self.parent.calendar_frame_begin.winfo_children():
            child.configure(state='disable')
        # self.parent.calendar_frame_begin.my_entry.config(state=tk.DISABLED)
        # self.parent.calendar_frame_begin.my_button.config(state=tk.DISABLED)
        for child in self.parent.calendar_frame_end.winfo_children():
            child.configure(state='disable')



    def ftp_download(self):
        '''my code - download all files in the folder, but not subfolders'''
        # ftp = FTP("192.168.0.237", "nawilzanie", "789")
        ftp = ftplib.FTP()
        ftp.connect('192.168.0.237', 21)
        ftp.login('nawilzanie', '789')

        # ftp.login()
        ftp.retrlines("LIST")

        ftp.cwd("HMI/HMI-000/@HMI0029/History/CSV/")
        ftp.dir()
        # ftp.cwd("HMI-000")  # or ftp.cwd("folderOne/subFolder")
        # ftp.cwd("@HMI0029")
        # ftp.cwd("CSV")

        # ftp.cwd("folderOne")
        # ftp.cwd("subFolder")  # or ftp.cwd("folderOne/subFolder")

        listing = []
        ftp.retrlines("LIST", listing.append)
        for x in listing:
            # words = listing[0].split(None, 8)
            words = x.split(None, 8)
            print(words)
            filename = words[-1].lstrip()
            print("listing_below")
            print(listing)
            print("filename below")
            print(filename)

            # download the file
            local_filename = os.path.join(r"C:\Users\piotr\PycharmProjects\Kon_hum_temp_v3\ftp_data", filename)
            print(local_filename)
            print(type(local_filename))
            lf = open(local_filename, "wb")
            print(lf)
            print(type(lf))
            ftp.retrbinary("RETR " + filename, lf.write, 8 * 1024)
        lf.close()



        return

    def ftpSeverDownload(self, ftp_handle, path = "HMI", destination = r"C:\Users\piotr\PycharmProjects\Kon_hum_temp_v3\ftp_data", overwrite = True, guess_by_extension = True):
        ''' change to class and make new page, list change to __init__ '''

        def _is_ftp_dir(ftp_handle, name, guess_by_extension=True):
            """ simply determines if an item listed on the ftp server is a valid directory or not """

            # if the name has a "." in the fourth to last position, its probably a file extension
            # this is MUCH faster than trying to set every file to a working directory, and will work 99% of time.
            if guess_by_extension is True:
                if name[-4] == '.':
                    return False

            original_cwd = ftp_handle.pwd()  # remember the current working directory
            try:
                ftp_handle.cwd(name)  # try to set directory to new name
                ftp_handle.cwd(original_cwd)  # set it back to what it was
                return True
            except:
                return False

        def _make_parent_dir(fpath):
            """ ensures the parent directory of a filepath exists """
            dirname = os.path.dirname(fpath)
            while not os.path.exists(dirname):
                try:
                    os.mkdir(dirname)
                    print("created {0}".format(dirname))
                except:
                    _make_parent_dir(dirname)

        def _download_ftp_file(ftp_handle, name, dest, overwrite):
            """ downloads a single file from an ftp server """
            _make_parent_dir(dest)
            if not os.path.exists(dest) or overwrite is True:
                with open(dest, 'wb') as f:
                    ftp_handle.retrbinary("RETR {0}".format(name), f.write)
                print("downloaded: {0}".format(dest))
            else:
                print("already exists: {0}".format(dest))

        def _mirror_ftp_dir(ftp_handle, name, overwrite, guess_by_extension):
            """ replicates a directory on an ftp server recursively """
            for item in ftp_handle.nlst(name):
                if _is_ftp_dir(ftp_handle, item):
                    _mirror_ftp_dir(ftp_handle, item, overwrite, guess_by_extension)
                else:
                    _download_ftp_file(ftp_handle, item, item, overwrite)

        def download_ftp_tree(ftp_handle, path, destination, overwrite=False, guess_by_extension=True):
            """
            Downloads an entire directory tree from an ftp server to the local destination

            :param ftp_handle: an authenticated ftplib.FTP instance
            :param path: the folder on the ftp server to download
            :param destination: the local directory to store the copied folder
            :param overwrite: set to True to force re-download of all files, even if they appear to exist already
            :param guess_by_extension: It takes a while to explicitly check if every item is a directory or a file.
                if this flag is set to True, it will assume any file ending with a three character extension ".???" is
                a file and not a directory. Set to False if some folders may have a "." in their names -4th position.
            """
            os.chdir(destination)
            _mirror_ftp_dir(ftp_handle, path, overwrite, guess_by_extension)

        ftp = ftplib.FTP()
        ftp.connect('192.168.0.237', 21)
        ftp.login('nawilzanie', '789')
        download_ftp_tree(ftp_handle, path, destination, overwrite, guess_by_extension)

        return

    def openFile(self):
        #openFileClass().openFile() used to generate one file
        self.df = openFileClass().openFile(self.cb_list_name_button, self.df)
        if not self.df.empty:
            for ch_button in self.cb_list_name_button:
                ch_button.config(state=tk.NORMAL)


    def makeChButtonNormal(self):
        if not (self.df_hum.empty and self.df_temp.empty):
            print(self.cb_list_name_button)
            for ch_button in self.cb_list_name_button:
                ch_button.config(state=tk.NORMAL)

    def disableGui(self):
        self.removeCheckButtons()
        for child in self.parent.calendar_frame_begin.winfo_children():
            child.configure(state='disable')
        for child in self.parent.calendar_frame_end.winfo_children():
            child.configure(state='disable')
        self.parent.rad_temp.config(state=tk.DISABLED)
        self.parent.rad_hum.config(state=tk.DISABLED)
        self.parent.plotButton.config(state=tk.DISABLED)
        self.parent.plotButton2.config(state=tk.DISABLED)
        self.parent.plotButton3.config(state=tk.DISABLED)
        return

    def enableGui(self):
        return

    def openDirectory(self):
        ###ToDo loading screen, maybe disable everything, do some main class where all widget inherit disable status
        try:
            self.disableGui()
            #OpenDirectoryPathClass() open directory class and walk through direcotry
            path = OpenDirectoryPath.OpenDirectoryPathClass().openFile(self.cb_list_name_button, self.df)
            # print(path)
            hum_path_list = []
            hum_filename_list = []
            temp_path_list = []
            temp_filename_list = []

            ''' Get directories and filenames, creates lists'''
            #changes made ofr special init file
            temp_filename_list, temp_path_list = OpenDirectoryPath.OpenDirectoryPathClass().walkDirectoryTopDown(path, ".csv", temp_filename_list, "TEMP", temp_path_list)

            if not temp_filename_list: #check is empty
                temp_filename_list, temp_path_list = OpenDirectoryPath.OpenDirectoryPathClass().walkDirectoryTopDown(path,
                                                                                                                     ".csv",
                                                                                                                     temp_filename_list,
                                                                                                                     "Temp",
                                                                                                                     temp_path_list)

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
            #

            self.cb_list_name = []
            self.df = pandas.DataFrame()
            # self.update_check_buttons(self.df, self.beg_date_temp, self.end_date_temp)
            self.parent.rad_selected.set(None)
            # self.parent.rad_temp.deselect()
            # self.parent.rad_hum.deselect()
            self.parent.rad_temp.config(state=tk.NORMAL)
            self.parent.rad_hum.config(state=tk.NORMAL)


            print("file is loaded")

        except:
            print("something gone wrong")
            raise

        # def getdate(self):

    def removeCheckButtons(self):
        '''takes list of variables'''
        # print("removeCheckButtons")
        for ch_button in self.cb_list_name_button:
            ch_button.destroy()

        self.cb_list_var.clear()
        self.cb_list_name_button.clear()
        self.cb_list_name.clear()

        return


    def addCheckButtons(self):
        '''removes list of variables'''
        # print("addCheckButtons")
        for idx, value_label_name in enumerate(self.cb_list_name):
            # print("for in addCheckButtons is working")
            self.cb_list_var.append(tk.StringVar())
            self.cb_list_var[idx].set(False)
            x = tk.Checkbutton(self.parent, text=value_label_name, var=self.cb_list_var[idx], onvalue=value_label_name,
                               offvalue=False, height=2, width=5, state=tk.DISABLED)
            self.cb_list_name_button.append(x)
        # print(self.cb_list_name_button)

        return

    def createCheckBoxListName(self, df):
        check_box_list_name = []
        for column in df.columns[2:]:
            if column == "Date_time":
                continue
            elif not df.loc[:, column].isnull().all():
                check_box_list_name.append(column)
        # print(check_box_list_name)
        return check_box_list_name

    def update_check_buttons(self, df, beg, end):
        # print("update_check_buttons - working")
        self.removeCheckButtons()
        self.cb_list_name = self.createCheckBoxListName(df)
        # print(self.cb_list_name)
        self.addCheckButtons()
        self.guiFunction()
        self.parent.calendar_frame_begin.selected_date.set(beg)
        self.parent.calendar_frame_end.selected_date.set(end)

        return

    def guiFunction(self):
        self.parent.open_directory_button = tk.Button(self.parent, command=self.openDirectory, height=2, width=12, text="Otwórz Folder",
                                          activeforeground="light sky blue", activebackground="steelblue",
                                          bg="light sky blue")

        self.parent.open_file_button = tk.Button(self.parent, command=self.openFile, height=2, width=12, text="Otwórz Plik",
                                     activeforeground="light sky blue", activebackground="steelblue",
                                     bg="light sky blue")

        # print("check date in gui")
        # print(self.beg_date_temp)
        # self.parent.selected_date = tk.StringVar()

        self.parent.calendar_frame_begin = CalendarFrame.CalendarFrame(self.parent, "Data poczatakowa", beg_date=self.beg_date_temp, end_date=self.end_date_temp)
        self.parent.calendar_frame_end = CalendarFrame.CalendarFrame(self.parent, "Data koncowa", beg_date=self.beg_date_temp, end_date=self.end_date_temp)

        # self.selected_date = CalendarFrame.CalendarFrame.getEntry()
        # print(self.selected_date)

        self.cb_list_var = []
        self.cb_list_name_button = []


        for idx, value_label_name in enumerate(self.cb_list_name):
            self.cb_list_var.append(tk.StringVar())
            self.cb_list_var[idx].set(False)
            x = tk.Checkbutton(self.parent, text=value_label_name, var = self.cb_list_var[idx],  onvalue = value_label_name, offvalue=False, height=2, width=5, state=tk.DISABLED)
            self.cb_list_name_button.append(x)




        self.parent.rad_temp = tk.Radiobutton(self.parent, value=0, text='Temperatura', variable=self.parent.rad_selected, command=self.resetCheckBox)
        self.parent.rad_hum = tk.Radiobutton(self.parent, value=1, text='Wilgotnosc', variable=self.parent.rad_selected, command=self.resetCheckBox)

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
        self.parent.plotButton3 = tk.Button(self.parent,
                                     command=self.clicked_export_csv,
                                     height=2,
                                     width=12,
                                     text="Export to .csv",
                                     activeforeground="light sky blue",
                                     activebackground="steelblue",
                                     bg="light sky blue")


        #grid data
        self.parent.grid_columnconfigure(1, minsize=30)
        self.parent.grid_columnconfigure(2, minsize=30)
        self.parent.grid_columnconfigure(3, minsize=30)

        self.parent.open_directory_button.grid(column=1, row=0, columnspan=1, sticky=tk.N + tk.E + tk.W + tk.S)
        self.parent.open_file_button.grid(column=0, row=0, columnspan=1, sticky=tk.N+tk.E+tk.W+tk.S)
        self.parent.rad_temp.grid(column=0, row=1)
        self.parent.rad_hum.grid(column=1, row=1)

        self.parent.calendar_frame_begin.grid(column=0, row=2, columnspan=3, sticky=tk.N + tk.E + tk.W + tk.S)
        self.parent.calendar_frame_end.grid(column=0, row=3, columnspan=3, sticky=tk.N + tk.E + tk.W + tk.S)

        column_int = 0
        beg_row_int = 4
        row_int = beg_row_int
        end_row_int =7
        for button in self.cb_list_name_button:
            button.grid(column=column_int, row=row_int , padx=0, pady=0, ipadx=0, ipady=0)
            row_int = row_int + 1
            if(row_int == (end_row_int+1)): #one more than is int number
                column_int = column_int + 1
                row_int = beg_row_int
        self.parent.plotButton.grid(column=0, row=9)
        self.parent.plotButton2.grid(column=1, row=9)
        self.parent.plotButton3.grid(column=2, row=9)

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

    def resetCheckBox(self):
        radio_button_value = self.parent.rad_selected.get()
        print("radio_button_value", radio_button_value)

        if (radio_button_value == 0):
            self.parent.rad_hum.deselect()
            self.parent.rad_temp.select()
            self.update_check_buttons(self.df_temp, self.beg_date_temp, self.end_date_temp)
            self.makeChButtonNormal()

            self.parent.calendar_frame_begin.beg_date = self.beg_date_temp
            self.parent.calendar_frame_begin.end_date = self.end_date_temp
            self.parent.calendar_frame_end.beg_date = self.beg_date_temp
            self.parent.calendar_frame_end.end_date = self.end_date_temp
            # self.guiFunction()

        elif (radio_button_value == 1):
            self.parent.rad_temp.deselect()
            self.parent.rad_hum.select()
            self.update_check_buttons(self.df_hum, self.beg_date_hum, self.end_date_hum)
            self.makeChButtonNormal()

            self.parent.calendar_frame_begin.beg_date = self.beg_date_hum
            self.parent.calendar_frame_begin.end_date = self.end_date_hum
            self.parent.calendar_frame_end.beg_date = self.beg_date_hum
            self.parent.calendar_frame_end.end_date = self.end_date_hum
            # self.guiFunction()

        return

    def clicked_export_csv(self,):
        radio_button_value = self.parent.rad_selected.get()
        if (radio_button_value == 0):
            self.df_temp.to_csv("EXPORTED_TEMP.csv")
        elif (radio_button_value == 1):
            self.df_hum.to_csv("EXPORTED_HUM.csv")
        return


    def clicked(self, version):

        try:
            def selectDataRange(df):
                #ToDo doulbe check this function with wider range of dates
                '''beginning_date and ending date are DataFrame() in pandas, for loop search beg and ending index'''
                beginning_date = self.parent.calendar_frame_begin.selected_date.get()#begging determined by users choice in Entry
                ending_date = self.parent.calendar_frame_end.selected_date.get()#end determined by users choice in Entry

                print("beginning_date", beginning_date)
                print("ending_date", ending_date)

                '''find index of row where to cut at the beg and end'''
                idx_beg = 0
                idx_end = 0

                print(self.df_temp)
                print(self.df_hum)

                if 'Date' in df.columns:
                    for idx, x in enumerate(df.loc[:, 'Date']):
                        if x == pandas.to_datetime(beginning_date, format='%d/%m/%Y'):
                            idx_beg = idx
                            break
                    for idx, x in enumerate(df.loc[:, 'Date']):
                        if x == pandas.to_datetime(ending_date, format='%d/%m/%Y'):
                            idx_end = idx
                elif 'Data' in df.columns:
                    print("elif Minuta")
                    for idx, x in enumerate(df.loc[:,'Data']): #or df.iloc[:,1]
                        # print("idx_beg x", x)
                        if x.date() == pandas.to_datetime(beginning_date, format='%d/%m/%Y').date():
                            idx_beg = idx
                            break
                    for idx, x in enumerate(df.loc[:, 'Data']):
                        # print("idx_end x", x)
                        if x == pandas.to_datetime(ending_date, format='%d/%m/%Y'):
                            idx_end = idx

                df_range = (idx_beg, idx_end)
                print("df_range", df_range)

                return df_range

            def selectData(df):
                '''function return cut version of data frame, cut alongside the row'''
                df_range = selectDataRange(df)
                print("df_range in selectData", df_range)
                df = df.iloc[df_range[0]:df_range[1], :]
                #print("df", df)

                return df

            # print("Entry below ")
            # print(self.parent.calendar_frame_begin.getEntry())
            # print(self.parent.calendar_frame_end.getEntry())
            cb_checked_list = self.cb_checked()
            cb_checked_list_string = []
            for x in cb_checked_list: #here I think we create string list of boxes which are checked
                cb_checked_list_string.append(str(x.get()))

            radio_button_value = self.parent.rad_selected.get()
            print("radio satus" ,radio_button_value)

            if (radio_button_value == 0):
                self.df = selectData(self.df_temp)

            elif (radio_button_value == 1):
                self.df = selectData(self.df_hum)

            print(cb_checked_list_string)
            print(cb_checked_list_string == [])
            if not (cb_checked_list_string == []):
                if (radio_button_value == 0):
                    graph_title_name = "Temperatura"
                    if version == "one_graph":
                        Plotter.Plotter().plot(cb_checked_list_string, self.df, graph_title_name)
                    elif version == "many_graphs":
                        Plotter.Plotter().plotAllInOne(cb_checked_list_string, self.df, graph_title_name)
                elif (radio_button_value == 1):
                    graph_title_name = "Wilgotność"
                    if version == "one_graph":
                        Plotter.Plotter().plot(cb_checked_list_string, self.df, graph_title_name)
                    elif version == "many_graphs":
                        Plotter.Plotter().plotAllInOne(cb_checked_list_string, self.df, graph_title_name)
            else:
                print("dataFrame is empty")

            return

        except:
            print("Cannot print the graph - function clicked")


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
