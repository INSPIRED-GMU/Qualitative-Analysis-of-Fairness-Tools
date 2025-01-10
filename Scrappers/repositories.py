import requests
import csv

def search_github_repositories(keyword, max_results=10):
    base_url = "https://api.github.com/search/repositories"
    params = {
        'q': keyword,
        'per_page': max_results,
    }

    headers = {
        'Accept': 'application/vnd.github.v3+json',  # Use the v3 API
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Check for errors in the response

        data = response.json()
        repositories = data.get('items', [])

        # Specify the CSV file name
        csv_filename = f"repositories_output.csv"

        # Write the data to the CSV file
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Keyword', 'Repository Name', 'Owner', 'Description', 'URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Check if the file is empty, write header only if it's empty
            if csvfile.tell() == 0:
                writer.writeheader()

            # Write the data
            for repo in repositories:
                writer.writerow({
                    'Keyword': keyword,
                    'Repository Name': repo['name'],
                    'Owner': repo['owner']['login'],
                    'Description': repo['description'],
                    'URL': repo['html_url'],
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
                    search_github_repositories(keyword, max_results)

                print("Data written to repositories_output.csv")

    except FileNotFoundError:
        print(f"Input file not found: {input_file_path}")
    except ValueError:
        print("Please enter a valid number for the maximum results.")
    except Exception as e:
        print(f"An error occurred: {e}")
