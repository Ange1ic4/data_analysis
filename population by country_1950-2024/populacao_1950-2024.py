import time
from operator import index
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Data():

    def __init__(self):
        pass

    def analysis(self):

        df = pd.read_csv(r'population by country_1950-2024.csv')

        # Create a list with years
        years = np.array((list(map(str, range(1950, 2025)))))

        # Obtaining a list with countries names
        country_sheet = (df.loc[0, 'country'])
        countries_sheet = [country_sheet]
        size_sheet = len(df.index)
        n=1

        while True:
            if (df.loc[n, 'country']) != country_sheet:
                country_sheet = (df.loc[n, 'country'])
                countries_sheet.append(country_sheet)

            n += 1

            if n > size_sheet - 1:
                break

        # Obtaining data of population of each country
        countries = {'years': years}
        for country in countries_sheet:
            country_data = df.loc[df['country'] == country, 'population']
            countries[str(country)] = country_data.values.tolist()

        # Creating a dataframe in which first column is the years between 1950 and 2024, and other columns are data of population of which country during the interval.
        country_dataframe = pd.DataFrame(data=countries, index=years)

        # Creating a sheet with values of average and stantard deviation for population values long the years
        countries_average = {'country': [], 'average': [], 'std_deviation': []}

        for p in countries_sheet:
            dado = df.query('country=="' + p + '"')
            countries_average['country'].append(p)
            countries_average['average'].append(dado['population'].mean())
            countries_average['std_deviation'].append(dado['population'].std())

        countries_average = pd.DataFrame(countries_average)

        # Selecting ten countries with the biggest average population and ploting a barplot with these informations
        countries_average_most = countries_average.sort_values('average', ascending=False).head(10)
        countries_average_less = countries_average.sort_values('average', ascending=False).tail(10)
        fig, axs = plt.subplots(1, 2, figsize=(10, 6))
        fig.subplots_adjust(hspace=0.5, wspace=0.6)
        axs[0].barh(countries_average_most['country'], countries_average_most['average'])
        axs[0].set_title('Countries with the \ngreatest average population')
        axs[1].barh(countries_average_less['country'], countries_average_less['average'])
        axs[1].set_title('Countries with the \nlowest average population')
        plt.show()


        # Ploting population growth chart for the ten most populous countries
        fig, axs = plt.subplots(2, 1, figsize=(10, 6))
        fig.subplots_adjust(hspace=0.5, wspace=0.5)
        subtitle_1 = []
        subtitle_2 = []


        for country in countries_average_most['country']:
            if country=='China' or country=="India":
                axs[0].plot(country_dataframe['years'], country_dataframe[country])
                subtitle_1.append(country)
            else:
                axs[1].plot(country_dataframe['years'], country_dataframe[country])
                subtitle_2.append(country)

        self.subplots_2(axs, 'Populational growth (1950 to 2024) \nof ten most populous countries', '', 'Year', 'Number of inhabitants', subtitle_1, subtitle_2)
        plt.show()

        fig, axs = plt.subplots(2, 1, figsize=(10, 6))
        fig.subplots_adjust(hspace=0.5, wspace=0.3)
        subtitle_1 = []
        subtitle_2 = []

        # Ploting population growth chart for the ten less populous countries
        for c in range(len(countries_average_less['country'])):
            if c < 5:
                axs[0].plot(country_dataframe['years'], country_dataframe[countries_average_less.iloc[c, 0]])
                subtitle_1.append(countries_average_less.iloc[c, 0])
            else:
                axs[1].plot(country_dataframe['years'], country_dataframe[countries_average_less.iloc[c, 0]])
                subtitle_2.append(countries_average_less.iloc[c, 0])

        self.subplots_2(axs, 'Populational growth (1950 to 2024) \nof ten less populous countries', '', 'Year', 'Number of inhabitants', subtitle_1, subtitle_2)

        plt.show()

        growth = {}

        intervals = []
        for y in range(len(years) - 1):
            row = years[y] + '-' + years[y + 1]
            intervals.append(row)

        growth['years_intervals'] = intervals

        countries_std_most = countries_average.sort_values('std_deviation', ascending=False).head(10)
        countries_std_less = countries_average.sort_values('std_deviation', ascending=False).tail(10)

        # Calculating the population change  year to year, by country, to visualize the interannual populational variation
        for country in countries_std_most['country']:
            var = country_dataframe.loc[:, country]
            subtitle_1.append(country)
            g = []
            for n in range(1,len(var)):
                variation = int(var.iloc[n]-var.iloc[n-1])
                g.append(variation)
            growth[country] = g

        for country in countries_std_less['country']:
            var = country_dataframe.loc[:, country]
            g = []
            subtitle_2.append(country)
            for n in range(1,len(var)):
                variation = int(var.iloc[n]-var.iloc[n-1])
                g.append(variation)
            growth[country] = g


        growth = pd.DataFrame(growth)

        fig, axs = plt.subplots(2, 1, figsize=(10, 6))
        fig.subplots_adjust(hspace=0.5, wspace=0.3)
        subtitle_1 = []
        subtitle_2 = []

        # Ploting the interannual populational variation for ten countries with greatests standard deviations
        for c in range(1,11):
            if growth.columns[c] == "China" or growth.columns[c] == "India":
                axs[0].plot(growth['years_intervals'], growth[growth.columns[c]])
                subtitle_1.append(growth.columns[c])
            else:
                axs[1].plot(growth['years_intervals'], growth[growth.columns[c]])
                subtitle_2.append(growth.columns[c])


        self.subplots_2(axs, 'Countries with the greatest interannual populational variation\n between 1950 - 2024', '', '', '', subtitle_1, subtitle_2)
        plt.show()

        fig, axs = plt.subplots(2, 1, figsize=(10, 6))
        fig.subplots_adjust(hspace=0.5, wspace=0.3)
        subtitle_1 = []
        subtitle_2 = []

        # Ploting the interannual populational variation for ten countries with lowest standard deviations
        for c in range(11, 21):
            if c < 16:
                axs[0].plot(growth['years_intervals'], growth[growth.columns[c]])
                subtitle_1.append(growth.columns[c])
            else:
                axs[1].plot(growth['years_intervals'], growth[growth.columns[c]])
                subtitle_2.append(growth.columns[c])

        self.subplots_2(axs, 'Countries with the lowest interannual populational variation \n between 1950 - 2024', '','', '', subtitle_1,subtitle_2)
        plt.show()

    def subplots_2(self,
                   axes,
                   title_zero,
                   title_one,
                   x_label,
                   y_label,
                   subtitle_zero,
                   subtitle_one):


        axes[0].set_title(title_zero)
        axes[0].set_xlabel(x_label)
        axes[0].set_ylabel(y_label)
        axes[0].xaxis.set_major_locator(plt.MultipleLocator(10))
        axes[0].legend(subtitle_zero)

        axes[1].set_title(title_one)
        axes[1].set_xlabel(x_label)
        axes[1].set_ylabel(y_label)
        axes[1].xaxis.set_major_locator(plt.MultipleLocator(10))
        axes[1].legend(subtitle_one)


analysis = Data()
analysis.analysis()