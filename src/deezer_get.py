# This script will retrieve your user data from Deezer, if your profile is public.
# If you have a private profile, I'd highly recommend you set your profile to public for this process can
# succeed. Basically this reduces the complexity of this script by not including OAuth/Token Exchange
# procedures.

import urllib.request
import urllib.parse
import json

# --- In case I need it ---
# import ssl
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
# --- +++ ---

# E.g 1820946382
user_id = input("Enter your Deezer user ID: ")
content_type = "playlists"
url = "https://api.deezer.com/user/"

values = int(user_id)
enc = url + '/' + user_id + '/' + content_type
uh = urllib.request.urlopen(enc).read()
js = json.loads(uh)
js_layout = json.dumps(js, indent=2)

print("\n")
print("=== Here you go, we've retrieved these {}. === \n".format(content_type))

count_index = 1
for info in js["data"]:
    print("{}. {} | Playlist ID: {}".format(count_index, info['title'], info['id']))
    count_index += 1

print("\n")
track_choice = input("Would you like to see the track list from one of these playlists? (yes / no) ")


def get_tracks_info(data, num_choice=False):
    """
    This function returns specific information about each track.
    1. Number
    2. Title
    3. Artist name
    4. Album title
    :param data: data requires a JSON file loaded as string (.loads method)
    :param num_choice: num_choice is a Boolean value and it's optional parameter.
    :return: List of tuples
    e.g [(1, Hotel California, The Eagles),...]
    """
    internal_counter = 1
    results = []
    if num_choice:
        for item in data:
            track_name = item['title']
            artist_name = item["artist"]["name"]
            album_title = item["album"]["title"]
            results.append((str(internal_counter),
                            track_name,
                            artist_name,
                            album_title))
            internal_counter += 1
    else:
        for item in data:
            track_name = item['title']
            artist_name = item["artist"]["name"]
            album_title = item["album"]["title"]
            results.append((track_name, artist_name, album_title))
    return results


def get_track_name_artist_only(data, num_choice=False):
    """
    This function returns specific information about each of the tracks
    with or without enumeration.
    1. Title
    2. Artist name
    3. Track number (if num_choice is set to True)
    :param num_choice: Adds a number in the tuple containing the track info.
    :param data: data requires a JSON file loaded as string (.loads method)
    :return: List of tuples.
    e.g [(Hotel California, The Eagles),...]
    """
    results = []
    track_info = get_tracks_info(data, num_choice=num_choice)
    if num_choice:
        for num, title, artist, album in track_info:
            pack = (num, title, artist)
            results.append(pack)
    else:
        for title, artist, album in track_info:
            pack = (title, artist)
            results.append(pack)
    return results


def get_albums(data, num_choice=False):
    """
    This function returns the album name with or without enumeration.
    1. Album name
    2. Element number (if num_choice is set to True)
    :param num_choice: Adds a number in the tuple containing the track info.
    :param data: data requires a JSON file loaded as string (.loads method)
    :return: List of tuples or just a list if the number is not added.
    e.g [(Hotel California, The Eagles),...]
    """
    results = []
    track_info = get_tracks_info(data, num_choice=num_choice)
    if num_choice:
        for num, title, artist, album in track_info:
            pack = (num, album)
            results.append(pack)
    else:
        for title, artist, album in track_info:
            results.append(album)
    return results


def get_track_name(data, num_choice=False):
    """
    This function returns the track name with or without enumeration.
    1. Track name
    2. Element number (if num_choice is set to True)
    :param num_choice: Adds a number in the tuple containing the track info.
    :param data: data requires a JSON file loaded as string (.loads method)
    :return: List of tuples or just a list if the number is not added.
    e.g [(Hotel California, The Eagles),...]
    """
    results = []
    track_info = get_tracks_info(data, num_choice=num_choice)
    if num_choice:
        for num, title, artist, album in track_info:
            pack = (num, title)
            results.append(pack)
    else:
        for title, artist, album in track_info:
            results.append(title)
    return results


