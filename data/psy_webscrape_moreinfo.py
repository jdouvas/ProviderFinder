#-----------------------------------------------------------------------
# psy_webscrape_moreinfo.py
# Author: Julia Douvas
# Description: Webscrapes PsychologyToday psychiatrist profiles in the
#              Princeton, NJ area using the urls gathered from running 
#              psy_webscrape_basic.py and stored in psy_ids.json and
#              psy_ids.csv. Collects the following information for
#              each provider and stores values in psy_moreinfo.json:
#                   1. Provider name (string)
#                   2. URL (string)
#                   3. Titles (list of strings)
#                   4. Phone number (string)
#                   5. Street Address (string)
#                   6. Zipcode (integer)
#                   7. City (string)
#                   8. State (string)
#                   9. Accepted insurances (list of strings)
#                   10.Telehealth option (Y/N)
#                   11.Pay by options (list of strings)
#                   12.Specialties, Issues, Mental Health (list of strings)
#                   13.Types of therapies offered (list of strings)
# Results: creation of psy_moreinfo.json, psy_moreinfo.csv, 
#          psy_moreinfo_newer.csv, psy_moreinfo_newest.csv 
# Notes: psy_moreinfo_newest.csv is a final edited version of 
#        psy_moreinfo.csv that omits small mistakes and is in an
#        acceptable format for uploading to a table in a database in
#        PgAdmin 4
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

__urls = []

