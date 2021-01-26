import pandas as pd
import numpy as np

class streamLitFunc:
    
    def plot_case_by_country_and_date(self, countries, df, log = False, date = '20200101', date_end = 0):

        if log == False:
            if date_end == 0:
                data = df['cases'][countries].rolling(14, win_type='triang').mean().loc[date:]
            else :
                data = df['cases'][countries].rolling(14, win_type='triang').mean().loc[date:date_end]
        else :
            if date_end  == 0:
                data = df['cases'][countries].rolling(14, win_type='triang').mean().loc[date:]
            else:
                data = df['cases'][countries].rolling(14, win_type='triang').mean().loc[date: date_end]
        
        fig = self.graph_plot(data.index, data, "Number of cases by date, smoothed.")

        return fig



    def plot_by_wave(self, df, countries, date_start, date_end, first_wave = True):

        df['daynum'] = (df.index - df.index.min()).days
        measure  = 'cases'
        pmeasure = 'pcases'

        if type(date_end)  != str:
            date_end = str(date_end)

        if first_wave:
            df_pred = pd.DataFrame({'x':df['daynum'], 'y':df[measure][countries].loc[:date_end].rolling(7).mean()})
            deg = 4
        else :
            df_pred = pd.DataFrame({'x':df['daynum']-7, 'y':df[measure][countries].loc[date_start:date_end].rolling(14).mean()})
            deg = 8

        df_pred = df_pred[df_pred['y'] > 100]
        fit = np.polyfit(x=df_pred['x'], y=df_pred['y'], deg=deg, full=True)
        df_pred['p'] = np.polyval(fit[0], df_pred['x'])
        df[(pmeasure, countries)] = 10 ** np.polyval(fit[0], df['daynum'])
        df[[(measure, countries), (pmeasure, countries)]].plot(figsize=(16, 9), grid=True)

        if first_wave:
            df[[(measure, countries), (pmeasure, countries)]].cumsum().plot(figsize=(16, 9), grid=True)
        else:
            df[[(measure, countries), (pmeasure, countries)]].loc[date_start:].cumsum().plot(figsize=(16, 9), grid=True)

        def graph_plot(self, x, y, title, countries=countries):
            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)

            ax.plot(x, y)

            ax.set_title(title)

            ax.set_xlabel("Date")
            ax.set_ylabel("Number of cases")

            ax.legend(countries)

            return fig
