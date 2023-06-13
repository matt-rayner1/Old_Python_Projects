# IWF_scraper
A python web scraper bot for getting all competition data for the current top international weightlifters.

(Writes data to .csv files)

## Getting Started

### Prerequisites
Python modules required:
```
Selenium (w/ Geckodriver for Firefox)
time
pandas
csv
```

### Setting up/installation
1) Install the required modules listed in 'Prerequisites'
2) Download GeckoDriver (https://github.com/mozilla/geckodriver/releases/tag/v0.26.0), and all 3 scripts ('IWF_scrape_STABLE.py', 'IWF_clean_overview.py', 'IWF_clean_athletes.py') and put in the same dedicated folder.
3) In 'IWF_scrape_STABLE.py', change the webdriver path in \_\_init__ of the class IWFbot() to the path of your GeckoDriver.

### Running the script(s)
1) run 'IWF_scrape_STABLE.py': ```>python -i IWF_scrape_STABLE.py```. This will take about 1 - 2 hours depending on internet speed.
2) run 'IWF_clean_overview.py': ```>python -i IWF_clean_overview.py```. This will clean the '[0]Overview' files from step 1.
3) run 'IWF_clean_athletes.py': ```>python -i IWF_clean_athletes.py```. This will clean the individual athlete data. 
!!WARNING!!: only run 2. and 3. ONE TIME, otherwise they will corrupt the data.

## Built with
Python 3.8

## Author
Matthew Rayner (https://github.com/matt-rayner1)
