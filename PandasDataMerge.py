import pandas
import math

class PandasDataFrameListToOneData():
    '''Takes list of paths and filenames and merge them into one, delete NULL column and sort them in ascending way'''
    def __init__(self):
        self.new_column_name = 'Date_time'


    def listToOneDataFrameConcat(self, df, filename_list, path_list):
        frames = []
        try:
            for idx, item in enumerate(path_list):
                df = pandas.read_csv(item, encoding='utf-16', delimiter='\t')
                df.rename(columns={'Unnamed: 0': 'Time'}, inplace=True)  # column without name, rename then
                df.rename(columns={'Unnamed: 1': 'Date'}, inplace=True)  # column without name, rename then
                # df.drop(df.columns[[12]], axis=1, inplace=True) #remove columns with null, idk wjy it exists
                df[self.new_column_name] = pandas.to_datetime(
                    df.iloc[:, 0] + ' ' + df.iloc[:, 1])  # merge data data + time and create new column
                df[self.new_column_name] = pandas.to_datetime(df[self.new_column_name], format='%Y-%m-%d %H:%M:%S')
                df.to_csv('rewritten_' + filename_list[idx])  # we save file to csv just in case
                frames.append(df)
                df = pandas.concat(frames, ignore_index=True)
            df.sort_values(by=[self.new_column_name], inplace=True, ascending=True) #sortning
            df.loc[:,'Date'] = pandas.to_datetime(df.loc[:,'Date'], format='%d/%m/%Y')
            # print(df.loc[:,'Date'])
            # print(df.iloc[:,12])
            print(df.iloc[:, 11].isnull().all())
            print(df.iloc[:, 12].isnull().all())
            # print(df)
            # print(df.loc[:,self.new_column_name].dt.date)
            # print(df.iloc[-1, df.columns.get_loc('Date')])
            self.createCheckBoxListName(df)
            return df
        except pandas.errors.EmptyDataError:
            print("input failed")
        except ValueError:
            print("input failed")


    def obtainBeginningDate(self, df):
        try:
            return df.iloc[0, df.columns.get_loc('Date')]
                # print(df.iloc[0,1])
                # df.iloc['Date_time']
        except pandas.errors.EmptyDataError:
            pass
        except ValueError:
            pass

    def obtainEndingDate(self, df):
        try:
            return df.iloc[-1, df.columns.get_loc('Date')]
                # print(df.iloc[0,1])
                # df.iloc['Date_time']
        except pandas.errors.EmptyDataError:
            pass
        except ValueError:
            pass


    def createCheckBoxListName(self, df):

        check_box_list_name = []
        for column in df.columns[2:]:
            if column == "Date_time":
                continue
            elif not df.loc[:, column].isnull().all():
                check_box_list_name .append(column)
        print(check_box_list_name)
        return check_box_list_name



