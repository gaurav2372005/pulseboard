from googleapiclient.discovery import build

API_KEY = "AIzaSyANAhflm-hlpVjBpJH-iDwjgXo99RMEdFY"
CHANNEL_ID = "UCsYprVyA4-b4393_fHq0nEg"

youtube = build("youtube", "v3", developerKey=API_KEY)


request = youtube.channels().list(
    part="snippet,statistics",
    id=CHANNEL_ID
)
response = request.execute()

if not response.get("items"):
    print("No channel found — check ID or API key.")
else:
    channel = response["items"][0]
    print("=== PULSEBOARD - YouTube Stats ===")
    print(f"Channel Name  : {channel['snippet']['title']}")
    print(f"Subscribers   : {channel['statistics']['subscriberCount']}")
    print(f"Total Views   : {channel['statistics']['viewCount']}")
    print(f"Total Videos  : {channel['statistics']['videoCount']}")


# lastest video 
def get_latest_video(channel_id):
    search_response = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=1,
        type="video"
    ).execute()

    if not search_response.get("items"):
        print("No videos found for this channel.")
        return None

    video_id = search_response["items"][0]["id"]["videoId"]
    snippet = search_response["items"][0]["snippet"]

    video_response = youtube.videos().list(
        part="statistics",
        id=video_id
    ).execute()

    stats = video_response["items"][0]["statistics"]

    return {
        "title": snippet["title"],
        "published_at": snippet["publishedAt"],
        "thumbnail": snippet["thumbnails"]["high"]["url"],
        "views": stats.get("viewCount", "0"),
        "likes": stats.get("likeCount", "0"),
        "comments": stats.get("commentCount", "0"),
    }


latest = get_latest_video(CHANNEL_ID)
if latest:
    print("\n=== LATEST VIDEO ===")
    print(f"Title         : {latest['title']}")
    print(f"Published On  : {latest['published_at']}")
    print(f"Views         : {latest['views']}")
    print(f"Likes         : {latest['likes']}")
    print(f"Comments      : {latest['comments']}")

from googleapiclient.discovery import build

API_KEY = "AIzaSyANAhflm-hlpVjBpJH-iDwjgXo99RMEdFY"
CHANNEL_ID = "UCsYprVyA4-b4393_fHq0nEg"

youtube = build("youtube", "v3", developerKey=API_KEY)


request = youtube.channels().list(
    part="snippet,statistics",
    id=CHANNEL_ID
)
response = request.execute()

if not response.get("items"):
    print("No channel found — check ID or API key.")
else:
    channel = response["items"][0]
    print("=== PULSEBOARD - YouTube Stats ===")
    print(f"Channel Name  : {channel['snippet']['title']}")
    print(f"Subscribers   : {channel['statistics']['subscriberCount']}")
    print(f"Total Views   : {channel['statistics']['viewCount']}")
    print(f"Total Videos  : {channel['statistics']['videoCount']}")


# lastest video 
def get_latest_video(channel_id):
    search_response = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=1,
        type="video"
    ).execute()

    if not search_response.get("items"):
        print("No videos found for this channel.")
        return None

    video_id = search_response["items"][0]["id"]["videoId"]
    snippet = search_response["items"][0]["snippet"]

    video_response = youtube.videos().list(
        part="statistics",
        id=video_id
    ).execute()

    stats = video_response["items"][0]["statistics"]

    return {
        "title": snippet["title"],
        "published_at": snippet["publishedAt"],
        "thumbnail": snippet["thumbnails"]["high"]["url"],
        "views": stats.get("viewCount", "0"),
        "likes": stats.get("likeCount", "0"),
        "comments": stats.get("commentCount", "0"),
    }


latest = get_latest_video(CHANNEL_ID)
if latest:
    print("\n=== LATEST VIDEO ===")
    print(f"Title         : {latest['title']}")
    print(f"Published On  : {latest['published_at']}")
    print(f"Views         : {latest['views']}")
    print(f"Likes         : {latest['likes']}")
    print(f"Comments      : {latest['comments']}")

    print(f"Thumbnail     : {latest['thumbnail']}")