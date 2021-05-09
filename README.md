# azure-selenium-webscraper
Docker instance of a Selenium web scraper hosted on Azure Functions that pushed to a Webflow site via its API.
Set-up the Azure infrastructure according to <a href="https://github.com/rebremer/azure-function-selenium"> this repo </a>. All credits on setting-up a functioning Dockerised instance on Azure Functions go to the creator.
\n
This web scraper builds on the above app by adding scraping functionality that is triggered to run on a scheduled basis. Scraped content is then pushed to a Webflow frontend using its API.
\n
To use the Webflow functionality, modify the webflow.py file to add the relevant API key and collection IDs.

## Scraping strategies
A brief write-up on the scraping strategies used in this web scraper can be found <a href="https://shawntcytan.medium.com/web-scraping-strategies-for-selenium-python-dbca1ae81bd0">here</a>.
