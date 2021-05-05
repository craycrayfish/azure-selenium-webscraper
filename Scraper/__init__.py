from shared_code import webflow
from shared_code import scrapers
from shared_code import keywords
from shared_code import helper_funcs
import re
import time
import json
import os
from datetime import datetime
import logging
import azure.functions as func
from selenium import webdriver
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.storage.blob import BlobServiceClient

def main(mytimer: func.TimerRequest) -> None:

    hour = datetime.now().strftime('%H')
    logging.info('Webflow scraper started @ hour {}.'.format(time))
    group = int(hour)%5

    company_id, location_id = webflow.find_id()
    location_list = list(location_id)
    current_jobs = webflow.get_current_jobs()
    excluded_companies = keywords.generate_excluded()

    companies = keywords.generate_links()
    companies = companies.split(',')
    company_links = {k: v for k, v in zip(companies[0::2], companies[1::2])}

    linked_in_companies = keywords.generate_linked_in()
    portal_xpaths = keywords.generate_company_xpaths()

    vacancies = {}

    # Scrape data
    for company, link in company_links.items():
        if company in excluded_companies:
            continue
        if company not in company_id:
            continue
        elif company in portal_xpaths:
            roles, urls, locations = scrapers.scrape_jobs(link, portal_xpaths[company])
        elif company in linked_in_companies:
            roles, urls, locations = scrapers.scrape_linked_in(linked_in_companies[company], company)
        else:
            continue
        vacancies[company] = {'roles': roles, 'urls': urls, 'locations': locations}
        time.sleep(3)

    for company, jobs in vacancies.items():
        count = 0
        # Delete jobs from this company
        if len(jobs['roles']) > 0 and company_id[company] in current_jobs:
            for job in current_jobs[company_id[company]]:
                r = webflow.delete_job(job)
        
        # Add jobs
        for role, url, location in zip(jobs['roles'], jobs['urls'], jobs['locations']):
            if role is None or url is None or location is None:
                continue
            isin_location = helper_funcs.find_location(location, location_list)
            if not isin_location:
                continue
            slug = re.sub('[\W_]+', '', ' '.join([company, role])).replace(' ', '-').lower()
            r = webflow.send_job(company_id[company], role, slug, location_id[isin_location], url)
            count += 1
        
        # Update data into webflow
        print(company_id[company], count)
        r = webflow.update_job_offers(company_id[company], count)

    return
