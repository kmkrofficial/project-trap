import requests
import json


def get_search_result(search):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    response = requests.get(f"https://query2.finance.yahoo.com/v1/finance/search?q={search}&lang=en-US&region=US&quotesCount=6&newsCount=3&listsCount=2&enableFuzzyQuery=false&quotesQueryId=tss_match_phrase_query&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_cie_vespa&enableCb=true&enableNavLinks=true&enableEnhancedTrivialQuery=true&enableResearchReports=true&enableCulturalAssets=true&enableLogoUrl=true&recommendCount=3", headers=headers)
    if response.status_code != 200:
        print("SearchAPI : Failed")
        return None
    content = json.loads(response.content)
    if (content["count"] > 0):
        return content["quotes"]

print(len(get_search_result("Amazon")))