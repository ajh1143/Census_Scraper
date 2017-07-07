from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import sys

def file_location():
    file_output_location = input("Enter a directory for output of generated text files.")
    return file_output_location

def core_logic():
    output = file_location()

    for decade in range(1880, 2020, 10):
        page_decade = "https://www.ssa.gov/oact/babynames/decades/names"+str(decade)+"s.html"
        soup = BeautifulSoup(urlopen(page_decade))
        targets = soup.find_all("tr",{"align":"right"})[1:]
        data = {
            'Rank' : [],
            'Name_Male' : [],
            'Number_Male' : [],
            'Name_Female' : [],
            'Number_Female' : []
        }

        for target in targets:
            target_acquired = target.get_text()
            z = target_acquired.split()
            data['Rank'].append(z[0])
            data['Name_Male'].append(z[1])
            data['Number_Male'].append(z[2])
            data['Name_Female'].append(z[3])
            data['Number_Female'].append(z[4])
        df_print(output, decade, data)

def df_print(file, year, populated_data_dict):
    file_output = file
    decade = year
    data = populated_data_dict
    pd.set_option('display.max_rows', 1000)
    df = pd.DataFrame(data)
    df = df[['Rank', 'Name_Male','Number_Male','Name_Female','Number_Female']]
    sys.stdout=open(file_output+str(decade)+"\.txt", "w")
    print (df)
    sys.stdout.close()

if __name__ == '__main__':
    core_logic()
