## demonstration-bwin
Project goal: scrape all of the tennis match odds available on the https://sports.bwin.com/ 
#
### tools:
* Python 3.9
* Scrappy framework (https://scrapy.org/)
* Selenium web-drive (https://pypi.org/project/selenium/)
* IDE PyCharm
* Multiple Python libraries (requirements.txt)

### structure:
Following scrapy framework structure most code is written in:
- bwin\bwin\spiders\tennis_spider.py
- bwin\bwin\items.py
- bwin\bwin\tools.py

### running:
In order ro run script and save data to json file:
 
<code>cd bwin </code>

<code>scrapy crawl tennis -o file.json</code>

<code>file.json</code> with content should appear inside /bwin directory

### considerations:
* Since there is no available free API to get data from bwin.com
I decided to scrape it with scrapy as it is described as the fastest scraping framework for python.
I did some test on my own and indeed beautifulsoap4 was way slower. Runtime bottleneck in my script 
is time to load full content (scrolling + waiting)

* Another challenge is dynamically loaded content via JS and modern front-end frameworks,
to overcome that script is using Selenium, once scrappy spider starts crawling it will run 
webdriver to perform actions like scrolling and clicking in order to load full page, 
then return that content back to scrappy where extracting data will happen.

* JSON file will store only results where all values are present - complete, incomplete
rows are stored in list for testing purposes

* After script execution there is basic summary shown in console (number of scraped items, elapsed time etc)
#
### summary:
* Writing this code took me 12-15h
* Tested on Windows 10 64bit and Ubuntu 64bit.
* Working with Chrome and Firefox  Selenium drivers
* It was my first time with Scrapy and scraping dynamically loaded content from page
