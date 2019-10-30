"""
This file is for data collection from list of best books ever on Goodreads.com
Original Author: Trung-Ng
Date: 30/10/2019
Fullstack Datascience Project Sample
"""

from bs4 import BeautifulSoup
import pandas as pd
import time
from requests import get

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Referer': 'https://cssspritegenerator.com',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8'}

class DataCollection:
    base_url = 'https://www.goodreads.com'
    books_data = 'books.csv'

    def __init__(self):
        pass

    @staticmethod
    def collect_books_url(from_url='https://www.goodreads.com/list/show/1.Best_Books_Ever', num_pages=2):
        books_df = pd.DataFrame()
        for i in range(1, num_pages):
            time.sleep(5)
            print('Reading page {}'.format(i))
            page_url = from_url + '?page=' + str(i)
            page = get(page_url, hdr)
            page_soup = BeautifulSoup(page.content, 'html.parser')
            list_books_table = page_soup.find('table', attrs={'class': 'tableList'})
            list_books_data = list_books_table.find_all('tr')
            for r in list_books_data:
                books_df = books_df.append({'URL': r.find('a', attrs={'class': 'bookTitle'}).attrs['href']}, ignore_index=True)
        books_df.to_csv(DataCollection.books_data)

if __name__ == "__main__":
    # 1. Collect books url
    DataCollection.collect_books_url(num_pages=3)





