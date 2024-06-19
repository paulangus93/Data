"""
Task summary

This script functions to calculate both the crude and age-standardised death rate in the United States and Uganda in 2019, per 100,000 people.

The first step is to get the available data into a readable and processable form by referring to the data sources outlined below.

Data sources:
    
"Ahmad OB, Boschi-Pinto C, Lopez AD, Murray CJ, Lozano R, Inoue M (2001). Age standardization of rates: a new WHO standard."
Table 1 contains a sample population distribution that I use in calculating the age-adjusted death rates.

"Table of age-specific death rates of COPD"
Provides the death rates of COPD, per 100,000 people, in the US and Uganda in 2019.

"UN World Population Prospects (2022) — Population Estimates 1950-2021"
Provides data for the age-based population distributions of the US and Uganda in 2019.

The data analysis procedure is as follows:
Create a dictionary containing the collected data, with keys "Age group", "Sample Pop %", "US Population", "US Death Rate", "Uganda Population", and "Uganda Death Rate", taking care that each value has the same length and that the data corresponds to the correct age groups.
Create a pandas dataframe from this dictionary, and visually confirm that the data within is structured appropriately via printing.
Add columns to the dataframe that represent the age-based population distribution in the US and Uganda, the values for which are calculated by dividing the population within each age group by the total population, and multiplying by 100. Labels are "US Pop %" and "Uganda Pop %".
Calculate crude death rates by multiplying the population percentages with the death rates, adding the resulting column as "Expected Deaths US/Uganda" as a new column, and sum this column over all age groups.
Calculate age adjusted death rates by multiplying the sample population percentages with the death rates, adding the resulting column as "Expected Deaths US/Uganda Adjusted", and sum this column over all age groups.
This process adds some additional data to the dataframe for further analysis if necessary, thus it is displayed at the end for clarity.

Results:
    
Crude Death Rate for COPD in the United States: 57.2 per 100,000 people
Crude Death Rate for COPD in Uganda: 5.8 per 100,000 people
Age-adjusted Death Rate for COPD in the United States: 28.4 per 100,000 people
Age-adjusted Death Rate for COPD in Uganda: 28.7 per 100,000 people

"""
import pandas as pd

#create a table from available data
data_dictionary = {
    "Age group": ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85+"],
    "Sample Pop %": [8.86, 8.69, 8.60, 8.47, 8.22, 7.93, 7.61, 7.15, 6.59, 6.04, 5.37, 4.55, 3.72, 2.96, 2.21, 1.52, 0.91, 0.63],
    "US Population": [19849000,20697000,22092000,21895000,21872000,23407000,22842000,22297000,20695000,21244000,21346000,22348000,20941000,17501000,13689000,9273000,6119000,6214000],
    "US Death Rate": [0.04, 0.02, 0.02, 0.02, 0.06, 0.11, 0.29, 0.56, 1.42, 4.00, 14.13, 37.22, 66.48, 108.66, 213.10, 333.06, 491.10, 894.45],
    "Uganda Population": [7329000,6614000,5899000,5151000,4348000,3500000,2619000,1903000,1504000,1235000,953000,687000,500000,353000,197000,93000,44000,20000],
    "Uganda Death Rate": [0.40, 0.17, 0.07, 0.23, 0.38, 0.40, 0.75, 1.11, 2.04, 5.51, 13.26, 33.25, 69.62, 120.78, 229.88, 341.06, 529.31, 710.40]
}

#! Create a pandas dataframe from the above table
df = pd.DataFrame(data_dictionary)

#! Display the dataframe
print(df)

#! Add to the dataframe the calculated population distributions
# Note that obtaining a percentage is purely for consistency with the sample population data.
df["US Pop %"] = (df["US Population"] / df["US Population"].sum()) * 100
df["Uganda Pop %"] = (df["Uganda Population"] / df["Uganda Population"].sum()) * 100

#! Calculate expected deaths for each age group by multiplying death rate by the population weights
# Divided by 100 again, thus making the above step redundant. But I like data consistency so ¯\_(ツ)_/¯
df["Expected Deaths US"] = (df["US Pop %"]) / 100 * df["US Death Rate"]
df["Expected Deaths Uganda"] = (df["Uganda Pop %"]) / 100 * df["Uganda Death Rate"]

#! Sum the expected deaths across all age groups to get the crude death rates
crude_death_rate_us = df["Expected Deaths US"].sum()
crude_death_rate_uganda = df["Expected Deaths Uganda"].sum()

#! Display the crude death rates
print("Crude Death Rate for COPD in the United States: {:.1f} per 100,000 people".format(crude_death_rate_us))
print("Crude Death Rate for COPD in Uganda: {:.1f} per 100,000 people".format(crude_death_rate_uganda))

#! Calculate expected deaths for each age group
df["Expected Deaths US Adjusted"] = (df["Sample Pop %"]) / 100 * df["US Death Rate"]
df["Expected Deaths Uganda Adjusted"] = (df["Sample Pop %"]) / 100 * df["Uganda Death Rate"]

#! Sum the expected deaths for each age group by multiplying death rate by the standard population weight.
adj_death_rate_us = df["Expected Deaths US Adjusted"].sum()
adj_death_rate_uganda = df["Expected Deaths Uganda Adjusted"].sum()

#! Display the adjusted death rates
print("Age-adjusted Death Rate for COPD in the United States: {:.1f} per 100,000 people".format(adj_death_rate_us))
print("Age-adjusted Death Rate for COPD in Uganda: {:.1f} per 100,000 people".format(adj_death_rate_uganda))

#! Display the updated dataframe for future reference if necessary
print(df)
