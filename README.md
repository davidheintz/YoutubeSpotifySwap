# YouTubeSpotifySwap

This program was created by myself, David Heintz

The purpose of this program is to transfer music between Spotify and YouTube in 2 different ways.

First: the program will use all videos in a user's YouTube playlist to generate a new Spotify playlist of all the songs found.

Second: the program will use all songs in a user's Spotify playlist to generate a new YouTube playlist with all the music videos founds from the songs.

This program uses apis and OAuth user consent (with client secret file) to allow user to login to YouTube and Spotify accounts and authorize program to access and manipulate their information (only used to access and generate playlists)

Current stage: program gets YouTube user authorization a reformats 2 playlists (user's first playlist, and a Kanye West playlist from playlist id provided in code)
* the reformatting splits the video title into song and artist name, along with features and other attributes of the song found (if video title not related to a song or album, it won't be found in spotify) *
