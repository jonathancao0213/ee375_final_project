import requests
from bs4 import BeautifulSoup as soup
import csv
import random

sequence = random.randrange(0, 10000000)
# sequence = 7603
# sequence = 1454160
# sequence = 1431045
# sequence = str(sequence)
#
# while len(sequence) < 7:
#     sequence = '0' + sequence


def make_url(sequence):
    return "https://www.imdb.com/title/tt%s/?ref_=fn_al_tt_1" % sequence


def get_movie(sequence):
    url = make_url(sequence)

    r = requests.get(url)
    con = r.content
    page = soup(con, "html.parser")
    a = page.find('h1')
    b = page.find('strong')
    e = page.find('div', id='error')
    s = page.find('div', 'inline canwrap')
    g = page.find('div', 'subtext')

    if e != None:
        return None

    try: # Get title
        title = a.contents[0]
    except:
        # print("Cannot find title")
        title = None

    try: # Get rating */10
        rating = b.contents[0].text
    except:
        # print("Cannot find rating")
        rating = None

    try: # Get plot summary
        plot = s.contents[1].text.lstrip()
        plot = plot.split('\n')[0]
    except:
        # print("Cannot find plot")
        plot = None

    try: # Get genres
        genres = []
        for each in g.contents:
            if 'genres' in str(each):
                genres.append(each.text)
    except:
        # print("Cannot find genres")
        genres = None

    try:
        r = g.contents[0].lstrip().rstrip()
        if len(r) != 0:
            tv_rating = r
        else:
            tv_rating = "Not Rated"
    except:
        tv_rating = "Not Rated"


    return [title, rating, tv_rating, plot, genres]


def enter_database(lst):
    if lst == None:
        return
    with open('imdb.csv', mode='a', newline='', errors='ignore') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(lst)

if __name__ == "__main__":
    for sequence in range(1000):
        sequence = str(sequence)

        while len(sequence) < 7:
            sequence = '0' + sequence

        l = get_movie(sequence)

        enter_database(l)