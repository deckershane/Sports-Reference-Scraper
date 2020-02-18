# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
import statsmodels.api as smi

# NBA season we will be analyzing
year = 2019
# URL page we will scraping (see image above)
url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
# this is the HTML from the given URL
html = urlopen(url)
soup = BeautifulSoup(html)
# Obtain all column headers
soup.findAll('tr',limit=2)

# use getText()to extract the text we need into a list
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
# exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
headers = headers[1:]
headers

#avoid the first header row
rows = soup.findAll('tr')[1:]
player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

#put data in data frame
df = pd.DataFrame(player_stats, columns = headers)
df.head(10)

#------------------------------------------------------#
# Run for soccer reference
url2 = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
html2 = urlopen(url2)
soup = BeautifulSoup(html2)

soup.findAll('tr')

s_headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
s_headers

#record season stats
srows = soup.findAll('tr')[2:]
stats = [[td.getText() for td in srows[i].findAll('td')] for i in range(len(srows))]


#finalize data frame
sdf = pd.DataFrame(stats, columns = s_headers)
sdf.head(10)

#-------------------------------------------------------------------#
# Run for Hockey data
def hockey_scrape(year_list, url = None):
    '''
    Scrapes hockey-reference.com for skater and goalie data.
    '''
    sk_df_final = pd.DataFrame()
    go_df_final = pd.DataFrame()
    
    for year in year_list:
        # skaters URL
        sk_url = "https://www.hockey-reference.com/leagues/NHL_{}_skaters.html".format(year)
        sk_html = urlopen(sk_url)
        # ping URL for data
        sk_soup = BeautifulSoup(sk_html)
        # Find all the tables on the webpage
        sk_soup.findAll('tr', limit=2)
        
        # Grab headers of data table
        sk_headers = [th.getText() for th in sk_soup.findAll('tr')[1].findAll('th')]
        sk_headers = sk_headers[1:]
        
        # Grab player stats for table
        sk_rows = sk_soup.findAll('tr')[2:]
        sk_stats = [[td.getText() for td in sk_rows[i].findAll('td')] for i in range(len(sk_rows))]
        
        # Build data frame with headers and player data
        sk_df = pd.DataFrame(sk_stats, columns = sk_headers); sk_df['Season'] = year
        sk_df_final = sk_df_final.append(sk_df)
        sk_df_final = sk_df_final.reset_index(drop = True)
        
        # Clean up data frame, remove None rows
        sk_nums = []
        for row in range(len(sk_df_final.Player)):
            if type(sk_df_final.Player[row]) == type(None):
                sk_nums.append(row)
        #drop all rows with None Goalie names
        sk_df_final = sk_df_final.drop(sk_df_final.index[sk_nums])
                
    # ------------------------------------------------------------------------------------#
        # goalie URL
        go_url = "https://www.hockey-reference.com/leagues/NHL_{}_goalies.html".format(year)
        go_html = urlopen(go_url)
        # Ping webpage
        go_soup = BeautifulSoup(go_html)
        
        # find all tables on the webpage
        go_soup.findAll('tr', limit=2)
        
        # Grab headers of data table
        go_headers = [th.getText() for th in go_soup.findAll('tr')[1].findAll('th')]
        go_headers = go_headers[1:]
        
        # Grab goalie stats for table
        go_rows = go_soup.findAll('tr')[2:]
        go_stats = [[td.getText() for td in go_rows[i].findAll('td')] for i in range(len(go_rows))]
        
        # Build data frame with headers and player data
        go_df = pd.DataFrame(go_stats, columns = go_headers); go_df['Season'] = year
        go_df_final = go_df_final.append(go_df)
        go_df_final = go_df_final.reset_index(drop = True)
        
        # Clean up data frame, remove None rows
        go_nums = []
        for row in range(len(go_df_final.Player)):
            if type(go_df_final.Player[row]) == type(None):
                go_nums.append(row)
        #drop all rows with None Goalie names
        go_df_final = go_df_final.drop(go_df_final.index[go_nums])

    return sk_df_final, go_df_final

sk_df, go_df = hockey_scrape([2018,2019])

# Write data frames to an excel file
import os
os.chdir("Documents")

with pd.ExcelWriter('NHL_Player Data.xlsx') as writer:  # doctest: +SKIP
    sk_df.to_excel(writer, sheet_name='Skater Data')
    go_df.to_excel(writer, sheet_name='Goalie Data')
import subprocess
print("Move the file into the correct folder. Please delete the file copy in the Yelp Scrap folder")
subprocess.Popen('explorer "Documents"')

