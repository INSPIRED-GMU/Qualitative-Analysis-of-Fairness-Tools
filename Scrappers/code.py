import requests
import csv

def search_github_codes(keyword, max_results=15):
    access_token = ""

    # The keyword you want to search for
    search_keyword = "fairlearn"

    # URL for the GitHub API's code search endpoint
    url = f"https://api.github.com/search/code?q={search_keyword}"
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
        repositories = data.get('items', [])

        # Specify the CSV file name
        csv_filename = f"codes_output.csv"

        # Write the data to the CSV file
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Keyword','Code URL', 'Repository', 'File Path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header

            # Check if the file is empty, write header only if it's empty
            if csvfile.tell() == 0:
                writer.writeheader()

            # Write the data
            for item in data["items"]:
                writer.writerow({
                    'Keyword': keyword,
                    'Code URL': item['html_url'],
                    'Repository': item['repository']['full_name'],
                    'File Path': item['path'],
                })


    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    input_file_path = input("Enter the path to the input file containing keywords: ")

    try:
        with open(input_file_path, 'r') as input_file:
            keywords = input_file.read().splitlines()

            if not keywords:
                print("No keywords found in the input file.")
            else:
                max_results = int(input("Enter the maximum number of results to retrieve: "))

                for keyword in keywords:
                    search_github_codes(keyword, max_results)
                print("Data written to codes_output.csv")

    except FileNotFoundError:
        print(f"Input file not found: {input_file_path}")
    except ValueError:
        print("Please enter a valid number for the maximum results.")
    except Exception as e:
        print(f"An error occurred: {e}")
