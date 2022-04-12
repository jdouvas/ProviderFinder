#-----------------------------------------------------------------------
# therapists_webscrape_basic.py
# Author: Julia Douvas
# Description: Webscrapes PsychologyToday therapist search results for
#              the Princeton, NJ area to gather basic information needed
#              to later run therapists_webscrape_moreinfo.py (url of 
#              specific provider profile pages)
# Results: creation of ids.json, ids.csv files
# Credits: This code was based on Scott Edenbaum's work which can be 
#          found at https://www.linkedin.com/pulse/scraping-therapists-python-selenium-beautifulsoup-scott-edenbaum/ 
#-----------------------------------------------------------------------

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import random
import lxml
import json
import csv
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen

def scrape_me(url):   # input parameter = string url to pyschologytoday's website
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    
    providers = [] # generating empty dict
    num_of_pages_to_scrape = 25
    while num_of_pages_to_scrape >= 0:
        time.sleep(1)           # added a 1 second sleep to limit bot detection
        try:
            driver.get(url)         # open the url in selenium
        except:
            print ('bad url!')
        soup = BeautifulSoup(driver.page_source, features="lxml") # grab the content with beautifulsoup for parsing
        main_table = soup.findAll('div',{'class':'results'})[0]  # select the desired html node
        docs_per_page = len(main_table.findAll('div',{'class':'results-row'},recursive=False)) # outputs number of html node chldren - aka therapists per web page
        # save all the names and ids on a given page
        # works on 2,5,8,11,14,17,...,59
        
        i = 2
        while i <= (3*(docs_per_page - 1) +2):
            spaces_prov_name = main_table.contents[i].contents[2].contents[0].text # can redo this to be like line 56 to be more readable
            prov_name = spaces_prov_name.strip()
            raw_prov_id = main_table.contents[i].get('data-x')
            prov_id_arr = raw_prov_id.split("-")
            prov_id = prov_id_arr[2]
            prov_url = 'https://www.psychologytoday.com/us/therapists/new-jersey/' + prov_id
            
            provider = {}
            keys = ["name", "id", "url"]
            provider["name"] = prov_name
            provider["id"] = prov_id
            provider["url"] = prov_url
            i += 3

            providers.append(provider)
        
        next_page_txt = soup.find("span", {"class": "chevron-right"}).text
        next_page_url = soup.find("a", {"title": "Next Therapists in Princeton, Mercer County, New Jersey"})['href'] # url for next page of content
        url = next_page_url       # set url = next page url to prepare for next page of scraping
        num_of_pages_to_scrape -= 1
    
    return providers # returns scrapped data as dict of dictionaries

def main():
    url = 'https://www.psychologytoday.com/us/therapists/nj/princeton'
    njdocs = scrape_me(url)
    with open('ids.json', 'w') as fp:
        json.dump(njdocs, fp)
    
    with open('ids.json') as json_file:
        jsondata = json.load(json_file)
 
    data_file = open('ids.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)
    count = 0
    for data in jsondata:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    data_file.close()


if __name__ == '__main__':
    main()
