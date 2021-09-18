## demonstration-bwin
Project goal: scrape all of the tennis match odds available on the https://sports.bwin.com/ 
#
### tools:
* Python 3.9
* Scrappy framework (https://scrapy.org/)
* Selenium web-drive
* IDE PyCharm
* Multiple Python libraries (requirements.txt)

### structure:
Following scrapy framework structure most code is written in:
- bwin\bwin\spiders\tennis_spider.py
- bwin\bwin\items.py
- bwin\bwin\tools.py

###running:
In order ro run script and save data to json file:
 
<code>cd bwin </code>

<code>scrapy crawl tennis -o file.json</code>





### considerations:
* Since there is no available free API to get data from bwin.com
I decided to scrape it with scrapy as it is described as the fastest scraping framework for python.
I did some test on my own and indeed beautifulsoap4 was way slower

* Another challenge is dynamically loaded content via JS and modern front-end frameworks,
to overcome that script is using Selenium, once scrappy spider starts crawling it will run 
webdriver to perform actions like scrolling and clicking in order to load full page, 
then return that content back to scrappy where extracting data will happen.

