"""
AJH
BeautifulSoup, Pandas, Python web scraper
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import sys

#Retrieves the user's desired text file output location in the form of C:\User\Name\Location
def file_location():
    file_output_location = input("Enter a directory for output of generated text files.")
    return file_output_location

#Scraping method, iterates through each web page based on decade and creates a dict of the scraped 
#data to be passed to df_print()
def core_logic():
    output = file_location()
    #For each decade in range 1880-2010
    for decade in range(1880, 2020, 10):
        #Pass correct webpage based on decade
        page_decade = "https://www.ssa.gov/oact/babynames/decades/names"+str(decade)+"s.html"
        #Open URL w/ BeautifulSoup
        soup = BeautifulSoup(urlopen(page_decade))
        #Assign targets to parse
        targets = soup.find_all("tr",{"align":"right"})[1:]
        #Create empty Dictionary to add results
        data = {
            'Rank' : [],
            'Name_Male' : [],
            'Number_Male' : [],
            'Name_Female' : [],
            'Number_Female' : []
        }
        #For each target dataset
        for target in targets:
            #Extract text
            target_acquired = target.get_text()
            #Split target values
            z = target_acquired.split()
            #Append to each category
            data['Rank'].append(z[0])
            data['Name_Male'].append(z[1])
            data['Number_Male'].append(z[2])
            data['Name_Female'].append(z[3])
            data['Number_Female'].append(z[4])
        df_print(output, decade, data)

#Transforms the dataset into a DataFrame using Pandas, prints to the previously acquired output location        
def df_print(file, year, populated_data_dict):
    #Assign output location/filename
    file_output = file
    #Assign current year
    decade = year
    #Assign the dictionary to data
    data = populated_data_dict
    #Allow max rows
    pd.set_option('display.max_rows', 1000)
    #Create DataFrame
    df = pd.DataFrame(data)
    #Assign datapoints to columns
    df = df[['Rank', 'Name_Male','Number_Male','Name_Female','Number_Female']]
    #Print a local csv copy to sepcified location, stored as .txt file named for each decade
    sys.stdout = open(file_output+"/"+str(decade)+".txt", "w")
    print (df)
    #Close output
    sys.stdout.close()

if __name__ == '__main__':
    core_logic()
