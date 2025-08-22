
import sys
from default_api import google_web_search, web_fetch

def perform_search(keyword, max_results=3):
    search_results = google_web_search(query=f'"{keyword}" ')
    if not search_results or not search_results.get('results'):
        print("Error: No web search results.")
        return

    urls_to_fetch = [result['link'] for result in search_results['results'][:max_results]]
    
    for url in urls_to_fetch:
        try:
            fetched_data = web_fetch(prompt=url)
            if fetched_data and fetched_data.get('content'):
                print(f'--- [Source: {url}] ---')
                print(fetched_data['content'])
                print('\n\n')
        except Exception as e:
            print(f"Error processing {url}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        perform_search(sys.argv[1])

