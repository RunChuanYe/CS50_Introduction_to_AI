import pandas as pd

df_data_set = pd.read_csv('./shopping.csv')

# get col's name
cols_name = list(df_data_set.columns)

print(cols_name)
# get specific col's domains
print(list(df_data_set['Month'].value_counts().keys()))
print(list(df_data_set['VisitorType'].value_counts().keys()))
print(list(df_data_set['Weekend'].value_counts().keys()))
print(list(df_data_set['Revenue'].value_counts().keys()))


# more easy map, using built-in lib
import calendar
month_to_number = {name: num - 1 for num, name in enumerate(calendar.month_abbr) if num}
print(month_to_number)