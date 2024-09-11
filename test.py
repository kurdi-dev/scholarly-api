from app.lib.scholarly import scholarly
from app.lib.scholarly import ProxyGenerator
from typing import Union
import json
import copy
import os



def set_free_proxies():
    try:
        while True:
            pg = ProxyGenerator()
            proxy_is_set = pg.FreeProxies()
            if proxy_is_set:
                scholarly.use_proxy(pg, pg)
                print("Free proxies are set!")
                return True
    except Exception as e:
        print("error while setting free proxies: ", e)
        return False
def set_scrapperapi_proxies(_api_key=False):
    try:
        pg = ProxyGenerator()
        scraper_api_key = os.environ.get("SCRAPER_API_KEY")

        if (_api_key):
            scraper_api_key = _api_key

        proxy_is_set = pg.ScraperAPI(scraper_api_key)
        if proxy_is_set:
            scholarly.use_proxy(pg, pg)
            print("ScrapperApi proxies are set!")
            return True
    except Exception as e:
        print("error while setting ScrapperApi proxies: ", e)
        return False


def get_citations(doi: Union[str, None] = None, title: Union[str, None] = None):
    query = None
    if (doi):
        query = doi
        print("checking paper with doi: ", query)
    elif (title):
        query = title
        print("checking paper with title: ", query)
    else:
        raise ValueError("Paper DOI or title is required!")

    print("geting paper information from Google Scholar")
    first_result = scholarly.search_single_pub(query)
    paper_info =  copy.deepcopy(first_result)
    print("paper search result retrived from Google Scholar")
    print(json.dumps(paper_info,sort_keys=True, indent=4))
    print("geting citation data from Google Scholar")
    citations_data = scholarly.citedby(first_result)
    print("citations data retrived from Google Scholar")
    scholarly.pprint(citations_data)
    citations = []
    for citation in citations_data:
        citations.append(citation)
    return {"info": paper_info, "citations": citations}




# Define inital proxy type
set_free_proxies()
# set_scrapperapi_proxies(_api_key="3180e731a19b08005a31d328ee84e805")

results = get_citations(doi="10.1016/j.measurement.2020.108819")

print(results)