import requests

import requests


def search_github_code(keyword, max_results=10):
    # setup owner name , access_token, and headers
    access_token = ""

    # The keyword you want to search for
    search_keyword = "fairlearn"

    # URL for the GitHub API's code search endpoint
    url = f"https://api.github.com/search/discussions?q={search_keyword}"
    params = {
        'q': keyword,
        'per_page': max_results,
    }
    headers = {
        "Authorization": f"token {access_token}",
        "User-Agent": "YourAppName",
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Check for errors in the response

        data = response.json()
        code_results = data.get('items', [])

        for code in code_results:
            print(f"File: {code['name']}")
            print(f"Repository: {code['repository']['full_name']}")
            print(f"URL: {code['html_url']}")
            print()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    keyword = input("Enter a keyword to search GitHub code: ")
    max_results = int(input("Enter the maximum number of results to retrieve: "))

    search_github_code(keyword, max_results)
