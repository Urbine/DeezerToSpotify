# In this file I am comparing both file to see the updates in a specific list.
# In this case, I want to see how much the deezer playlist has changed and apply those changes to Spotify.

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

# import ssl
#
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE

scope = "user-library-read user-library-modify playlist-read-private playlist-modify-private "
# cli_id = input("Please enter your Spotify Client ID: ") #  32878798075240d98dee5b2ad2a70e5a
# cli_secret = input("Please enter your Spotify Client Secret:  ") # 433594c80b6044ee9c92b87438e8e170
# redir_uri = input("Please enter your redirect URI: ")

# Common redirect URI: http://localhost:8888/callback/ <whitelisted in Spotify>

cl_id = "32878798075240d98dee5b2ad2a70e5a"
secret = "433594c80b6044ee9c92b87438e8e170"
uri = "http://localhost:8888/callback/"  # Whitelist this URI within the application page.

spot_client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cl_id,
                                                        client_secret=secret,
                                                        redirect_uri=uri,
                                                        scope=scope))


# TODO: Add an option for the user to enter the file name.
# TODO: Add a boolean based list to display the migration results to the user.
# TODO: Try with list of tuples once again.
def get_from_file(file_name):
    results = {}
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for ln in file.readlines():
                st = ln.split("|")
                key = st[1].strip()
                val = st[0].strip()
                if key in results.keys():
                    continue
                else:
                    results[key] = val
        return results
    except IndexError:
        print("This item could not be processed" + str(st))
        pass


# TODO: Find a way to match the content of a key, not part of it.
def find_updates(data_one, data_two):
    updates = {}
    for key in data_one.keys():
        if key in data_two.keys():
            if data_two[key] is data_one[key]:
                continue
            else:
                updates[key] = data_one[key]
        else:
            updates[key] = data_one[key]
        return updates


file_deezer = "tracks-playlist-Love Songs.txt"
file_spotify = "tracks-playlist-Love Songs-Spotify.txt"

tracks_deezer = get_from_file(file_deezer)
tracks_spotify = get_from_file(file_spotify)

track_updates = find_updates(tracks_deezer, tracks_spotify)

print("We've found these tracks below are not in Spotify yet! \n")
update_counter = 1
for key, val in track_updates.items():
    print(f'{key} | {val}')
    update_counter += 1

# TODO: Redo list comparison algorithm. IDEA! Word comparison.

print("\n")
print("In total, we found {} tracks".format(update_counter - 1))

print("\n")

print("If you choose to add all tracks, we'll add the first result in every occurrence of the track.")
user_choice = input("Would you like to add all the tracks to Spotify? (yes / no) \n")

# Spotify API encodes queries by adding "%20", "%28", "%29" or "+"
# if there's a whitespace, and adds it to the address.
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
    username = input("Please enter your Spotify username: ")  # TODO: Delete this line of code
    add_playlist_counter = -1

    items = []
    for track in range(len(track_updates)):
        search = spot_client.search(track_updates[track], limit=10, offset=0, type='track',
                                    market=None)
        try:
            search_id = search['tracks']['items'][0]['id']
            if search_id in items:
                pass
            else:
                items.append(search_id)
                add_playlist_counter += 1
        except IndexError:
            add_playlist_counter += 1
            continue

    add_items = spot_client.playlist_add_items(playlist_id, items, position=None)
    print('Adding {} elements to your playlist "{}".\n'.format(len(items), playlist_name))
    print(add_items)

if user_choice == 'no':
    print("\n")
    user_specific = input("Add a specific song from the list of updates? (yes / no) ")
    if user_specific == 'yes':
        print('\n')
        user_specific = input("Which number? 1 to {}: ".format(len(track_updates)))
        print("Got it, let me see the matches we've got from spotify. . .\n")
        count_index = 0
        search = spot_client.search(track_updates[int(user_specific) - 1], limit=10, offset=0, type='track',
                                    market=None)

        # First ten.
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