def scrape_me_more(url):   # input parameter = string url to pyschologytoday's website
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    
    providers_moreinfo = [] # generating empty dict
    url_num = 0

    while url_num < (len(__urls) - 1):
        time.sleep(1)           # added a 1 second sleep to limit bot detection
        try:
            driver.get(url)         # open the url in selenium
        except:
            print ('bad url!')
        soup = BeautifulSoup(driver.page_source, features="lxml") # grab the content with beautifulsoup for parsing

        provider_moreinfo = {}

        # provider name
        name = soup.find("h1", {"itemprop": "name"})
        if name is not None:
            name = name.text.strip()
            provider_moreinfo["name"] = name
        else: 
            provider_moreinfo["name"] = ''
        
        # url
        provider_moreinfo["url"] = url

        # title
        title_panel = soup.find("div", {"class": "profile-title"})
        if title_panel is not None:
            number_titles = len(title_panel.findAll("span", {"class": "nowrap"}))
            if number_titles > 0:
                titles = []
                j = 1
                while j < (2*number_titles):
                    result = title_panel.find("h2").contents[j].text.replace(",","").strip()
                    titles.append(result)
                    j += 2
                provider_moreinfo["titles"] = titles
            else:
                provider_moreinfo["titles"] = ''
        else: 
            provider_moreinfo["titles"] = ''
        
        # phone
        phone_panel = soup.find("div", {"class": "profile-phone"})
        if phone_panel is not None:
            phone_number = phone_panel.find("a", {"id": "phone-click-reveal"}).text.replace(",","").strip()
            provider_moreinfo["phone_number"] = phone_number
        else: 
            provider_moreinfo["phone_number"] = ''

        
        # location needed for searching
        total_address = soup.find("div", {"class": "location-address-phone"}).contents[1].contents[1].text.replace(",","").strip()
        if total_address is not None:
            provider_moreinfo["address"] = total_address
        else: 
            provider_moreinfo["address"] = ''
        zipcode = soup.find("span", {"itemprop": "postalcode"})
        if zipcode is not None:
            zipcode = zipcode.text.strip()
            provider_moreinfo["zipcode"] = zipcode
        else: 
            provider_moreinfo["zipcode"] = ''
        city = soup.find("span", {"itemprop": "addressLocality"})
        if city is not None:
            city = city.text.replace(",","").strip()
            provider_moreinfo["city"] = city
        else: 
            provider_moreinfo["city"] = ''
        state = soup.find("span", {"itemprop": "addressRegion"})
        if state is not None:
            state = state.text.strip()
            provider_moreinfo["state"] = state
        else:
            provider_moreinfo["state"] = ''
        
        # accepted insurance plans
        insurance_panel = soup.find("div", {"class": "spec-list attributes-insurance"})
        if insurance_panel is not None:
            accepted_insurances = insurance_panel.find("ul", {"class": "attribute-list copy-small"})
            if accepted_insurances is not None:
                number_of_accept_insur = len(accepted_insurances.findAll("li"))
                if number_of_accept_insur > 0:
                    insurances = []
                    j = 1
                    while j < (2*number_of_accept_insur):
                        result = insurance_panel.find("ul", {"class": "attribute-list copy-small"}).contents[j].text.replace(",","").strip()
                        insurances.append(result)
                        j += 2
                    provider_moreinfo["insurances"] = insurances
                else:
                    provider_moreinfo["insurances"] = ''
            else: 
                provider_moreinfo["insurances"] = ''
        else: 
            provider_moreinfo["insurances"] = ''


        # # cost_per_session
        # finances_office = soup.find("div", {"class":"finances-office"})
        # if finances_office is not None:
        #     finances = finances_office.find("ul")
        #     if finances is not None:
        #         cost_per_session = finances.find("li")
        #         if cost_per_session is not None:
        #             cost_per_session = cost_per_session.text.replace("Cost per Session: ","").replace("$","").strip()
        #             cost_per_session = cost_per_session.split(" - ")
        #             # if it says sliding scale 
        #             if (len(cost_per_session) > 1):
        #                 if (cost_per_session[0].isnumeric()) and (cost_per_session[1].isnumeric()) and (cost_per_session[0].isalpha() is False) and (cost_per_session[1].isalpha() is False):
        #                     low_cost = cost_per_session[0]
        #                     high_cost = cost_per_session[1]
        #                     provider_moreinfo["low_cost"] = low_cost
        #                     provider_moreinfo["high_cost"] = high_cost
        #             elif (cost_per_session[0].isnumeric()) and (cost_per_session[0].isalpha() is False):
        #                 low_cost = cost_per_session[0]
        #                 provider_moreinfo["low_cost"] = low_cost.replace("+", "")
        #                 provider_moreinfo["high_cost"] = str(float('inf'))
        #         else:
        #             provider_moreinfo["low_cost"] = ''
        #             provider_moreinfo["high_cost"] = ''
        #     else:
        #         provider_moreinfo["low_cost"] = ''
        #         provider_moreinfo["high_cost"] = ''
        # else: 
        #     provider_moreinfo["low_cost"] = ''
        #     provider_moreinfo["high_cost"] = ''
        
        # online therapy options
        telehealth = soup.find("div", {"class": "profile-phone-online-conult icon-online-therapy cursor-pointer"}) 
        if telehealth is not None:
            provider_moreinfo["telehealth_option"] = 'Y'
        else:
            provider_moreinfo["telehealth_option"] = 'N'

        # pay_by info
        pay_by_info = soup.find("div", {"class": "spec-subcat attributes-payment-method"})
        if pay_by_info is not None:
            number_payment_methods = len(pay_by_info.findAll("span", recursive=False)) - 1  # pay by: Amex, etc'
            if number_payment_methods > 0:
                pay_by = []
                for i in range(3, number_payment_methods + 3):
                    result = soup.find("div", {"class": "spec-subcat attributes-payment-method"}).contents[i].text
                    if (i != 3):
                        result = result.replace(",","").strip()
                    pay_by.append(result)
                provider_moreinfo["pay_by"] = pay_by
            else:
                provider_moreinfo["pay_by"] = ''
        else:
            provider_moreinfo["pay_by"] = ''

        # specialties and issues and mental health (list)
        specialties_group = soup.find("div", {"class": "specialties-section top-border"})
        specialties_issues = []
        if specialties_group is not None:
            specialties = specialties_group.find("ul", {"class": "attribute-list specialties-list"})
            if specialties is not None:
                number_specialties = len(specialties.findAll("li", {"class": "highlight"}, recursive=False))
                if number_specialties > 0:
                    k = 1
                    while k < (2*number_specialties):
                        result = specialties_group.find("ul", {"class": "attribute-list specialties-list"}).contents[k].text.strip()
                        specialties_issues.append(result)
                        k += 2

        issues_group = soup.find("div", {"class": "spec-list attributes-issues"})
        if issues_group is not None:
            issues = issues_group.find("ul", {"class": "attribute-list copy-small"})
            if issues is not None:
                number_issues = len(issues.findAll("li", {"class": ""}, recursive=False))
                if number_issues > 0:
                    k = 1
                    while k < (2*number_issues):
                        result = issues_group.find("ul", {"class": "attribute-list copy-small"}).contents[k].text.strip()
                        specialties_issues.append(result)
                        k += 2
        
        mental_health_group = soup.find("div", {"class": "spec-list attributes-mental-health"})
        if mental_health_group is not None:
            mental_health = mental_health_group.find("ul", {"class": "attribute-list copy-small"})
            if mental_health is not None:
                number_mental_health = len(mental_health.findAll("li", {"class": ""}, recursive=False))
                if number_mental_health > 0:
                    k = 1
                    while k < (2*number_mental_health):
                        result = mental_health_group.find("ul", {"class": "attribute-list copy-small"}).contents[k].text.strip()
                        specialties_issues.append(result)
                        k += 2
        
        if len(specialties_issues) > 0:
            provider_moreinfo["specialties_issues"] = specialties_issues
        else:
            provider_moreinfo["specialties_issues"] = ''


        # sexuality (list)
        sexuality_group = soup.find("div", {"class": "spec-list attributes-sexuality"})
        if sexuality_group is not None:
            sexuality = sexuality_group.find("ul", {"class": "attribute-list copy-small"})
            if sexuality is not None:
                number_sexuality = len(sexuality.findAll("li", {"class": ""}, recursive=False))
                if number_sexuality > 0:
                    sexuality = []
                    k = 1
                    while k < (2*number_sexuality):
                        result = sexuality_group.find("ul", {"class": "attribute-list copy-small"}).contents[k].text.strip()
                        sexuality.append(result)
                        k += 2
                    provider_moreinfo["sexuality"] = sexuality
                else:
                    provider_moreinfo["sexuality"] = ''
            else:
                provider_moreinfo["sexuality"] = ''
        else:
            provider_moreinfo["sexuality"] = ''


        # types of therapy (list)
        therapy_types_group = soup.find("div", {"class": "spec-list attributes-treatment-orientation"})
        if therapy_types_group is not None:
            therapy_types = therapy_types_group.find("ul", {"class": "attribute-list copy-small"})
            if therapy_types is not None:
                number_therapy = len(therapy_types.findAll("li", {"class": ""}, recursive=False))
                if number_therapy > 0:
                    therapies_offered = []
                    k = 1
                    while k < (2*number_therapy):
                        result = therapy_types_group.find("ul", {"class": "attribute-list copy-small"}).contents[k].text.strip()
                        therapies_offered.append(result)
                        k += 2
                    provider_moreinfo["therapies_offered"] = therapies_offered
                else:
                    provider_moreinfo["therapies_offered"] = ''
            else: 
                provider_moreinfo["therapies_offered"] = ''
        else:
            provider_moreinfo["therapies_offered"] = ''

        providers_moreinfo.append(provider_moreinfo)
        url_num += 1
        url = __urls[url_num]
    
    return providers_moreinfo # returns scrapped data as dict of dictionaries

def main():
    # need to get url from first thing in ids.json (and ids.csv by extension)
    with open('psy_ids.json', 'r') as json_file:
	    json_data = json.load(json_file)

    for item in json_data:
        __urls.append(item['url'])

    first_url = __urls[0]
    njdocs = scrape_me_more(first_url)
    
    # save data from webscrap to json file
    with open('psy_moreinfo.json', 'w') as fp:
        json.dump(njdocs, fp)
    
    # save data from webscrap to csv file
    with open('psy_moreinfo.json') as json_file:
        jsondata = json.load(json_file)

    data_file = open('psy_moreinfo.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)
    count = 0
    for data in jsondata:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    data_file.close()

    # fix file
    text = open("psy_moreinfo.csv", "r")
    text = ''.join([i for i in text]).replace("[", "{").replace("]", "}").replace("\"\"", "\'")
    x = open("psy_moreinfo_newer.csv","w")
    x.writelines(text)
    x.close()

    # fix file
    text = open("psy_moreinfo_newer.csv", "r")
    text = ''.join([i for i in text]).replace("inf", "-1")
    x = open("psy_moreinfo_newest.csv","w")
    x.writelines(text)
    x.close()


if __name__ == '__main__':
    main()