import os, sys 
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Set Development For Testing
dev = True

####
# URLs to process
# Each URL is structured as an array. The first element is the URL to process, the second is the method of search, 
# and the third is the number of total pages to load.
# The method of search can be "datatable" or "paged".
# If the method of search is "datatable", the script will search for a table with the class "datatable" and download the PDFs.
# If the method of search is "paged", the script will load the number of pages specified and download the PDFs.
# The script will download the PDFs to the DOWNLOAD_DIR directory.
####
urls = [
    ["https://www.archives.gov/research/jfk/release-2025", 'datatable'],
    ["https://www.archives.gov/research/jfk/release-2021","datatable"],
    ["https://www.archives.gov/research/jfk/release-2022" ,"paged", 265],
    ["https://www.archives.gov/research/jfk/release-2023", "paged", 53],
    ["https://www.archives.gov/research/jfk/release-2017-2018", "paged", 1092],
]

# Create a a log file to track the last ran url
last_url_file = "last_url.txt"
last_url = None
last_page = None

# If the log file exists, read the last ran URL, else create the file and write an empty string
if os.path.exists(last_url_file):
    with open(last_url_file, "r") as f:
        last_url = f.read().strip()
        if "page=" in last_url:
            last_page = int(last_url.split("page=")[-1])
else:
    with open(last_url_file, "w") as f:
        f.write("")

# If there is a last run, start from the last grabbed link.
if(last_url):
    print(f"Previous run detected. Starting at the last url: {last_url}")

    # Get the base URL so we can figure out which url in the urls array to start from
    base_url = last_url.split("?")[0]
    for i, url in enumerate(urls):
        if base_url in url[0]:
            urls = urls[i:]
            break
    
    print(f"Base URL: {base_url}")
    print(f"Last ran URL: {last_url}")
    print(f"Last ran Page: {last_page}")

#sys.exit()

# Directory to save downloaded PDFs
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

## Download the PDF file
def download_pdf(pdf_url, filename):

    # Development mode, do not download the file but print the URL
    if dev:
        print(f"Downloading: {pdf_url}")
        return;

    filepath = os.path.join(DOWNLOAD_DIR, filename)

    # If the filename exists, do not overwrite it, instead create a new filename with a random suffix
    if os.path.exists(filepath):
        base, ext = os.path.splitext(filename)
        filename = f"{base}_duplicate_{os.urandom(4).hex()}{ext}"
        filepath = os.path.join(DOWNLOAD_DIR, filename)

    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {pdf_url}: {e}")

## Process the url
def process_page(url):
    link = url[0]
    method = url[1]

    # Update the last ran URL
    last_url = link
    with open(last_url_file, "w") as f:
        f.write(last_url)

    if method == "datatable":
        process_datatable(link)

    elif method == "paged":
        pages = url[2]
        start_page = 1
        if(last_page):
            start_page = last_page
        for i in range(start_page, pages + 1):

            # If it is the first page, the URL is the same as the link, else it is the link with the page number
            if i == 1:
                page_url = link
            else:
                page_url = f"{link}?page={i}"
                process_paged(page_url)

# Function to process a page ith datatable structure
def process_datatable(url):
    try:
        print(f"\nProcessing Datatable: {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the datatable
        table = soup.find("table", class_="datatable")
        if not table:
            print("No datatable found.")
            return

        rows = table.find_all("tr")
        for row in rows[1:]:  # Skip header row
            cells = row.find_all("td")
            if len(cells) >= 2:
                link_tag = cells[0].find("a", href=True)
                if link_tag and ".pdf" in link_tag['href'].lower():
                    pdf_url = urljoin(url, link_tag['href'])
                    #release_date = cells[1].get_text(strip=True)

                    filename = os.path.basename(pdf_url)
                    # Optionally add date to filename: f"{release_date}_{filename}"
                    download_pdf(pdf_url, filename)
                    #print(f"Release Date: {release_date}")
    except Exception as e:
        print(f"Error processing {url}: {e}")

# Function to process a page with paged structure
def process_paged(url):
    try:
        print(f"\nProcessing Paged: {url}")
        with open(last_url_file, "w") as f:
            f.write(url)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all links with 'jfk/releases' in the URL
        links = soup.find_all("a", href=True)
        for link in links:
            href = link['href']
            if 'jfk/releases' in href and href.lower().endswith('.pdf'):
                pdf_url = urljoin(url, href)
                filename = os.path.basename(pdf_url)
                download_pdf(pdf_url, filename)
    except Exception as e:
        print(f"Error processing {url}: {e}")

# Run the script
for url in urls:
    process_page(url)

print("\nAll done.")
