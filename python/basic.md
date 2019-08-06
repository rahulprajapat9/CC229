# Basics

1. lambda function
g = lambda x : x + 10

2. pandas read_csv and date_time formatting:
df = pandas.read_csv('lapp_data.csv', delimiter=';', parse_dates=[['Date', 'Time']], index_col='Date_Time')
