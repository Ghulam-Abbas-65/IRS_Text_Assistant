
import requests
from bs4 import BeautifulSoup
import json
import time
import os


def fetch_publication_links(base_url):
    """Fetch IRS publication links from the main page."""
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    publication_table = soup.find('table')

    if not publication_table:
        print("No publication table found.")
        return []

    rows = publication_table.find_all('tr')[1:]
    publication_links = []

    for row in rows:
        columns = row.find_all('td')

        if len(columns) > 1:
            html_link_tag = columns[1].find('a', href=True)

            if html_link_tag:
                html_url = html_link_tag['href']

                if html_url.startswith("http"):
                    full_html_url = html_url
                else:
                    full_html_url = f'https://www.irs.gov{html_url}'

                publication_links.append(full_html_url)

    return publication_links

def fetch_clean_text(url):
    """Fetch and clean text content from a URL."""
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: Status Code {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.extract()

        text = soup.get_text(separator="\n", strip=True)
        text_lines = [line.strip() for line in text.split("\n") if line.strip()]
        clean_text = "\n".join(text_lines)

        return clean_text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def load_existing_data(filename):
    """Load existing data from JSON file."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_to_json(data, filename):
    """Save data to JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def scrape_irs_data():
    """
    Main function to scrape IRS publications and update JSON if changes are found.
    Returns the updated data dictionary.
    """
    base_url = "https://www.irs.gov/publications"
    json_filename = "irs_real_time.json"

    print("🔹 Fetching latest IRS publication links...")
    publication_links = fetch_publication_links(base_url)

    existing_data = load_existing_data(json_filename)
    updated_data = {}

    for html_link in publication_links:
        print(f"🔹 Checking: {html_link}")
        
        new_text = fetch_clean_text(html_link)

        if new_text:
            if html_link not in existing_data or existing_data[html_link] != new_text:
                print(f"🔹 Update found in: {html_link}")
                updated_data[html_link] = new_text

        time.sleep(1)  

    if updated_data:
        existing_data.update(updated_data)
        save_to_json(existing_data, json_filename)
        print(f"✅ Changes detected! Updated JSON saved as '{json_filename}'")
        return existing_data 
    else:
        print("✅ No changes found. Data is already up-to-date.")
        return existing_data  

if __name__ == "__main__":
    while True:
        print("\n🚀 Running IRS Scraper... Fetching new updates...\n")
        scrape_irs_data()
        print("\n⏳ Sleeping for 24 hours before next run...\n")
        time.sleep(86400)


