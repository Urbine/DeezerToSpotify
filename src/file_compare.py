# In this file I am comparing both file to see the updates in a specific list.
# In this case, I want to see how much the deezer playlist has changed and apply those changes to Spotify.

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re

# Just in case.
# import ssl
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE

scope = 'user-library-read user-library-modify playlist-modify playlist-read-private playlist-modify-private'
cli_id = input("Please enter your Spotify Client ID: ")
cli_secret = input("Please enter your Spotify Client Secret:  ")
# redir_uri = input("Please enter your redirect URI: ")

# Common redirect URI: http://localhost:8888/callback/ <whitelisted in Spotify>

uri = "http://localhost:8888/callback/"  # Whitelist this URI within the application page.

spot_client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cli_id,
                                                        client_secret=cli_secret,
                                                        redirect_uri=uri,
                                                        scope=scope))

# auth_man = SpotifyClientCredentials(client_id=cl_id, client_secret=secret)
# spot_client = spotipy.Spotify(client_credentials_manager=auth_man)

# TODO: Add an option for the user to enter the file name.
# TODO: Add a boolean based list to display the migration results to the user.
# TODO: Try with list of tuples once again.


def get_from_file(file_name):
    results = {}
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for ln in file.readlines():
                st = ln.split("|")
                theme, art, *others = st
                # key = st[1].strip()
                # val = st[0].strip()
                if results.get(art) is not None:
                    continue
                else:
                    results[theme.strip()] = art.strip()
                if others:
                    results['misc'] = others
        return results
    except ValueError:
        print("This item could not be processed" + str(st))
        pass


# TODO: Find a way to match the content of a key, not part of it.
def find_updates(data_one, data_two):
    try:
        updates = {}
        for key in data_one.keys():
            if data_two.get(key) is not None:
                continue
            else:
                updates[key] = data_one[key]
        return updates
    except AttributeError:
        pass


def track_search_spotify(track_name, limit, offset):
    """
        This function will use the Spotipy module to search songs in Spotify.
        :param track_name: String
        :param limit: Integer
        :param offset: Integer
        :return: Loaded JSON file / Dictionary
    """
    result = spot_client.search(track_name, limit=limit, offset=offset, type='track',
                                market=None)
    return result


file_deezer = "../tracks-playlist-Bill Evans Solo Piano-Spotify.txt"
file_spotify = "../tracks-playlist-Music for supermarkets-Spotify.txt"

tracks_deezer = get_from_file(file_deezer)
tracks_spotify = get_from_file(file_spotify)

track_updates = find_updates(tracks_deezer, tracks_spotify)

print("We've found these tracks below are not in Spotify yet! \n")
update_counter = 1

for key, val in track_updates.items():
    print(f'{update_counter}. {key} | {val}')
    update_counter += 1

print("\n")
print("In total, we found {} tracks".format(update_counter - 1))

print("\n")

print("If you choose to add all tracks, we'll add the first result in every occurrence of the track.")
user_choice = input("Would you like to add all the tracks to Spotify? (yes / no) \n")

# Spotify API encodes queries by adding "%20", "%28", "%29" or "+"
# if there's a whitespace, and adds it to the URL.
# The module handles this. I am just adding the track without any formatting.

if user_choice == 'yes':
    print("Here's a list of your playlists:\n")
    # Limited to 50 playlists.
    playlists = spot_client.current_user_playlists(limit=50, offset=0)

    counter_playlists = 1
    for data in playlists["items"]:
        print("{}. {}\n".format(counter_playlists, data["name"]))
        counter_playlists += 1

    index = input("Please select a playlist from {} to {}: ".format(1, counter_playlists - 1))
    print("\n")
    playlist_id = playlists["items"][int(index) - 1]['id']
    playlist_name = playlists["items"][int(index) - 1]['name']

    print("Okay, this is your playlist ID: {}\n".format(playlist_id))
    add_playlist_counter = -1

    items = []
    not_found = []
    found = []
    for theme in track_updates.keys():
        search = track_search_spotify(track_updates[theme], 20, 0)
        # search['tracks']['items'][0]['name'] / search['tracks']['items'][0]['artists'][0]['name']
        try:
            search_index = 0
            offset = 0
            while True:
                search_id = search['tracks']['items'][search_index]['id']
                artist_name = search['tracks']['items'][search_index]['artists'][0]['name']
                track_name = search['tracks']['items'][search_index]['name']
                # Some names may contain '*' or sometimes '+'
                # This is a known bug with the regex module, added try/except block.
                try:
                    evaluate = re.findall(artist_name, track_updates[theme])
                except re.error:
                    not_found.append(f'{theme} | {track_updates[theme]} Not Found!')
                    evaluate = []
                    pass
                if track_updates[theme] in evaluate:
                    if search_id in items:
                        break
                    else:
                        print(f'Adding: {track_name} | {artist_name}')
                        items.append(search_id)
                        add_playlist_counter += 1
                        search_index = 0
                        break
                else:
                    if search_index < 49:
                        search_index += 1
                        continue
                    else:
                        if offset <= 100:
                            offset += 20
                            search_index = 0
                            search = track_search_spotify(track_updates[theme], 20, offset)
                            continue
                        else:
                            raise IndexError

        except IndexError:
            offset = 0
            search_index = 0
            not_found.append(f'{theme} | {track_updates[theme]} ---> Not Found!')
            add_playlist_counter += 1
            continue

    add_items = spot_client.playlist_add_items(playlist_id, items, position=None)
    print('Added {} elements to your playlist "{}".\n'.format(len(items), playlist_name))
    print(add_items)
    print(f'From these {len(items)} songs, we could not locate:\n')
    for i in not_found:
        print(f'{i} ---> Not found')

if user_choice == 'no':
    print("\n")
    user_specific = input("Add a specific song from the list of updates? (yes / no) ")
    if user_specific == 'yes':
        print('\n')
        user_specific = input("Which number? 1 to {}: ".format(len(track_updates)))
        print("Got it, let me see the matches we've got from spotify. . .\n")
        count_index = 0
        # TODO: Now we have a dictionary not a list...
        search = spot_client.search(track_updates[user_specific], limit=10, offset=0, type='track',
                                    market=None)

        # First ten.
        try:
            for top in range(10):
                search_name = search['tracks']['items'][top]['name']
                search_id = search['tracks']['items'][top]['id']
                artist_name = search['tracks']['items'][top]['artists'][0]['name']
                album_name = search['tracks']['items'][top]['album']['name']
                released = search['tracks']['items'][top]['album']['release_date']
                count_index += 1
                print("{}. {} | {} | {} | Track ID: {}".format(count_index,
                                                               search_name,
                                                               album_name,
                                                               artist_name,
                                                               search_id))
        except IndexError:
            pass
