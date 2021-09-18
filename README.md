## demonstration-bwin
Project goal: scrape all of the tennis match odds available on the https://sports.bwin.com/ 
#
### tools:
* Python 3.9
* Scrappy framework (https://scrapy.org/)
* IDE PyCharm
* Multiple Python libraries (requirements.txt)
### considerations:
* Since there is no available free API to get data from bwin.com
I decided to scrape it with scrapy as it is described as the fastest scraping framework for python.
I did some test on my own and indeed beautifulsoap4 was way slower

* Another challenge is dynamically loaded content via JS and modern front-end frameworks,
to overcome that script is using Selenium, once scrappy spider starts crawling it will run 
webdriver to perform actions like scrolling and clicking in order to load full page, 
then return that content back to scrappy where extracting data will happen.

