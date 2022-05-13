#Input selection
print("Which day do you want to get data?")
print("1. Yesterday")
print("2. 2 days ago")

selection = int(input("Input your selection: "))

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Create an URL object
url = 'https://www.worldometers.info/coronavirus/'

# Create object page
page = requests.get(url)

# parser-lxml = Change html to Python friendly format
# Obtain page's information
soup = BeautifulSoup(page.text, 'lxml')

# Obtain information from tag <table>
table1 = soup.find('table', id='main_table_countries_yesterday2' if selection == 2 else 'main_table_countries_yesterday')

# Obtain every title of columns with tag <th>
headers = []
for i in table1.find_all('th'):
    title = i.text
    headers.append(title)

headers[10] = "TotalCases/1M pop"
headers[13] = "Test/1M pop"

# Create a dataframe
mydata = pd.DataFrame(columns = headers)

# Create a for loop to fill mydata
for j in table1.find_all('tr')[1:]:
    row_data = j.find_all('td')
    row = [i.text for i in row_data]
    length = len(mydata)
    mydata.loc[length] = row

# Drop and clearing unnecessary rows
mydata.drop(mydata.index[236:], inplace=True)
mydata.drop(mydata.index[0:7], inplace=True)
mydata.reset_index(inplace=True, drop=True)

# Drop “#” column
mydata.drop("#", inplace=True, axis=1)

#Get date with selection
from datetime import date, timedelta
_date = (date.today() - timedelta(days = selection)).strftime("%Y_%m_%d")
fout_name = 'Covid_Data_{}.csv'.format(_date)

# Export to csv
mydata.to_csv(fout_name, index=False)

print("\nOutput file: {}\n".format(fout_name))

# Try to read csv
mydata2 = pd.read_csv(fout_name)
print(mydata2)