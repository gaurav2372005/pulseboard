<<<<<<< HEAD
import pandas as pd
from googleapiclient.discovery import build

# ── Config ────────────────────────────────────────────────
API_KEY    = "AIzaSyANAhflm-hlpVjBpJH-iDwjgXo99RMEdFY"        # same key from fetch.py
CHANNEL_ID = "UCsYprVyA4-b4393_fHq0nEg" # same UC... ID from fetch.py

youtube = build("youtube", "v3", developerKey=API_KEY)

# ── Step 1: Get the uploads playlist ID ───────────────────
def get_uploads_playlist_id():
    res = youtube.channels().list(
        part="contentDetails",
        id=CHANNEL_ID
    ).execute()
    return res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# ── Step 2: Get all video IDs from the playlist ───────────
def get_all_video_ids(playlist_id):
    video_ids = []
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

# ── Step 3: Get stats for each video ──────────────────────
def get_video_stats(video_ids):
    all_videos = []

    # YouTube API allows max 50 IDs per request
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        res = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(batch)
        ).execute()

        for item in res["items"]:
            stats   = item.get("statistics", {})
            snippet = item.get("snippet", {})

            all_videos.append({
                "video_id"      : item["id"],
                "title"         : snippet.get("title", ""),
                "published_at"  : snippet.get("publishedAt", ""),
                "views"         : int(stats.get("viewCount",    0)),
                "likes"         : int(stats.get("likeCount",    0)),
                "comments"      : int(stats.get("commentCount", 0)),
                "thumbnail"     : snippet.get("thumbnails", {})
                                         .get("high", {})
                                         .get("url", "")
            })

    return all_videos

# ── Step 4: Build DataFrame ───────────────────────────────
def fetch_all_videos():
    print("Fetching uploads playlist...")
    playlist_id = get_uploads_playlist_id()

    print("Fetching video IDs...")
    video_ids = get_all_video_ids(playlist_id)
    print(f"Found {len(video_ids)} videos")

    print("Fetching video stats...")
    videos = get_video_stats(video_ids)

    df = pd.DataFrame(videos)
    df["published_at"] = pd.to_datetime(df["published_at"])
    df = df.sort_values("published_at", ascending=False).reset_index(drop=True)

    return df

# ── Run ───────────────────────────────────────────────────
if __name__ == "__main__":
    df = fetch_all_videos()

    print("\n=== ALL VIDEOS ===")
    print(df[["title", "views", "likes", "comments"]].to_string())

    print("\n=== SUMMARY ===")
    print(f"Total videos  : {len(df)}")
    print(f"Total views   : {df['views'].sum():,}")
    print(f"Total likes   : {df['likes'].sum():,}")
    print(f"Avg views/vid : {df['views'].mean():.1f}")
=======
import pandas as pd
from googleapiclient.discovery import build

# ── Config ────────────────────────────────────────────────
API_KEY    = "AIzaSyANAhflm-hlpVjBpJH-iDwjgXo99RMEdFY"        # same key from fetch.py
CHANNEL_ID = "UCsYprVyA4-b4393_fHq0nEg" # same UC... ID from fetch.py

youtube = build("youtube", "v3", developerKey=API_KEY)

# ── Step 1: Get the uploads playlist ID ───────────────────
def get_uploads_playlist_id():
    res = youtube.channels().list(
        part="contentDetails",
        id=CHANNEL_ID
    ).execute()
    return res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# ── Step 2: Get all video IDs from the playlist ───────────
def get_all_video_ids(playlist_id):
    video_ids = []
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

# ── Step 3: Get stats for each video ──────────────────────
def get_video_stats(video_ids):
    all_videos = []

    # YouTube API allows max 50 IDs per request
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        res = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(batch)
        ).execute()

        for item in res["items"]:
            stats   = item.get("statistics", {})
            snippet = item.get("snippet", {})

            all_videos.append({
                "video_id"      : item["id"],
                "title"         : snippet.get("title", ""),
                "published_at"  : snippet.get("publishedAt", ""),
                "views"         : int(stats.get("viewCount",    0)),
                "likes"         : int(stats.get("likeCount",    0)),
                "comments"      : int(stats.get("commentCount", 0)),
                "thumbnail"     : snippet.get("thumbnails", {})
                                         .get("high", {})
                                         .get("url", "")
            })

    return all_videos

# ── Step 4: Build DataFrame ───────────────────────────────
def fetch_all_videos():
    print("Fetching uploads playlist...")
    playlist_id = get_uploads_playlist_id()

    print("Fetching video IDs...")
    video_ids = get_all_video_ids(playlist_id)
    print(f"Found {len(video_ids)} videos")

    print("Fetching video stats...")
    videos = get_video_stats(video_ids)

    df = pd.DataFrame(videos)
    df["published_at"] = pd.to_datetime(df["published_at"])
    df = df.sort_values("published_at", ascending=False).reset_index(drop=True)

    return df

# ── Run ───────────────────────────────────────────────────
if __name__ == "__main__":
    df = fetch_all_videos()

    print("\n=== ALL VIDEOS ===")
    print(df[["title", "views", "likes", "comments"]].to_string())

    print("\n=== SUMMARY ===")
    print(f"Total videos  : {len(df)}")
    print(f"Total views   : {df['views'].sum():,}")
    print(f"Total likes   : {df['likes'].sum():,}")
    print(f"Avg views/vid : {df['views'].mean():.1f}")
>>>>>>> f9b4a5240b4d2356f3186c2debbace000dc7a5f6
    print(f"Top video     : {df.iloc[0]['title']} ({df.iloc[0]['views']} views)")