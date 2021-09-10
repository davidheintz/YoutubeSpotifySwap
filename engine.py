from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import pandas as pd


# uses key param to generate youtube build
def gen_public_build(key):
    return build('youtube', 'v3', developerKey=key)


# takes in build and playlistId and generates list of id's of videos on playlist
def get_playlist(yt, pid):

    # generate list of content details of each song on playlist
    pl_request = yt.playlistItems().list(
        part='contentDetails',
        playlistId=pid,
        maxResults=200,
        pageToken=None).execute()

    vid_ids = []

    # store videoId's in array to return
    for item in pl_request['items']:
        vid_ids.append(item['contentDetails']['videoId'])
    return vid_ids  # can now be searched individually


# prompts user to login using client_secret and url, then generates instance w tokens
def enter_user_account():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes=["https://www.googleapis.com/auth/youtube"])

    flow.run_local_server(port=8080, prompt="consent")  # using localhost:8080


# use access token, generate new one using refresh, or prompt login
def gen_user_token():
    cred = None

    # load token
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            cred = pickle.load(token)

    # if token not valid or created
    if not cred or not cred.valid:
        # if expired, generate new one with credentials.refresh
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        # if not created, prompt user login to generate tokens
        else:
            enter_user_account()

            with open("token.pickle", "wb") as f:
                pickle.dump(cred, f)
    # generate build using token
    youtube = build('youtube', 'v3', credentials=cred)
    return youtube


# gets user playlists using build.playlists().list, then store title and id in dataframe
def get_user_playlists(yt):
    all_play = yt.playlists().list(part="id, snippet", mine=True).execute()
    pl_list = pd.DataFrame(columns=['title', 'id'])
    for item in all_play['items']:
        pl_list = pl_list.append({'title': item['snippet']['title'], 'id': item['id']},
                                 ignore_index=True)
    return pl_list


# generate new playlist in user account using build.playlists().insert
# params t, d, s become title, description, and status for the playlist
def gen_user_playlist(yt, t, d, s):
    resp = yt.playlists().insert(part="snippet,status",
                                 body=dict(snippet=dict(
                                     title=t,
                                     description=d
                                 ),
                                     status=dict(
                                         privacyStatus=s
                                     )
                                 ), fields="id").execute()
    return resp


# transforms list of video id's (pl_ids) into a dataframe of video information
def clean_playlist(yt, pl_ids):

    # get video snippet information from each id
    vid_request = yt.videos().list(
        part="snippet",
        id=','.join(pl_ids)
    )

    # storing video title and channel of each video in dataframe columns
    vid_info = pd.DataFrame(columns=['title', 'channel'])
    vid_response = vid_request.execute()
    for item in vid_response['items']:
        vid_info = vid_info.append({'title': item['snippet']['title'], 'channel': item['snippet']['channelTitle']},
                                   ignore_index=True)

    # if ' - ' found: split video into artist, song because that the most common format
    if vid_info['title'].str.contains(' - ').sum() > 0:
        vid_info[['artist', 'song']] = vid_info['title'].str.split(' - ', expand=True)

    # if no ' - ', assume whole title is song and artist in account name
    else:
        vid_info['song'] = vid_info['title']

    # if some songs don't contain ' - ', fix misplacement of song into artist
    vid_info.loc[vid_info.artist == vid_info.title, 'song'] = vid_info['title']
    vid_info.loc[vid_info.artist == vid_info.title, 'artist'] = None

    # if ' ft. ' found in songs, split into song name and features
    if vid_info['title'].str.contains(' ft. ').sum() > 0:
        vid_info[['song', 'features']] = vid_info['song'].str.split(' ft. ', expand=True)

    # more cleaning:
    vid_info.drop(['title'], axis=1, inplace=True)  # eliminate title column after used
    vid_info['explicit'] = vid_info['song'].str.find(r'(Explicit)')  # count explicit instances
    vid_info['song'] = vid_info['song'].str.replace(r' \(.*\)', '')  # delete all items in ()
    return vid_info
