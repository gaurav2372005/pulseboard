import os
import json
import requests
import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
]

def load_client_secrets():
    # Try Streamlit secrets first (cloud + local .streamlit/secrets.toml)
    try:
        cfg = st.secrets["google_client"]
        return {
            "client_id"    : cfg["client_id"],
            "client_secret": cfg["client_secret"],
            "redirect_uri" : cfg["redirect_uris"]
        }
    except Exception:
        pass

    # Fallback to client_secrets.json for local dev
    with open("client_secrets.json", "r") as f:
        data = json.load(f)["web"]
    return {
        "client_id"    : data["client_id"],
        "client_secret": data["client_secret"],
        "redirect_uri" : data["redirect_uris"][0]
    }

def get_auth_url():
    import urllib.parse
    secrets = load_client_secrets()
    params  = {
        "client_id"    : secrets["client_id"],
        "redirect_uri" : secrets["redirect_uri"],
        "response_type": "code",
        "scope"        : " ".join(SCOPES),
        "access_type"  : "offline",
        "prompt"       : "consent"
    }
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)

def exchange_code_for_token(code):
    secrets   = load_client_secrets()
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code"         : code,
        "client_id"    : secrets["client_id"],
        "client_secret": secrets["client_secret"],
        "redirect_uri" : secrets["redirect_uri"],
        "grant_type"   : "authorization_code"
    }
    response   = requests.post(token_url, data=data)
    token_data = response.json()

    if "error" in token_data:
        raise Exception(f"Token error: {token_data}")

    return Credentials(
        token         = token_data["access_token"],
        refresh_token = token_data.get("refresh_token"),
        token_uri     = "https://oauth2.googleapis.com/token",
        client_id     = secrets["client_id"],
        client_secret = secrets["client_secret"],
        scopes        = SCOPES
    )

def get_youtube_client(credentials):
    return build("youtube", "v3", credentials=credentials)

def get_user_info(credentials):
    service = build("oauth2", "v2", credentials=credentials)
    return service.userinfo().get().execute()

def get_channel_info(youtube):
    res = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        mine=True
    ).execute()
    if not res.get("items"):
        return None
    return res["items"][0]

def get_all_videos(youtube, playlist_id):
    video_ids       = []
    next_page_token = None
    while True:
        res = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        for item in res["items"]:
            video_ids.append(item["contentDetails"]["videoId"])
        next_page_token = res.get("nextPageToken")
        if not next_page_token:
            break
    return video_ids

def get_video_stats(youtube, video_ids):
    import pandas as pd
    all_videos = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        res   = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(batch)
        ).execute()
        for item in res["items"]:
            stats   = item.get("statistics", {})
            snippet = item.get("snippet", {})
            all_videos.append({
                "video_id"    : item["id"],
                "title"       : snippet.get("title", ""),
                "published_at": snippet.get("publishedAt", ""),
                "views"       : int(stats.get("viewCount",    0)),
                "likes"       : int(stats.get("likeCount",    0)),
                "comments"    : int(stats.get("commentCount", 0)),
                "thumbnail"   : snippet.get("thumbnails", {})
                                       .get("high", {})
                                       .get("url", "")
            })
    df = pd.DataFrame(all_videos)
    if not df.empty:
        df["published_at"] = pd.to_datetime(df["published_at"])
        df = df.sort_values("published_at", ascending=False).reset_index(drop=True)
    return df