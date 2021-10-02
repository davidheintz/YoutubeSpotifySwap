import engine

import pandas as pd

api_key = 'AIzaSyCu7nbedRlnqFMeKBLnE8yLRbKppWgJNTE'
playlist_id = 'PLyORnIW1xT6zumu3ulCtqQXO0FaIZUsdQ'

client_id = '7d1774da3ede46d491c9a387cf7309be'
client_secret = '9feabd94101f41e1b3ed8e8f80b13fab'

sp_df = pd.read_excel('spotify_data.xlsx')
yt_df = pd.read_excel('youtube_data.xlsx')

print(yt_df)
print(sp_df)

# generates youtube build using api_key variable
# then generates list of song id's using a playlistId and the generated build
youtube = engine.gen_public_build(api_key)
edm_pl = engine.get_playlist(youtube, playlist_id)

# edm playlist items reformatted into dataframe using clean method
edm_info = engine.clean_playlist(youtube, edm_pl)

# user login prompt and generate new build using gen_user_token method
# list of id's from user playlists generated using new build
# using a single id, video info is gathered, cleaned, and stored in dataframe
youtube = engine.gen_user_token()
my_pl = engine.get_user_playlists(youtube)
first_pl = engine.get_playlist(youtube, my_pl.at[0, "id"])
pl_info = engine.clean_playlist(youtube, first_pl)

# spotify user authorization
user = 'davidheintz'
sp = engine.spotify_user_authentication(client_id, client_secret, user)
sp_pl = engine.get_spotify_user_playlists(sp, user)


yt_ids = engine.search_for_ids(youtube, sp_pl, 'Bangers')
yt_id_df = pd.DataFrame(yt_ids, columns=['Bangers_yt_ids'])

sp_to_yt_out = pd.concat([sp_pl, yt_id_df], ignore_index=True, axis=1)

"""title = 'Bangers (from Spotify)'
desc = 'top searches for each song on my Spotify playlist called Bangers'
resp = engine.gen_user_playlist(youtube, title, desc, 'public')
for vid in yt_ids:
    engine.add_video_to_playlist(resp["id"], vid)"""


sp_to_yt_out.to_excel('spotify_data.xlsx')
pl_info.to_excel('youtube_data.xlsx')

"""f = open('spotify_data.xlsx', 'w')
f.write('spotify_data.xlsx')
f.close()"""

# print out reformatted playlist video info
print(edm_info)
print(pl_info)

sp_df = pd.read_excel('spotify_data.xlsx')
yt_df = pd.read_excel('youtube_data.xlsx')

print(yt_df)
print(sp_df)
