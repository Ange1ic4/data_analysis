from operator import index
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'C:\Users\PC\Downloads\popolazione-globale-per-paese-1950-2024.csv')

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
lendf = len(country_dataframe.index)

# Creating a sheet with values of average and stantard deviation for population values long the years
countries_average = {'country': [], 'average': [], 'std_deviation': []}

for p in countries_sheet:
    dado = df.query('country=="' + p + '"')
    countries_average['country'].append(p)
    countries_average['average'].append(dado['population'].mean())
    countries_average['std_deviation'].append(dado['population'].std())

countries_average = pd.DataFrame(countries_average)

# print(countries_average.head())

# Selecting ten countries with the biggest average population and ploting a barplot with these informations
# top_10_most_populous = countries_average.sort_values('average', ascending=False).head(10)
# top_10_less_populous = countries_average.sort_values('average', ascending=False).tail(10)
# top_10_mean_population = (countries_average.sort_values('average', ascending=False)).iloc[int((lendf/2)-5):int((lendf/2)+5)]
countries_average_most = countries_average.sort_values('average', ascending=False).head(10)
countries_average_less = countries_average.sort_values('average', ascending=False).tail(10)
# fig, axs = plt.subplots(1, 2, figsize=(10, 6))
# axs[0].barh(countries_average_most['country'], countries_average_most['average'])
# axs[1].barh(countries_average_less['country'], countries_average_less['average'])
# plt.show()

subtitle_1 = []
subtitle_2 = []
plt.show()

# Population growth chart for the ten most populous countries
fig, axs = plt.subplots(1, 2, figsize=(10, 6))
fig.subplots_adjust(hspace=0.5, wspace=0.3)
subtitle_1 = []
subtitle_2 = []

for country in countries_average_most:
    if country=='China' or country=="India":
        axs[0].plot(country_dataframe['years'], country_dataframe[country])
        subtitle_1.append(country)
    else:
        axs[1].plot(country_dataframe['years'], country_dataframe[country])
        subtitle_2.append(country)

axs[0].set_title('population growth\nfrom 1950 to 2024')
axs[0].set_xlabel('Year')
axs[0].set_ylabel('Number of inhabitants')
axs[0].xaxis.set_major_locator(plt.MultipleLocator(10))
axs[0].legend(subtitle_1)

axs[1].set_title('Population growth\nfrom 1950 to 2024')
axs[1].set_xlabel('Year')
axs[1].set_ylabel('Number of inhabitants')
axs[1].xaxis.set_major_locator(plt.MultipleLocator(10))
axs[1].legend(subtitle_2)

plt.show()
growth = {}

countries_std_most = countries_average.sort_values('std_deviation', ascending=False).head(10)
countries_std_less = countries_average.sort_values('std_deviation', ascending=False).tail(10)

# Calculating the population change from year to year, by country, to visualize the rate of population growth
for country in countries_std_most:
    var = country_dataframe.loc[:, country]
    g = []
    for n in range(1,len(var)):
        variation = int(var.iloc[n]-var.iloc[n-1])
        g.append(variation)
    growth['country'] = country
    growth['growth'] = g

for country in countries_std_less:
    var = country_dataframe.loc[:, country]
    g = []
    for n in range(1,len(var)):
        variation = int(var.iloc[n]-var.iloc[n-1])
        g.append(variation)
    growth['country'] = country
    growth['growth'] = g

growth = pd.DataFrame(growth)

fig, axs = plt.subplots(1, 2, figsize=(10, 6))
fig.subplots_adjust(hspace=0.5, wspace=0.3)
axs[0].plot(growth['country'], growth['growth'])
axs[0].set_title('')
axs[0].set_xlabel('')
axs[0].set_ylabel('')
axs[0].xaxis.set_major_locator(plt.MultipleLocator(10))
axs[0].legend(subtitle_1)

axs[1].set_title('Population growth\nfrom 1950 to 2024')
axs[1].set_xlabel('Year')
axs[1].set_ylabel('Number of inhabitants')
axs[1].xaxis.set_major_locator(plt.MultipleLocator(10))
axs[1].legend(subtitle_2)


# função para formatar o gráfico
