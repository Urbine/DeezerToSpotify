import urllib.request
import urllib.parse
import json

# --- In case I need it ---
# import ssl

# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE

# --- +++ ---
# This works if your profile is public. If you have a private profile I'd highly recommend you
# set your profile to public for this process, this will avoid the complexity of working with OAuth tokens which is
# overkill, in my opinion, of course. :)

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


def print_tracks_all(data):
    # Prints out everything about a track, included in a numbered list.
    internal_counter = 0
    allowed_selection = ['y', 'yes', 'n', 'no']
    prompt = input("Would you like to print a numbered list? (y / n) \n")
    if prompt == 'y' or prompt == 'yes':
        for item in data:
            track_name = item['title']
            artist_name = item["artist"]["name"]
            album_title = item["album"]["title"]
            print("{}. {} | {} | {}\n".format(internal_counter,
                                              track_name,
                                              artist_name,
                                              album_title))
            internal_counter += 1

    if prompt == 'n' or prompt == 'no':
        for item in data:
            track_name = item['title']
            artist_name = item["artist"]["name"]
            album_title = item["album"]["title"]
            print("{} | {} | {}\n".format(track_name,
                                          artist_name,
                                          album_title))
            internal_counter += 1

    if prompt not in allowed_selection:
        raise Exception("You typed in an incorrect value, please try again!")
    else:
        pass


def print_track_name_only(data):
    # Just the name of the track, meant for comparison.
    # The comparison algorithm should be improved so from there
    # the need of refactoring every time we make major modifications.
    internal_counter = 0
    allowed_selection = ['y', 'yes', 'n', 'no']
    prompt = input("Would you like to print a numbered list? (y / n) ")
    if prompt == 'y' or prompt == 'yes':
        for item in data:
            track_name = item['title']
            print("{}. {}\n".format(internal_counter, track_name))
            internal_counter += 1

    if prompt == 'n' or prompt == 'no':
        for item in data:
            track_name = item['title']
            print("{}\n".format(track_name))
            internal_counter += 1

    if prompt not in allowed_selection:
        raise Exception("You typed in an incorrect value, please try again!")
    else:
        pass


def print_track_name_and_artist(data):
    # Track name and artist, included in a numbered list
    # if the user specifically chooses so.
    allowed_selection = ['y', 'yes', 'n', 'no']
    internal_counter = 0
    prompt = input("Would you like to print a numbered list? (y / n) ")
    if prompt == 'y' or prompt == 'yes':
        for item in data:
            track_name = item['title']
            artist_name = item["artist"]["name"]
            print("{}. {} | {}\n".format(internal_counter, track_name, artist_name))
            internal_counter += 1

    if prompt == 'n' or prompt == 'no':
        for item in data:
            track_name = item['title']
            artist_name = item["artist"]["name"]
            print("{} | {}\n".format(track_name, artist_name))
            internal_counter += 1

    if prompt not in allowed_selection:
        raise Exception("You typed in an incorrect value, please try again!")
    else:
        pass


def print_albums(data):
    # Prints out the album related to the track, included in a numbered list.
    # Number list is optional.
    internal_counter = 0
    allowed_selection = ['y', 'yes', 'n', 'no']
    prompt = input("Would you like to print a numbered list? (y / n) ")
    if prompt == 'y' or prompt == 'yes':
        for item in data:
            album_title = item["album"]["title"]
            print("{}. {}\n".format(internal_counter, album_title))
            internal_counter += 1

    if prompt == 'n' or prompt == 'no':
        for item in data:
            album_title = item["album"]["title"]
            print("{}".format(album_title))
            internal_counter += 1

    if prompt not in allowed_selection:
        raise Exception("You typed in an incorrect value, please try again!")
    else:
        pass


def print_artist(data):
    # Prints out everything about a track, included in a numbered list.
    internal_counter = 0
    allowed_selection = ['y', 'yes', 'n', 'no']
    prompt = input("Would you like to print a numbered list? (y / n) ")
    if prompt == 'y' or prompt == 'yes':
        for item in data:
            artist_name = item["artist"]["name"]
            print("{}. {}\n".format(internal_counter, artist_name))
            internal_counter += 1

    if prompt == 'n' or prompt == 'no':
        for item in data:
            artist_name = item["artist"]["name"]
            print("{}\n".format(artist_name))
            internal_counter += 1

        if prompt not in allowed_selection:
            raise Exception("You typed in an incorrect value, please try again!")
        else:
            pass

# TODO: Investigate why the items are being dismissed and file not created.
def write_tracks(file_name, data):
    # For this function we need to handle a TypeError exception.
    # When the previous functions finish doing their job, they return None
    # this will end up in exception if not handled.
    print("What would you like to write? \n")
    options = ["Track Name and Artist", "Track Name", "Album", "Artist", "All (default/recommended)"]
    for number, option in enumerate(options, start=1):
        print("{}. {}\n".format(number, option))

    prompt = input("Please type in the option number: ()")
    # The input from the user is always a string. ;)
    try:
        if prompt == '1':
            file_name.write(print_track_name_and_artist(data))

        if prompt == '2':
            file_name.write(print_track_name_only(data))

        if prompt == '3':
            file_name.write(print_albums(data))

        if prompt == '4':
            file_name.write(print_artist(data))

        if prompt == '5':
            file_name.write(print_tracks_all(data))
    except TypeError:
        print("=== Text file ready ===")
        print(" -----> Exiting <----- ")
        quit()


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
            print_tracks_all(dat["tracks"]["data"])

            print("\n")
            echo_to_file = input("Would you like to write the contents of this list to a text file? (yes / no) ")
            if echo_to_file == 'yes':
                playlist_name = js["data"][int(index) - 1]['title']
                with open('tracks-playlist-' + playlist_name + ".txt", "a+", encoding="utf-8") as tracks:
                    playlist_id = js["data"][int(index) - 1]['id']
                    track_url = "https://api.deezer.com/playlist/" + str(playlist_id)
                    result = urllib.request.urlopen(track_url).read()
                    dat = json.loads(result)
                    total = dat["nb_tracks"]
                    number_of_tracks = input("Include number of tracks? (y / n)")
                    if number_of_tracks == 'y' or 'yes':
                        tracks.write(" **** This playlist has a total of {} tracks. ****\n".format(total))
                        write_tracks(tracks, dat["tracks"]["data"])
                    else:
                        write_tracks(tracks, dat["tracks"]["data"])

            if echo_to_file == "no":
                print("\n")
                print("=== Alright, exiting... ===")
                break

        if track_choice == 'no':
            print("\n")
            print("=== Alright, exiting... ===")
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
