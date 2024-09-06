from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scholarly import scholarly
from scholarly import ProxyGenerator
from typing import Union
import json
import copy
import os

def get_application():
    _app = FastAPI(title="scholarly-api")
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in os.getenv("BACKEND_CORS_ORIGINS",[""])],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


def set_free_proxies():
    try:
        while True:
            pg = ProxyGenerator()
            proxy_is_set = pg.FreeProxies()
            if proxy_is_set:
                scholarly.use_proxy(pg)
                print("Free proxies are set!")
                return True
    except Exception as e:
        print("error while setting free proxies: ", e)
        return False


def set_scrapperapi_proxies(_api_key=False):
    try:
        pg = ProxyGenerator()
        scraper_api_key = os.getenv("SCRAPER_API_KEY")

        if (_api_key):
            scraper_api_key = _api_key

        proxy_is_set = pg.ScraperAPI(scraper_api_key)
        if proxy_is_set:
            scholarly.use_proxy(pg)
            print("ScrapperApi proxies are set!")
            return True
    except Exception as e:
        print("error while setting ScrapperApi proxies: ", e)
        return False


app = get_application()


# Define inital proxy type
# set_free_proxies()
set_scrapperapi_proxies()

@app.get("/")
def home():
    return {"message":"Scholarly-Api, check /docs endpoint!"}


@app.get("/status")
def check_status():
    return {"message":"OK"}

@app.post("/use-freeproxies")
async def use_free_proxies():
    success = set_free_proxies()
    if (success):
        return {"seccess": success, "message": "New proxies are set!"}
    else:
        raise HTTPException(
            status_code=500, detail='Server error while setting free proxies!')


@app.post("/use-scrapperapi")
async def use_scrapperapi_proxies(scrapper_api_key: str):
    success = set_scrapperapi_proxies(scrapper_api_key)
    if (success):
        return {"seccess": success, "message": "ScrapperApi proxies are set!"}
    else:
        raise HTTPException(
            status_code=500, detail='Server error while setting ScrapperApi proxies!')


@app.get("/citations")
def get_citations(doi: Union[str, None] = None, title: Union[str, None] = None):
    query = None
    if (doi):
        query = doi
    elif (title):
        query = title
    else:
        raise HTTPException(
            status_code=400, detail="Paper DOI or title is required!")

    try:
        print("checking paper with doi: ", query)
        search_query = scholarly.search_pubs(query)
        first_result = next(search_query)
        paper_info =  copy.deepcopy(first_result)
        print("paper search result retrived from Google")
        print(json.dumps(paper_info,sort_keys=True, indent=4))
        citations_data = scholarly.citedby(first_result)
        print("citations data retrived from Google")
        citations = []
        for citation in citations_data:
            citations.append(citation)
        return {"info": paper_info, "citations": citations}
    except Exception as e:
        print("Error occured while fetching from google scholar: ", e)
        raise HTTPException(
            status_code=408, detail="Request timed out while fetching information from google scholar")
