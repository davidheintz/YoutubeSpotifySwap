import engine

api_key = 'AIzaSyCu7nbedRlnqFMeKBLnE8yLRbKppWgJNTE'
playlist_id = 'PLdYwhvDpx0FI2cmiSVn5cMufHjYHpo_88'

# generates youtube build using api_key variable
# then generates list of song id's using a playlistId and the generated build
youtube = engine.gen_public_build(api_key)
kanye_pl = engine.get_playlist(youtube, playlist_id)

# kanye playlist items reformatted into dataframe using clean method
kanye_info = engine.clean_playlist(youtube, kanye_pl)

# user login prompt and generate new build using gen_user_token method
# list of id's from user playlists generated using new build
# using a single id, video info is gathered, cleaned, and stored in dataframe
youtube = engine.gen_user_token()
my_pl = engine.get_user_playlists(youtube)
first_pl = engine.get_playlist(youtube, my_pl.at[0, "id"])
pl_info = engine.clean_playlist(youtube, first_pl)

# print out reformatted playlist video info
print(kanye_info)
print(pl_info)
