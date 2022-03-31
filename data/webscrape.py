# import libraries
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
# import pandas as pd
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen

# Step 1: Webscrape search page for all the names and ids for all providers in New Jersey

def scrape_me(url):   # input parameter = string url to pyschologytoday's website
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    
    providers = [] # generating empty dict
    num_of_pages_to_scrape = 50
    while num_of_pages_to_scrape >= 0:
        time.sleep(1)           # added a 1 second sleep to limit bot detection
        try:
            driver.get(url)         # open the url in selenium
        except:
            print ('bad url!')
        soup = BeautifulSoup(driver.page_source, features="lxml") # grab the content with beautifulsoup for parsing
        main_table = soup.findAll('div',{'class':'results'})[0]  # select the desired html node
        # /html/body/div[1]/div/div/div[7]/div[1] - full XML path for the first provider page
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
        next_page_url = soup.find("a", {"title": "Next Therapists in New Jersey"})['href'] # url for next page of content
        url = next_page_url       # set url = next page url to prepare for next page of scraping
        num_of_pages_to_scrape -= 1

        # next_page_txt = soup.find("span", {"class": "chevron-right"}).text
        # if next_page_txt == 'Next':  # if a 'next page' exists...
        #     next_page_url = soup.find("a", {"title": "Next Therapists in New Jersey"})['href'] # url for next page of content
        #     url = next_page_url       # set url = next page url to prepare for next page of scraping
        # else:
        #     print("Scraping Complete!")
        #     break
    
    return providers # returns scrapped data as dict of dictionaries

def main():
    url = 'https://www.psychologytoday.com/us/therapists/new-jersey'
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


# Step 2: To get from each provider and store in JSON directory
#   Provider Name (string) 
#   ID number (int)
#   Titles / Degrees (list)
#   Specialties / Issues (list)
#   Finances (dict)
#   Insurances accepted (list)
#   Cost per session (double)
#   Pay by (list)
#   Additional notes from provider (string)
#   More Info (link to PsychologyToday profile)

# Where to find:
#   Provider Name: <div class="row hidden-sm-down profile-name-phone">
#   ID number: needed from URL
#   Titles / Degrees: <div class="row hidden-sm-down profile-name-phone">
#   Specialties: <div class="col-xs-12 col-sm-12 col-md-5 col-lg-5 specialties-column">
#   Finances: <div class="profile-finances details-section">
#   Insurances accepted (list)
#   Cost per session (double)
#   Pay by (list)
#   Additional notes from provider (string)
#   More Info (link to PsychologyToday profile)
#   URL: https://www.psychologytoday.com/us/therapists/[state_or_zip]/[provider_id]?category=[category]


# Step 3: save this desired info into a nested dict for easy querying, save nested dict into json file