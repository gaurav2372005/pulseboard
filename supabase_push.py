from supabase import create_client
from videos import fetch_all_videos
from datetime import timezone

# ── Config ────────────────────────────────────────────────
SUPABASE_URL =  "https://gyelcdzeqzpdaaymxhae.supabase.co"  # https://xxxx.supabase.co
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd5ZWxjZHplcXpwZGFheW14aGFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODMwMDY1MTcsImV4cCI6MjA5ODU4MjUxN30.xZ7avn_Crjx4Bos_IpI5oUCgsHIQgZm24IoieQz4OfA"      # anon public key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── Push data to Supabase ─────────────────────────────────
def push_videos():
    print("Fetching video data...")
    df = fetch_all_videos()

    # Convert DataFrame to list of dicts
    records = []
    for _, row in df.iterrows():
        records.append({
            "video_id"    : row["video_id"],
            "title"       : row["title"],
            "published_at": row["published_at"].isoformat(),
            "views"       : int(row["views"]),
            "likes"       : int(row["likes"]),
            "comments"    : int(row["comments"]),
            "thumbnail"   : row["thumbnail"]
        })

    print(f"Pushing {len(records)} videos to Supabase...")

    # Upsert — updates if video_id exists, inserts if new
    result = supabase.table("youtube_videos").upsert(records).execute()

    print(f"✅ Done! {len(result.data)} rows pushed to Supabase.")
    return result

# ── Run ───────────────────────────────────────────────────
if __name__ == "__main__":

 from supabase import create_client
 from videos import fetch_all_videos
 from datetime import timezone

# ── Config ────────────────────────────────────────────────
SUPABASE_URL =  "https://gyelcdzeqzpdaaymxhae.supabase.co"  # https://xxxx.supabase.co
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd5ZWxjZHplcXpwZGFheW14aGFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODMwMDY1MTcsImV4cCI6MjA5ODU4MjUxN30.xZ7avn_Crjx4Bos_IpI5oUCgsHIQgZm24IoieQz4OfA"      # anon public key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── Push data to Supabase ─────────────────────────────────
def push_videos():
    print("Fetching video data...")
    df = fetch_all_videos()

    # Convert DataFrame to list of dicts
    records = []
    for _, row in df.iterrows():
        records.append({
            "video_id"    : row["video_id"],
            "title"       : row["title"],
            "published_at": row["published_at"].isoformat(),
            "views"       : int(row["views"]),
            "likes"       : int(row["likes"]),
            "comments"    : int(row["comments"]),
            "thumbnail"   : row["thumbnail"]
        })

    print(f"Pushing {len(records)} videos to Supabase...")

    # Upsert — updates if video_id exists, inserts if new
    result = supabase.table("youtube_videos").upsert(records).execute()

    print(f"✅ Done! {len(result.data)} rows pushed to Supabase.")
    return result

# ── Run ───────────────────────────────────────────────────
if __name__ == "__main__":

    push_videos()