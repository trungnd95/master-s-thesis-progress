"""
This file is for data collection from list of best books ever on Goodreads.com
Original Author: Trung-Ng
Date: 30/10/2019
Fullstack Datascience Project Sample
"""

from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Referer': 'https://cssspritegenerator.com',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8'}

class DataCollection:
    base_url = 'https://www.goodreads.com'
    books_url = 'books.csv'
    books_detail = 'book_data.csv'

    def __init__(self):
        pass

    @staticmethod
    def collect_books_url(from_url='https://www.goodreads.com/list/show/1.Best_Books_Ever', num_pages=2):
        books_df = pd.DataFrame()
        for i in range(1, num_pages):
            time.sleep(5)
            print('Reading page {}'.format(i))
            page_url = from_url + '?page=' + str(i)
            page = requests.get(page_url, hdr)
            page_soup = BeautifulSoup(page.content, 'html.parser')
            list_books_table = page_soup.find('table', attrs={'class': 'tableList'})
            list_books_data = list_books_table.find_all('tr')
            for r in list_books_data:
                books_df = books_df.append({'URL': r.find('a', attrs={'class': 'bookTitle'}).attrs['href']}, ignore_index=True)
        books_df.to_csv(DataCollection.books_url)

    @staticmethod
    def collect_book_data():
        # Create book infos dataframe
        book_data = pd.DataFrame(columns=['image_url', 'title', 'description', 'authors', 'edition', 'format', 'isbn',
                                          'num_of_pages', 'rating', 'num_of_ratings', 'num_of_reviews', 'genres'])
        books_url = pd.read_csv(DataCollection.books_url)
        save_every = 10

        for i in range(len(book_data), len(books_url)):
            time.sleep(30)
            book_page = requests.get(DataCollection.base_url + books_url.loc[i, 'URL'], hdr, verify=False)
            print(book_page)
            book_soup = BeautifulSoup(book_page.content, 'html.parser')
            book_inst = dict()

            # - 1st column: Find image url
            image_tag = book_soup.find('img', attrs={'id': 'coverImage'})
            book_inst['image_url'] =  image_tag.attrs['src'] if image_tag else ''

            # - 2nd: Find book title
            book_title_tag = book_soup.find('h1', attrs={'id': 'bookTitle'})
            book_inst['title'] =  book_title_tag.text.replace('\n', '').strip() if book_title_tag else ''

            # - 3rd: Find book Description
            description_block = book_soup.find('div', attrs={'id': 'description'})
            book_inst['description'] =  description_block.find_all('span')[-1].text if description_block else ''

            # - 4th: Find book authors
            list_authors_tag = book_soup.find('div', attrs={'class': 'authorName__container'})
            book_inst['authors'] = '|'.join([a.find('span').text for a in list_authors_tag.find_all('a')]) if list_authors_tag else ''

            book_details_tag =  book_soup.find('div', attrs={'id': 'details'})
            # 5th: Find edition
            book_inst['edition'] =  book_details_tag.find('span', attrs={'itemprop', 'bookEdition'}) if book_details_tag else ''

            # 6th: Find book format
            book_inst['format'] = book_details_tag.find('span', attrs={'itemprop', 'bookFormat'}) if book_details_tag else ''

            # 7th: Find book pages
            book_inst['num_of_pages'] = book_details_tag.find('span', attrs={'itemprop', 'numOfPages'}) if book_details_tag else ''

            # 8th: Find book isbn
            book_data_box = book_details_tag.find('div', attrs={'id': 'bookDataBox'})
            book_inst['isbn'] = book_data_box.find_all('div', attrs={'class': 'clearFloats'})[1]\
                .find('div', attrs={'class': 'infoBoxRowTitle'}).text if book_data_box else ''

            book_meta_block = book_soup.find('div', attrs={'id': 'bookMeta'})
            # 9th: Find book rating
            book_inst['rating'] = book_meta_block.find('span', attrs={'itemprop': 'ratingValue'}).text\
                .replace('\n', '').strip() if book_meta_block else ''

            # 10th: Find number rating of book
            book_inst['num_of_ratings'] = book_meta_block.find('meta', attrs={'itemprop': 'ratingCount'})\
                .attrs['content'] if book_meta_block else ''

            # 11th: Find number reviews of book
            book_inst['num_of_reviews'] = book_meta_block.find('meta', attrs={'itemprop': 'reviewCount'})\
                .attrs['content']  if book_meta_block else ''

            # 12th: Find book genres
            list_book_genres_tag = book_soup.find('div', attrs={'class': 'bigBoxContent containerWithHeaderContent'})
            book_inst['genres'] = '|'.join([ge.find('a', attrs={'class': 'actionLinkLite bookPageGenreLink'}).text for ge in list_book_genres_tag.find_all('elementList')])

            book_data = book_data.append(book_inst, ignore_index=True)
            print(book_data)
            if i % save_every == 0:
                book_data.to_csv(DataCollection.books_detail)

if __name__ == "__main__":
    # 1. Collect books url
    # DataCollection.collect_books_url(num_pages=3)

    # 2. Collect book data
    DataCollection.collect_book_data()


