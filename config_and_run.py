# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 18:27:54 2020

@author: theo goe
"""

import os
# set path to current folder
folder_loc = os.path.dirname(os.path.realpath(__file__))
os.chdir(folder_loc)
from resources.scraper_function import twitter_scraper
import pandas as pd
from datetime import timedelta, date

###############################################################
# set your parameters
###############################################################

browser_path = 'C:/vnineteen/chromedriver.exe'

# replace the urls here with your twitter advanced searches 
# AND make sure to erase anything after the end of the query
# AKA cut your twitter advanced search query to look like this:
# https://twitter.com/search?q=hotel%20(repurposing%20OR%20repurpose)
urls = [
    'https://twitter.com/search?q=hotel%20(repurposing%20OR%20repurpose)']

# how many times to scroll down 
scroll_down_num = 4

# output file name
out_name = 'repurpose.csv'

start_date = '2020-6-1'
end_date = '2020-10-13'

# how many days between each search
# aka 2020-6-1    and then if days_between = 2
# the next search will be for 2020-6-3 till it reaches end_date
days_between = 2

# no need to change the following variable unless Twitter html changes
# its the xpath of each tweet
post_element_xpath = '//div/div/article/div/div'

###############################################################
# start of script -- no need to edit below this point
###############################################################


if __name__ == '__main__':

    # make folder to save files into
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    os.chdir('outputs')

    # run scraper to get each tweet
    df = twitter_scraper(browser_path, urls,
                         scroll_down_num, post_element_xpath,
                         start_date, end_date, days_between)

    # output the tweets
    df.to_csv(out_name)

    # ok we got the basic data in, lets parse the text
    def parse_text(text):
        try:
            text_list = str.splitlines(text)  # split by new line
            # longest_text = max(text_list, key=len)
            # return longest_text
            username = text_list[0]  # always the first element
            # find the handle in the first few elements with the @ symbol
            handle = ''.join(x for x in text_list[1:3] if '@' in x)
            # the date always goes after the dot
            # find the dot index position in list
            dot_position = text_list[1:4].index('·')
            date = text_list[dot_position + 2]  # get the date

            # check if its a reply to someone else
            # this might break if extra element after username/handle
            if text_list[4] == "Replying to ":
                reply_to = True
                reply_to_handle = text_list[5]
                text = text_list[6]
            else:
                reply_to = False
                reply_to_handle = ''
                # find the longest string in the selection of the list
                text = max(text_list[4:6], key=len)
            return pd.Series([username, handle,
                              date, reply_to, reply_to_handle, text])
        except:
            return pd.Series(['', '', '', '', '', ''])

    # run parse function
    df[['username', 'handle', 'date', 'reply_to', 'reply_to_handle', 'text']
       ] = df['all_text'].apply(parse_text)

    # output the dataset
    df.to_csv(out_name.split('.csv')[0] + '_parsed.csv')


'''
for reference, this is what the raw string looks like from scrape:

gus
@EmmArrGus
·
Oct 9
THE SIMPSONS PREDICTED ME???
2.9K views
0:05 / 0:16
7
30
255



Spookja
@ItsMeNikja
·
Oct 10
Replying to
@simpsons_vids
The Simpsons predicted YouTube Poop as well.
4
70
'''
