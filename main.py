import requests
from bs4 import BeautifulSoup
import pandas as pd
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
url = requests.get('https://m.imdb.com/chart/top/',headers=headers)
soup = BeautifulSoup(url.text , 'html.parser')

#getting each movie's page link
ul_element = soup.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 eBRbsI compact-list-view ipc-metadata-list--base')
movie_links = []
if ul_element:
    # Find all <a> elements containing movie links within the <ul>
    link_elements = ul_element.find_all('a', href=True,class_='ipc-title-link-wrapper')
    
    # Extract the URLs from the <a> elements
    for link_element in link_elements[:10]:
        movie_url = link_element['href']
        # Append the URL to the list of movie links
        movie_links.append("https://www.imdb.com" + movie_url)

print(movie_links)

movie_info = []
for movie_url in movie_links:
    response = requests.get(movie_url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('span', class_='hero__primary-text').text.strip()
    rating = soup.find('span', class_='sc-bde20123-1 cMEQkK').text.strip()
    year = soup.find('a', class_='ipc-link ipc-link--baseAlt ipc-link--inherit-color').text.strip()
    genre = soup.find('span',class_='ipc-chip__text').text.strip()
    director = soup.find('li',class_='ipc-inline-list__item').text.strip()
    # Store movie information in a dictionary
    movie_detail = {
        "Title": title,
        "Rating":rating,
        "Year":year,
        "Genre" : genre,
        "Director" : director,
    }
    
    movie_info.append(movie_detail)
# Print movie information
for movie in movie_info:
    print(movie)