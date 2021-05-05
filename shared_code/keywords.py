def generate_excluded():
    excluded = ['AmpiFire']
    return excluded


def generate_linked_in():
    linked_in_keywords = {'Microsoft': 'microsoft'
                                }

    locations = {'worldwide': 'Worldwide'}

    query = 'https://www.linkedin.com/jobs/search?keywords={}&location={}'

    linked_in_companies = {k: query.format(v, locations['worldwide']) for k, v in linked_in_keywords.items()}
    return linked_in_companies

def generate_company_xpaths():
    portal_xpaths = {'Kyra Media': ['//div[@id="resultDiv"]/div/ul/li', './/a', 
                        './/a', './/div[@itemprop="name"]']
         }   
    return portal_xpaths

def generate_links():
        return "Kyra Media,https://kyra.bamboohr.com/jobs/"