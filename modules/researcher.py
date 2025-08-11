import requests

class Researcher:
    def __init__(self, api_key: str, cse_id: str):
        """
        Initialize the Researcher with Google Custom Search API credentials.
        :param api_key: Google API key.
        :param cse_id: Custom Search Engine ID.
        """
        self.api_key = api_key
        self.cse_id = cse_id

    def search(self, query: str, num_results: int = 10):
        """
        Search Google using the Custom Search JSON API.
        :param query: Search query string.
        :param num_results: Number of results to fetch (max 10 per API call).
        :return: List of search result dicts.
        """
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.cse_id,
            "q": query,
            "num": min(num_results, 10)  # API limit per request
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()

        items = []
        if "items" in results:
            for item in results["items"]:
                items.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet")
                })
        return items
