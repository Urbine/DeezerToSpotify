import spotipy
from spotipy.oauth2 import SpotifyOAuth

# import ssl
#
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE

sco = "user-library-read user-library-modify playlist-read-private playlist-modify-private"
# cli_id = input("Please enter your Spotify Client ID: ") #  32878798075240d98dee5b2ad2a70e5a
# cli_secret = input("Please enter your Spotify Client Secret:  ") # 433594c80b6044ee9c92b87438e8e170
# redir_uri = input("Please enter your redirect URI: ")

# Common redirect URI: http://localhost:8888/callback/ <whitelisted in Spotify>

# TODO: Resolve token issues

cl_id = "32878798075240d98dee5b2ad2a70e5a"
secret = "433594c80b6044ee9c92b87438e8e170"
uri = "http://localhost:8888/callback/"  # Whitelist this URI within the application page.

spot_client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cl_id,
                                                        client_secret=secret,
                                                        redirect_uri=uri,
                                                        scope=sco))

print("Here's a list of your playlists:\n")
playlists = spot_client.current_user_playlists(limit=50, offset=0)

counter_index = 1
for data in playlists["items"]:
    print("{}. {} | Playlist ID: {}\n".format(counter_index, data["name"], data["id"]))
    counter_index += 1


def call_playlist_items(offset):
    return spot_client.playlist_items(playlist_id,
                                      fields=None,
                                      limit=100,
                                      offset=offset)


index = input("Please select a playlist from {} to {}: ".format(1, counter_index - 1))
print("\n")
playlist_id = playlists["items"][int(index) - 1]['id']

locate_playlist_call = call_playlist_items(0)  # Needed to extract "total" variable.
count_track = 1
offset_count = 0
total = locate_playlist_call["total"]

track_names = []
artist_names = []
album_names = []

print("This playlist has a total of {} tracks.\n".format(total))

while True:
    locate_playlist_call = call_playlist_items(offset_count)
    # TODO: Place an option to select the field the user wants to print.
    for track in locate_playlist_call["items"]:
        track_name = track["track"]["name"]
        artist_name = track["track"]["album"]["artists"][0]["name"]
        album_title = track["track"]["album"]["name"]
        track_names.append(track_name)
        artist_names.append(artist_name)
        album_names.append(album_title)
        print("{}. {} | {} | {}".format(count_track, track_name, artist_name, album_title))
        count_track += 1
        offset_count += 1

    print("\n")
    # If there are no more results than those already printed, the module handles the exception.
    # In that case the method call will result in a blank line, prompting for the option anew.
    cont = input("Would you like to continue to the next page of results? (yes / no) \n")

    if cont == 'yes':
        locate_playlist_call = call_playlist_items(offset_count + 100)
        continue

    if cont == 'no':
        print("=== Okay, closing connection... ===")
        break
    else:
        print("\n")
        print("Please enter yes or no as specified.")
        print("Showing next page of results, if any...\n")
        continue

print("\n")
echo_to_file = input("Would you like to write the contents of this list to a text file? (yes / no) ")

if echo_to_file == 'yes':
    playlist_name = playlists["items"][int(index) - 1]['name']
    combined = zip(track_names, artist_names, album_names)
    with open('tracks-playlist-' + playlist_name + "-Spotify.txt", "a+", encoding="utf-8") as track_list:
        count_track = 1
        for track, artist, album in combined:
            track_list.write("{} | {}\n".format(track, artist))  # Deleted count_track and album
            # track_list.write(track + "\n")
            count_track += 1
            if count_track == total:
                print("=== Text file ready ===")
                print(" -----> Exiting <----- ")
else:
    print("\n")
    print("==== Alright, exiting... ===")
