from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import time
import random

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36', 'Referer': 'http://google.com'}

print("Link format: https://www.azlyrics.com/d/drake.html")
artist_url = input("Please enter artist link: ")
out_filename = input("Please enter file name: ")

artist_response = get(artist_url, headers = header)
artist_soup = BeautifulSoup(artist_response.text, 'html.parser')

a_links = []
a_title = []
for div in artist_soup.select('#listAlbum a'):
    a_links.append('https://www.azlyrics.com' + div['href'][2-len(div['href']):])
    a_title.append(div.text)

song_response = []
for url in range(len(a_links)-2):
    song_response.append(get(a_links[url], headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36', 'Referer': 'http://google.com'}))
    time.sleep(random.randrange(175,1000)/100)
    if url%5 == 0:
        print(str(url) + ' out of ' + str(len(a_links)-2))
        if url%100 ==0:
            print("Breaking...")
            time.sleep(random.randrange(300,600))
            print("Restarting...")

song_soup = []
for resp in song_response:
    song_soup.append(BeautifulSoup(resp.text, 'html.parser'))

lyrics = []
for song in song_soup:
    for div in song.find_all('div', class_ = ''):
        lyrics.append(div.text)

to_df = list(zip(a_title[0:len(lyrics)],lyrics))
data = pd.DataFrame(to_df, columns=['Song Name','Lyrics'])

data.to_csv(str(out_filename) + '.csv')
