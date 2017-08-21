from bs4 import BeautifulSoup
import urllib
import urllib.parse
import urllib.request
from config import bot, warning, domen, search_link
from random import randint


def find_song(song, user_id):

    query_search = song
    results = {}

    try:
        url = search_link + urllib.parse.urlencode({'query_search': query_search})
        print(url)
        data = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(data, "lxml")
    except Exception:
        return None
    else:
        if soup.find("div", attrs={'class': 'search-page__no-results'}):
            bot.send_message(user_id, "There no results for: ' %s'." % song)
            return None
        else:
            # find all songs on result page
            find_data_url = soup.find_all("div", attrs={'class': 'musicset-track'})

            # if we find more than one song
            if len(find_data_url) > 1:
                try:
                    for data in find_data_url:
                        # find song author
                        find_song_author = data.find("div", attrs={'class': 'musicset-track__artist'})

                        # find song name
                        find_song_name = data.find("div", attrs={'class': 'musicset-track__track-name'})

                        song_author = find_song_author.find('a').text
                        song_name = find_song_name.find('a').text

                        print("SONG: {0} - {1}".format(song_author, song_name))

                        # find tag <a> with href to detail page with download link
                        find_url = data.find('a', attrs={'class': 'musicset-track__download-link'})

                        # link to detail page with download link
                        href = find_url['href']

                        # ---------------------------------------------

                        try:
                            # open detail page to get song link
                            details = urllib.request.urlopen(domen + href).read()
                            details_soup = BeautifulSoup(details, "lxml")

                            # get song link
                            download_href = details_soup.find("a", attrs={'id': 'audiotrack-download-link'})
                            direct_dl_link = download_href['href']
                            print(direct_dl_link)

                            results[song_author + '-' + song_name] = direct_dl_link

                        except TypeError:
                            continue

                        # get only first 5 songs
                        if len(results) >= 5:
                            break
                except AttributeError:
                    pass

                # return song to user

                song_names = list(results.keys())
                song_links = list(results.values())
                # get random song from song list
                num = randint(0, len(song_names)-1)

                # send song to user
                bot.send_message(user_id,"I found this song for you:\n\n%s\n\n%s" % (song_names[num], warning))
                bot.send_chat_action(user_id, 'upload_audio')
                bot.send_audio(user_id, song_links[num])

            # if only one song is existed
            else:
                # find song author
                find_song_author = soup.find("div", attrs={'class': 'musicset-track__artist'})

                # find song name
                find_song_name = soup.find("div", attrs={'class': 'musicset-track__track-name'})

                song_author = find_song_author.find('a').text
                song_name = find_song_name.find('a').text

                print("SONG: {0} - {1}".format(song_author, song_name))

                # find tag <a> with href to detail page with download link
                find_url = soup.find('a', attrs={'class': 'musicset-track__download-link'})

                # link to detail page with download link
                href = find_url['href']

                # ---------------------------------------------

                try:
                    # open detail page to get song link
                    details = urllib.request.urlopen(domen + href).read()
                    details_soup = BeautifulSoup(details, "lxml")

                    # get song link
                    download_href = details_soup.find("a", attrs={'id': 'audiotrack-download-link'})
                    direct_dl_link = download_href['href']
                    print(direct_dl_link)
                    results[song_author + '-' + song_name] = direct_dl_link
                except TypeError:
                    pass

                # return song to user

                song_names = list(results.keys())
                song_links = list(results.values())

                # send song to user
                bot.send_message(user_id, "I found this song for you:\n\n%s\n\n%s" % (song_names[0], warning))
                bot.send_chat_action(user_id, 'upload_audio')
                bot.send_audio(user_id, song_links[0])




