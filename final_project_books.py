import requests
import time
from bs4 import BeautifulSoup as soup
import csv
import sys
import numpy as np

def make_url(sequence):
    return "https://www.goodreads.com/book/show/%s" % sequence


def get_book(sequence):
    url = make_url(sequence)
    r = requests.get(url)
    con = r.content
    page = soup(con, "html.parser")

    if page.find('h4'):  # h4 header means the book doesnt exist
        return None

    title = get_title(page)
    rating = get_rating(page)
    description = get_description(page)
    genres = get_genre(page)
    pages = get_pages(page)

    return [sequence, title, pages, rating, genres, description]


def get_title(page):
    title = page.find('h1', id='bookTitle').string
    title = title.replace('\n', '').lstrip().rstrip()
    return title


def get_rating(page):
    rating = page.find('span', itemprop='ratingValue').string
    rating = float(rating.replace('\n', '').lstrip().rstrip())
    return rating


def get_description(page):
    description = page.find('div', id='descriptionContainer').contents
    description = description[1].text.split('\n')
    short = description[1]
    description = description[2]
    return description if description else short


def get_genre(page):
    genres = []
    g = page.find_all('div', 'elementList')
    for each in g:
        c = each.contents[1].text
        c = c.replace('\n', '')
        c = c.split('>')
        c = c[0].lstrip().rstrip()
        genres.append(c)

    if '' in genres:
        genres.remove('')

    return list(dict.fromkeys(genres))


def get_pages(page):
    p = page.find('span', itemprop='numberOfPages').text
    p = p.split(' ')
    return int(p[0])


def enter_database(data):
    with open('books.csv', mode='a', newline='', errors='ignore') as file:
        writer = csv.writer(file, delimiter=',')
        if len(np.array(data, dtype='object').shape) == 1:
            writer.writerow(data)
        else:
            writer.writerows(data)


def run(more):
    """
        more is how many more books you want to add to the database.
        For example if there are books numbered 1-1000 in the database at the moment, and more=200,
        this function will add books 1001-1200 to the database.
    """
    with open('books.csv', mode='r', newline='', errors='ignore') as file:
        num = list(file)
        num = int(num[-1][0])

    start = num + 1
    end = start + more

    data = []

    for i in range(start, end):
        print(i)
        data.append(get_book(i))

    enter_database(data)

# print(get_book(10242))
# t = ["Index", "Title", "Pages", "Rating", "Genres", "Description"]

if __name__ == "__main__":
    r = sys.argv[1]
    print('Adding %s books to the database' % r)
    start_time = time.time()
    run(r)
    print('Finished adding books to the database')
    dif = time.time() - start_time
    print("-----Execution Time: %s seconds -----" % dif)