# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 18:27:54 2020

@author: theo goe
"""

# imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import pandas as pd
from progressbar import ProgressBar
pbar = ProgressBar()
from datetime import timedelta, date
from datetime import datetime
from dateutil.relativedelta import relativedelta

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")



def sleep_for(opt1, opt2):
    time_for = random.uniform(opt1, opt2)
    time_for_int = int(round(time_for))
    sleep(abs(time_for_int - time_for))
    for i in range(time_for_int, 0, -1):
        sleep(1)


def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 30):
        yield date1 + timedelta(n)


def list_of_dates(start_date, end_date, num_days):
    cur_date = start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()

    dates_list = []
    dates_list.append(start_date)
    while cur_date < end:
        # print(cur_date)
        cur_date += relativedelta(days=num_days)
        dates_list.append(cur_date)

    # if last date is after the end date, remove
    if dates_list[-1] > end:
        dates_list.pop(-1)
        
    # add the last day
    dates_list.append(end)
    # list of tuples of each date pairing
    tup_list = []
    counter = 1
    for i in dates_list:
        # print(i)
        try:
            tup_list.append((i,dates_list[counter]))
            counter += 1
        except:  # lazy way to skip last date pairing
            pass
    return tup_list


def twitter_scraper(browser_path, urls, scroll_down_num, post_element_xpath,
                    start_date, end_date, days_between):

    # setting the chromedriver path and initializing driver
    driver = webdriver.Chrome(options=chrome_options)
    #driver = webdriver.Chrome(executable_path=browser_path)
    driver.set_page_load_timeout(100)

    # create master df to append to
    master_df = pd.DataFrame()

    dates_list = list_of_dates(start_date, end_date, num_days=days_between)

    # loop through the list of urls listed in config_and_run.py
    for orig_url in pbar(urls):
        print(str(orig_url))
        for day_tup in dates_list:
            print(str(day_tup[0]))
            print(str(day_tup[1]))
            url = orig_url + '%20until%3A' + str(day_tup[1]) + \
                '%20since%3A' + str(day_tup[0]) + '&src=typed_query'

            driver.get(url)
            print(str(url))
            sleep_for(10, 15)  # sleep a while to be safe

            # scroll x number of times
            for i in range(0, scroll_down_num):
                # scroll down
                driver.find_element_by_xpath('//body').send_keys(Keys.END)
                sleep_for(4, 7)

            # get a list of each post
            post_list = driver.find_elements_by_xpath(post_element_xpath)

            post_text = [x.text for x in post_list]

            print(post_text)

            # create temp dataset of each tweet
            temp_df = pd.DataFrame(post_text, columns={'all_text'})

            master_df = master_df.append(temp_df)
            print('master df len   ' + str(len(master_df)))
            print()

    return master_df
