import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import pandas
from pandas.plotting import register_matplotlib_converters



class Plotter():
    '''Two plottig functions, takes number of series and their data and plot them in one or many graphs'''
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
        # print(dt)


        return None


    def plotAllInOne(self, cb_checked_list_string, df, graph_title_name):
        # TODO exceptions while closed without user
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
