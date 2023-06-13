from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException as NSEE
from selenium.common.exceptions import StaleElementReferenceException as SERE
from time import sleep
import pandas as pd
import csv

'''
PROGRAM NAME:       IWF_scrape_STABLE.py
AUTHOR:             Matthew Rayner
DEPENDENCIES:       Selenium (w/ Geckodriver for Firefox), time, pandas, csv
DESCRIPTION:        Interacts with IWF qualifier database to get current top lifters in each category/weightclass/gender
'''

class IWFbot():
    #Change webdriver depending on browser choice, and driver location
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path=r'/your/path/here')
        self.driver.get('https://www.iwf.net/qualif/menu/')
        self.driver.implicitly_wait(5)
    
    #Refreshes driver session due to memory leak issues with Firefox.
    def refresh_driver(self, gender):
        self.driver.quit()
        self.driver = webdriver.Firefox(executable_path=r'/your/path/here')
        self.driver.get('https://www.iwf.net/qualif/menu/')
        self.driver.implicitly_wait(5)
        self.gender_choice(gender)

    #Choose from the [men][women] button at the top of the page
    def gender_choice(self, gender):
        self.driver.switch_to.default_content()
        if gender == "Men":
            men_btn = self.driver.find_element_by_xpath('//*[@id="item_14"]')
            men_btn.click()
        elif gender == "Women":
            women_btn = self.driver.find_element_by_xpath('//*[@id="item_15"]')
            women_btn.click()
        
        #Rest of data is inside an iframe in the DOM, this is required to find other xpaths
        iframe = self.driver.find_element_by_xpath('//*[@id="iframe_menu"]')
        self.driver.switch_to.frame(iframe)
    
    #Gets the overview of current top lifters for a given gender and weight class(/category).
    #   stores as a .csv of form "<Gender>_<category>_0[overview].csv"
    #   function returns names of all athletes in the category, for use in scrape_athlete()
    def scrape_overview(self, gender, category):        
        category_element = self.driver.find_element_by_xpath('//a[text() = "{}"]'.format(category))
        category_element.click()
        
        #Scrolls down to bottom of page, to load relevant <tr> tags into DOM, 
        #   then puts entire table into a .csv
        i = 5
        while i:
            body = bot.driver.find_element_by_css_selector('body')
            body.send_keys(Keys.END)
            sleep(0.5)
            i -= 1
        filename = '{}_{}_0[OVERVIEW].csv'.format(gender, category)
        table_ref = self.driver.find_element_by_xpath('//*[@id="sc-ui-grid-body-466e086e"]/tbody')
        with open(filename, 'w', newline='') as csvfile:
            wr = csv.writer(csvfile)
            for row in table_ref.find_elements_by_css_selector('tr'):
                wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
            csvfile.close()
        
        #Returns list of athlete names in current weight class
        ret_file = pd.read_csv(filename)
        return ret_file.Name

    #Finds athlete of given name, clicks to open new page
    def athlete_entry(self, gender, category, name):
        for attempt in range(5):
            try:
                name_element = self.driver.find_element_by_xpath('//a[contains(text(),"{}")]'.format(name))
                name_element.click()
            except NSEE:
                print("Name not found in DOM for athlete {}_{}_{}, attempt {}. Retrying...".format(gender, category, name, attempt+1))
                if attempt == 4:
                    print("Error, athlete not found in overview table. Moving on")
                    unsuccessfuls.write("{}_{}_{}\n".format(gender, category, name))
                    return
            break

    #Grab table for this name, store in .csv with name formatted based on gender, class and name.
    #   For some unknown reason, putting a <try:except:> block in this function returns a blank csv, 
    #   hence it is put in main driver instead
    def scrape_table(self, gender, category, name):
        table_ref2 = self.driver.find_element_by_xpath('//*[contains(@id, "sc-ui-grid-body")]')
        filename2 = '{}_{}_{}.csv'.format(gender, category, name)
        with open(filename2, 'w', newline='') as csvfile:
            wr = csv.writer(csvfile)
            for row in table_ref2.find_elements_by_css_selector('tr'):
                wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])

    #Presses the 'back' button to return to overview page
    def back_btn(self, gender, category, name):
        for attempt in range(5):
            try:
                back_btn = self.driver.find_element_by_xpath('//*[@id="sai_top"]')
                back_btn.click()
            except NSEE:
                print("Back button not found during loop, for athlete {}, attempt {}. Retrying...".format(name, attempt+1))
                if attempt == 4:
                    print("Error, back button not found. ")
                    unsuccessfuls.write("{}_{}_{}\n".format(gender, category, name))
                    return
            break
    
    #sorts SERE errors from scrape_table()
    def except_SERE(self, gender, category, name, attempt):
        print("Table reset for athlete {}_{}_{}, attempt {}. Retrying...".format(gender, category, name, attempt+1))
        check_valids.write("{}_{}_{}\n".format(gender, category, name))
        if attempt == 4:
            print("Error, table not copied successfuly. Moving on")
            unsuccessfuls.write("{}_{}_{}\n".format(gender, category, name))

#current IWF standard gender/categories
genders = ["Men","Women"]
men_categs = ["55kg","61kg","67kg","73kg","81kg","89kg","96kg","102kg","109kg","+109kg"]
women_categs = ["45kg","49kg","55kg","59kg","64kg","71kg","76kg","81kg","87kg","+87kg"]

#------------------------------MAIN DRIVER-----------------------------
#Creates object from IWFbot() class and logically executes its methods.
#Note: The try/except for bot.scrape_table() only works properly 
#      from the main driver loop. It makes the loop look ugly 
#      but its the only solution I've found.
unsuccessfuls = open("0_unsuccessfuls.txt", "w")
check_valids = open("0_check_valid.txt", "w")

bot = IWFbot()

for gender in genders:
    bot.gender_choice(gender)
    if gender == "Men":
        for man_categ in men_categs:
            sleep(2)
            names = bot.scrape_overview(gender, man_categ)
            for name in names:
                bot.athlete_entry(gender, man_categ, name)
                for attempt in range(5):
                    try:
                        bot.scrape_table(gender, man_categ, name)
                    except SERE:
                        bot.except_SERE(gender, man_categ, name, attempt)
                bot.back_btn(gender, man_categ, name)
            bot.refresh_driver(gender)
    elif gender == "Women":
        for woman_categ in women_categs:
            sleep(2)
            names = bot.scrape_overview(gender, woman_categ)
            for name in names:
                bot.athlete_entry(gender, woman_categ, name)
                for attempt in range(5):
                    try:
                        bot.scrape_table(gender, woman_categ, name)
                    except SERE:
                        bot.except_SERE(gender, woman_categ, name, attempt)
                bot.back_btn(gender, woman_categ, name)
            bot.refresh_driver(gender)

#post-driver report

print("These athletes were not scraped successfully (please refer to 'unsuccessfuls.txt'): ")
for line in unsuccessfuls.read():
    print(line)
print("These athletes MAY not have been scraped successfully (please refer to 'check_valid.txt'):")
for check in check_valids.read():
    print(line)
print("\nProgram ended successfully.")

unsuccessfuls.close()
check_valids.close()
