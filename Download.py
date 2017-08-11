from bs4 import BeautifulSoup
import urllib
import urllib.parse
import urllib.request
from config import bot, warning


def download_song(song):
    zaycev_search = "http://zaycev.net/search.html?"
    domen = "http://zaycev.net"
    query_search = song
    results = {}

    try:
        url = zaycev_search + urllib.parse.urlencode({'query_search': query_search})
        print(url)
        data = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(data, "lxml")
    except Exception:
        return None
    else:
        if soup.find("div", attrs={'class': 'search-page__no-results'}):
            return None
        else:
            find_data_url = soup.find("div", attrs={'class': 'musicset-track'})

            # find song author
            find_song_author = find_data_url.find("div", attrs={'class': 'musicset-track__artist'})

            # find song name
            find_song_name = find_data_url.find("div", attrs={'class': 'musicset-track__track-name'})

            song_author = find_song_author.find('a').text
            song_name = find_song_name.find('a').text

            print("SONG: {0} - {1}".format(song_author, song_name))

            # find tag <a> with href to detail page with download link
            find_url = find_data_url.find('a', attrs={'class': 'musicset-track__download-link'})

            # link to detail page with download link
            href = find_url['href']

            # creating BS for page with details
            details = urllib.request.urlopen(domen + href).read()
            details_soup = BeautifulSoup(details, "lxml")

            # get direct link to download
            download_href = details_soup.find("a", attrs={'id': 'audiotrack-download-link'})
            direct_dl_link = download_href['href']
            print(direct_dl_link)

            results[song_author + '-' + song_name] = direct_dl_link
            return results


def handle(user_id, song):
    song_list = download_song(song)
    if song_list is not None:

        song_names = list(song_list.keys())
        song_links = list(song_list.values())

        bot.send_message(user_id, "I found this song for you:\n\n%s\n\n%s" % (song_names[0], warning))
        bot.send_chat_action(user_id, 'upload_audio')
        bot.send_audio(user_id, song_links[0])

    else:
        bot.send_message(user_id, "There no results for: ' %s'." % song)