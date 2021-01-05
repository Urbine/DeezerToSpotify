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
track_choice = input("Would you like to see the tracklist from one of these playlists? (yes / no) ")


def print_tracks():
    track_name = track['title']
    artist_name = track["artist"]["name"]
    album_title = track["album"]["title"]
    print("{}. {} | {} | {}".format(count_track, track_name, artist_name, album_title))


def write_tracks():
    track_name = track['title']
    artist_name = track["artist"]["name"]
    album_title = track["album"]["title"]
    # tracks.write("{}. {} | {} | {}\n".format(count_track, track_name, artist_name, album_title))
    tracks.write(track_name + "\n")


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

            for track in dat["tracks"]["data"]:
                print_tracks()
                count_track += 1

            print("\n")
            echo_to_file = input("Would you like to write the contents of this list to a text file? (yes / no) ")
            if echo_to_file == 'yes':
                playlist_name = js["data"][int(index) - 1]['title']
                with open('tracks-playlist-' + playlist_name + ".txt", "a+", encoding="utf-8") as tracks:
                    playlist_id = js["data"][int(index) - 1]['id']
                    track_url = "https://api.deezer.com/playlist/" + str(playlist_id)
                    result = urllib.request.urlopen(track_url).read()
                    dat = json.loads(result)
                    count_track = 1
                    total = dat["nb_tracks"]
                    # tracks.write(" **** This playlist has a total of {} tracks. ****\n".format(total))

                    for track in dat["tracks"]["data"]:
                        write_tracks()
                        count_track += 1
                        if count_track == total:
                            print("=== Text file ready ===")
                            print(" -----> Exiting <----- ")
                break

            if echo_to_file == "no":
                print("\n")
                print("=== Alright, exiting... ===")
                break

        if track_choice == 'no':
            print("\n")
            print("=== Alright, exiting... ===")
            break

    except:
        print("\n")
        print("Please enter yes or no!")
        print("\n")
        track_choice = input("Would you like to see the tracklist from one of these playlists? (yes / no) ")
        if track_choice == "yes":
            continue
        else:
            print("\n")
            print("=== Alright, exiting... ===")
            break
