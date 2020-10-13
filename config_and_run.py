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

###############################################################
###############################################################

browser_path = 'C:/vnineteen/chromedriver.exe'

urls = [
    'https://twitter.com/search?q=simpsons%20(predicted%20OR%20covid)&src=typed_query']

scroll_down_num = 5

out_name = 'output.csv'

# no need to change the following variable unless Twitter html changes
post_element_xpath = '//div/div/article/div/div'

###############################################################
###############################################################


if __name__ == '__main__':

    # make folder to save files into
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    os.chdir('outputs')

    df = twitter_scraper(browser_path, urls,
                         scroll_down_num, post_element_xpath)

    df.to_csv(out_name)

    # ok we got the basic data in, lets get the text

    def parse_text(text):
        text_list = str.splitlines(text)  # split by new line
        # longest_text = max(text_list, key=len)
        # return longest_text
        username = text_list[0]  # always the first element
        # find the handle in the first few elements with the @ symbol
        handle = ''.join(x for x in text_list[1:3] if '@' in x)
        # the date always goes after the dot
        dot_position = text_list[1:4].index('·')  # find the dot index position in list
        date = text_list[dot_position + 2]  # get the date

        # check if its a reply to someone else
        if text_list[4] == "Replying to ":  # this might break if extra element after username/handle
            reply_to = True
            reply_to_handle = text_list[5]
            text = text_list[6]
        else:
            reply_to = False
            reply_to_handle = ''
            text = max(text_list[4:6], key=len)  # find the longest string in the selection of the list
        return pd.Series([username, handle,
                          date, reply_to, reply_to_handle, text])

    # run function above
    df[['username', 'handle', 'date', 'reply_to', 'reply_to_handle', 'atext']
       ] = df['text'].apply(parse_text)

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
