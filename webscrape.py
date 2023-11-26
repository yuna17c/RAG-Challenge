from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)

SENTENCE = 'quels sont les aliments populaires'

blocklist = [
  'style',
  'script',
  'footer',
  # other elements,
]


def parse_content(links: list) -> list:
    data = []
    counter = 0
    for link in links:
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('title').text
        text_elements = [t for t in soup.find_all(text=True) if (t.parent.name not in blocklist and len(t) > 10 and '\n' not in t)]
        text_elements = " ".join(text_elements)
        d = {}
        d["title"] = title
        d["snippet"] = text_elements
        data.append(d)
        if counter == 3: break
        counter += 1

    return data



def write_data_to_txt(d: dict) -> None:
    """
    generate a bunch of txt files in a folder containing all the text for each dictionary
    """
    pass


def search_content(input_str: str) -> list:
# Query to obtain links
    query = input_str
    links = [] # Initiate empty list to capture final results
    n_pages = 2
    for page in range(1, n_pages):
        url = "http://www.google.com/search?q=" + query + "&start=" +      str((page - 1) * 10)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # soup = BeautifulSoup(r.text, 'html.parser')

        search = soup.find_all('div', class_="yuRUbf")
        for h in search:
            links.append(h.a.get('href'))
    
    return links


def main():
    links = search_content(SENTENCE)
    RAG_DOCUMENT = {}
    print(links)
    data = parse_content(links)
    RAG_DOCUMENT["message"] = SENTENCE
    RAG_DOCUMENT["documents"] = data
    print(RAG_DOCUMENT)



if __name__ == main():
    main()