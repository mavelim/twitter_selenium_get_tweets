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


def sleep_for(opt1, opt2):
    time_for = random.uniform(opt1, opt2)
    time_for_int = int(round(time_for))
    sleep(abs(time_for_int - time_for))
    for i in range(time_for_int, 0, -1):
        sleep(1)


def twitter_scraper(browser_path, urls, scroll_down_num, post_element_xpath):
    # setting the chromedriver path and initializing driver
    driver = webdriver.Chrome(executable_path=browser_path)
    driver.set_page_load_timeout(100)

    # create master df to append to
    master_df = pd.DataFrame()

    # loop through the list of urls listed in config_and_run.py
    for url in pbar(urls):
        driver.get(url)
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

    return master_df
