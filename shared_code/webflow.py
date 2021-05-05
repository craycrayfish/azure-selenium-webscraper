import requests
import json
import time

KEY = 'WEBFLOW API KEY'
headers = {'Authorization': 'Bearer {}'.format(KEY),
            'accept-version': '1.0.0',
            'Content-Type': 'application/json'}
JOB_COLLECTION = 'JOB COLLECTIONS ID'
COMPANY_COLLECTION = 'COMPANY COLLECTIONS ID'

def find_id():
    """Get company and location IDs. Returns 2 dicts: {company name: company id}
    """
    r = requests.get('https://api.webflow.com/collections/{}/items/'.format(COMPANY_COLLECTION), headers=headers)
    r.content
    company_id = {}
    for item in r.json()['items']:
        company_id[item['name']] = item['_id']

    location_id = {}
    r = requests.get('https://api.webflow.com/collections/{}'.format(JOB_COLLECTION), headers=headers)
    for item in r.json()['fields']:
        if item['name'] == 'Location':
            for location in item['validations']['options']:
                location_id[location['name']] = location['id']
    return company_id, location_id

def get_current_jobs():
    """Gets all current jobs in a collection. Returns dict of dicts: {company id: {job id: job name}}
    """
    current_jobs = {}
    r = requests.get('https://api.webflow.com/collections/{}/items'.format(JOB_COLLECTION), headers=headers).json()
    total = r['total']
    for i in range(int(total / 100 + 1)):
        params = {'offset': i * 100}
        r = requests.get('https://api.webflow.com/collections/{}/items'.format(JOB_COLLECTION), headers=headers, params=params).json()
        time.sleep(1)
        if len(r) == 0:
            continue
        for item in r['items']:
            company = item['company']
            _id = item['_id']
            if company not in current_jobs:
                current_jobs[company] = {}
            current_jobs[company][_id] = item['name']
    return current_jobs

def send_job(company_id, role, slug, location_id, link):
    url = 'https://api.webflow.com/collections/{}/items'.format(JOB_COLLECTION)
    payload = {'collection_id': JOB_COLLECTION,
                'fields': {
                     'name': role,
                     'slug': slug,
                     'company': company_id,
                     'location-3': location_id,
                     'job-detail-url': link,
                    '_archived': False,
                    '_draft': False
                        },
               'live': True
                    }
    
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    time.sleep(1)
    return r.json()

def delete_job(job_id):
    """Deletes job with given job id
    """
    r = requests.delete('https://api.webflow.com/collections/{}/items/{}'.format(JOB_COLLECTION, job_id),
                    headers=headers)
    time.sleep(1)
    return r.json()

