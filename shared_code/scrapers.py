from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import re
import os
import csv
import time
import requests

def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver

def wait_till_load(xpath, driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
    except:
        pass
    return driver

def clean_location(string):
    bad_words = ['Location: ']
    for word in bad_words:
        string = string.replace(word, '')
    return string

def scrape_jobs(url, xpaths):
    vacancies = {}
    driver = get_driver()
    driver.get(url)
    driver = wait_till_load(xpaths[0], driver)
    time.sleep(4)
    jobs = driver.find_elements_by_xpath(xpaths[0])
    location = None
    for job in jobs:
        if xpaths[1] == '':
            role = job.text
        else:
            try: 
                role = job.find_element_by_xpath(xpaths[1]).text
            except:
                continue
                
        if role == '':
            continue
        
        if xpaths[2] == '':
            url = job.get_attribute('href')
        else:
            try:
                url = job.find_element_by_xpath(xpaths[2]).get_attribute('href')
            except:
                continue
        
        if xpaths[3] != '':
            try:
                location = job.find_element_by_xpath(xpaths[3]).text
            except:
                pass
        
        vacancies[role] = {'url': url, 'location': location}
        
    if location == None and len(xpaths) > 5:
        for job in list(vacancies):
            if xpaths[5] == '':
                vacancies[job]['location'] = None
                continue
            try:
                driver.get(vacancies[job]['url'])
                driver = wait_till_load(xpaths[5], driver)
                time.sleep(4)
                location = driver.find_element_by_xpath(xpaths[5])
                location_text = clean_location(location.text)
                vacancies[job].update({'location': location_text})
            except:
                vacancies[job]['location'] = None
    
    roles = []
    urls = []
    locations = []
    for job in vacancies:
        roles.append(job)
        urls.append(vacancies[job]['url'])
        locations.append(vacancies[job]['location'])
    driver.quit()
    return roles, urls, locations

def scrape_linked_in(url, company):
    roles = []
    urls = []
    locations = []
    vacancies = {}
    driver = get_driver()
    driver.get(url)
    xpath = '//main//ul[1]//li'
    #button_xpath = '//button[contains(text(), "{}")]'.format('Show more')
    description_xpath = '//section[@class="description"]'
    url_xpath = './/a'
    driver = wait_till_load(xpath, driver)
    jobs = driver.find_elements_by_xpath(xpath)

    for job in jobs:    
        metadata = job.text.split('\n')
        if len(metadata) == 0:
            continue
        if company.lower() not in metadata[1].lower():
            continue
        role = metadata[0]
        location = metadata[2]
        date = metadata[3].split('Apply Now')[0]
        url = job.find_element_by_xpath(url_xpath).get_attribute('href')

        roles.append(role)
        urls.append(url)
        locations.append(location)
    
    driver.quit()
    return roles, urls, locations