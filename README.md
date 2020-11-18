# Twitter_selenium
 A basic twitter scraper example using selenium -- this version adds start and end dates to maximize the number of tweets you can get via scraping with headless browser

## Prep
1. download chromedriver and keep track of where you save it (download [here](https://chromedriver.chromium.org/downloads))

2. use twitter advanced search and copy/paste the urls into the `config_and_run.py` file

## How to run
1. open up `config_and_run.py` and edit accordingly

2. you may want to change the sleep times in the resources/scraper_function.py as well to scrape faster

3. run `config_and_run.py`

## Other notes
1. I only parsed some of the tweet -- there are some variables that you'll have to extract still, but you can use the format I layed out.

2. Again, this is probs the least efficient way of gathering Tweets, but hey, if you just need a sample of temporal twitter data.. its not the end of the world to run this.