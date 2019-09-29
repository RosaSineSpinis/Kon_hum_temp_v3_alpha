import pandas
import math

class PandasDataFrameListToOneData():
    '''Takes list of paths and filenames and merge them into one, delete NULL column and sort them in ascending way'''
    def __init__(self):
        self.new_column_name = 'Date_time'


    def listToOneDataFrameConcat(self, df, filename_list, path_list):
        frames = []
        # try:
        # print(df)
        for idx, item in enumerate(path_list):
            # print(item)
            df = pandas.read_csv(item, encoding='utf-16', delimiter='\t')
            # print(type(df))
            # print(df.iloc[:,1])
            # print(df)
            # print(df.iloc[:, 2])
            # print(df.columns)
            # print(df)
            # print("Unnamed: 0" in df.columns)
            if "Unnamed: 0" in df.columns:
                df.rename(columns={'Unnamed: 0': 'Time'}, inplace=True)  # column without name, rename then
            if "Unnamed: 1" in df.columns:
                df.rename(columns={'Unnamed: 1': 'Date'}, inplace=True)  # column without name, rename then
             # print(df)
            # df.drop(df.columns[[12]], axis=1, inplace=True) #remove columns with null, idk wjy it exists
            df[self.new_column_name] = pandas.to_datetime(
                df.iloc[:, 0] + ' ' + df.iloc[:, 1])  # merge data data + time and create new column
            df[self.new_column_name] = pandas.to_datetime(df[self.new_column_name], format='%Y-%m-%d %H:%M:%S')
            df.to_csv('rewritten_' + filename_list[idx])  # we save file to csv just in case
            frames.append(df)
            df = pandas.concat(frames, ignore_index=True)
        df.sort_values(by=[self.new_column_name], inplace=True, ascending=True) #sortning
        df = df.reset_index(drop=True) #reorganise index
        for column in df.columns[:]:
            if df.loc[:, column].isnull().all():
                df.drop(df.loc[:, [column]], axis=1, inplace=True) #remove columns with null
        if 'Date' in df.columns:
            df.loc[:,'Date'] = pandas.to_datetime(df.loc[:,'Date'], format='%d/%m/%Y')
        else:
            df.rename(columns = {df.columns[1]: 'Data'}, inplace=True)
            df.iloc[:, 1] = pandas.to_datetime(df.iloc[:, 1], format='%m/%d/%Y')
        return df
    # except:
        #     raise
        # # except pandas.errors.EmptyDataError:
        #     print("input failed")
        # except ValueError:
        #     print("input failed")


    def obtainBeginningDate(self, df):
        try:
            if "Date" in df.columns:
                # print("in if")
                # print(df)
                # return df.iloc[0, df.columns.get_iloc('Date')]
                return df.loc[0, 'Date']
            else:
                # print("we are in else")
                # print(df)
                # print(df.iloc[0, 1])
                return df.iloc[0, 1]


                # print(df.iloc[0,1])
                # df.iloc['Date_time']
        except pandas.errors.EmptyDataError:
            pass
        except ValueError:
            pass

    def obtainEndingDate(self, df):
        try:
            if "Date" in df.columns:
                return df.iloc[-1, df.columns.get_loc('Date')]
            else:
                return df.iloc[-1, 1]

                # print(df.iloc[0,1])
                # df.iloc['Date_time']
        except pandas.errors.EmptyDataError:
            pass
        except ValueError:
            pass






