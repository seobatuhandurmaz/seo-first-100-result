import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st

def search(query, api_key, cse_id, start_index, **kwargs):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
        'start': start_index,
        'num': 10,  # Request 10 results per batch
    }
    params.update(kwargs)
    response = requests.get(url, params=params)
    return response.json()

# Get user inputs for 'site', 'api_key', and 'cse_id'
api_key = input("Enter your Google API key: ")
cse_id = input("Enter your Custom Search Engine ID: ")
query = input("Enter your search query: ")

# Initialize lists to store results
urls = []
titles = []
meta_descriptions = []
h1_tags = []

# Perform the custom search in batches of 10 results
for start_index in range(1, 101, 10):
    results = search(query, api_key, cse_id, start_index)
    search_items = results.get('items', [])
    for item in search_items:
        urls.append(item['link'])

# Extract titles, meta descriptions, and h1 tags from HTML content
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the title from the HTML
    title_tag = soup.find('title')
    title = title_tag.text.strip() if title_tag else ''
    titles.append(title)

    # Get the meta description from the HTML
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    meta_description = meta_tag['content'].strip() if meta_tag and 'content' in meta_tag.attrs else ''
    meta_descriptions.append(meta_description)

    # Get the h1 tag from the HTML
    h1_tag = soup.find('h1')
    h1_content = h1_tag.text.strip() if h1_tag else ''
    h1_tags.append(h1_content)

# Create a DataFrame with the extracted data
data = {
    'URL': urls,
    'Title': titles,
    'Meta Description': meta_descriptions,
    'H1 Tag': h1_tags
}
df = pd.DataFrame(data)

# Write the DataFrame to an Excel file
df.to_excel('output.xlsx', index=False)

try:
    # Attempt to download the file in Colab
    from google.colab import files
    files.download('output.xlsx')
except ImportError:
    # If not in Colab, inform the user to manually download the file
    print("Search results saved to 'output.xlsx' file. Please download the file manually.")
