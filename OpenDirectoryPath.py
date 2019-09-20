import os
import tkinter as tk

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