def get_artist(data, num_choice=False):
    """
    This function returns the artist name with or without enumeration.
    1. Artist name
    2. Element number (if num_choice is set to True)
    :param num_choice: Adds a number in the tuple containing the track info.
    :param data: data requires a JSON file loaded as string (.loads method)
    :return: List of tuples or just a list if the number is not added.
    e.g [(Hotel California, The Eagles),...]
    """
    results = []
    track_info = get_tracks_info(data, num_choice=num_choice)
    if num_choice:
        for num, title, artist, album in track_info:
            pack = (num, artist)
            results.append(pack)
    else:
        for title, artist, album in track_info:
            results.append(artist)
    return results


def write_tracks(file_name, data):
    """
    This function will write the objects into the file selected.
    It should be used when there is a file handle already and we just
    want to write the contents.
    :param file_name: file name assigned to the file handle
    :param data: data coming from the JSON loaded file to be processed by other functions.
    """
    print("What would you like to write? \n")
    options = ("Track Name and Artist", "Track Name", "Album", "Artist", "All (default/recommended)")
    for number, option in enumerate(options, start=1):
        print("{}. {}".format(number, option))
    prompt = input("Please type in the option number: ")
    # The input from the user is always a string. ;)
    if prompt == '1':
        print_list = get_track_name_artist_only(data)
        for i, k in print_list:
            file_name.write("{} | {}\n".format(i, k))
    if prompt == '2':
        print_list = get_track_name(data)
        for i in print_list:
            file_name.write("{}\n".format(i))
    if prompt == '3':
        print_list = get_albums(data)
        for i in print_list:
            file_name.write("{}\n".format(i))
    if prompt == '4':
        print_list = get_artist(data)
        for i in print_list:
            file_name.write("{}\n".format(i))
    if prompt == '5':
        print_list = get_tracks_info(data)
        for i, j, k in print_list:
            file_name.write("{} | {} | {}\n".format(i, j, k))

while True:
    try:
        if track_choice == 'yes':
            print("\n")
            index = input("Which number? ")
            print("\n")
            playlist_id = js["data"][int(index) - 1]['id']
            track_url = "https://api.deezer.com/playlist/" + str(playlist_id)
            result = urllib.request.urlopen(track_url).read()
            dat = json.loads(result)
            count_track = 1
            total = dat["nb_tracks"]
            print("This playlist has a total of {} tracks.\n".format(total))

            # Data = dat["tracks"]["data"] >> this is passed into all printing functions.
            tracks = get_tracks_info(dat["tracks"]["data"], num_choice=True)
            for x, j, k, l in tracks:
                print("{}. {} | {} | {}".format(x, j, k, l))

            print("\n")
            echo_to_file = input("Would you like to write the contents of this list to a text file? (yes / no) ")
            if echo_to_file == 'yes':
                playlist_name = js["data"][int(index) - 1]['title']
                with open('tracks-playlist-'
                          + playlist_id
                          + '.txt',
                          "a+", encoding="utf-8") as tracks:
                    playlist_id = js["data"][int(index) - 1]['id']
                    track_url = "https://api.deezer.com/playlist/" + str(playlist_id)
                    result = urllib.request.urlopen(track_url).read()
                    dat = json.loads(result)
                    total = dat["nb_tracks"]
                    write_tracks(tracks, dat["tracks"]["data"])
                    break

            if echo_to_file == "no":
                print("\n")
                print("=== Alright, exiting... ===")
                break

        if track_choice == 'no':
            print("\n")
            print('=== If you would like to print the contents to a file, select "yes" next time. ===')
            break

    except Exception as ex:
        print(ex)
        print("\n")
        print("Please enter yes or no!")
        print("\n")
        track_choice = input("Would you like to see the track list from one of these playlists? (yes / no) ")
        if track_choice == "yes":
            continue
        else:
            print("\n")
            print("=== Alright, exiting... ===")
            break
