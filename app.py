import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from groq import Groq
from auth import (
    get_auth_url, exchange_code_for_token,
    get_youtube_client, get_user_info,
    get_channel_info, get_all_videos, get_video_stats
)
from search_engine import semantic_search
import os

try:
    GROQ_KEY = st.secrets["GROQ_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    GROQ_KEY = os.getenv("GROQ_KEY")

groq_client = Groq(api_key=GROQ_KEY)

st.set_page_config(
    page_title="PulseBoard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; background: #00000f !important; color: #cbd5e1; }
.stApp { background: #00000f !important; overflow-x: hidden; }
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(99,102,241,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.03) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
}
.main .block-container { position: relative; z-index: 2; padding-top: 1rem !important; max-width: 1400px !important; }
.hero-wrap { text-align: center; padding: 2.5rem 0 1rem; position: relative; }
.hero-ring {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 500px; height: 160px; border-radius: 50%;
    background: radial-gradient(ellipse, rgba(139,92,246,0.18) 0%, transparent 70%);
    animation: ring-pulse 4s ease-in-out infinite; pointer-events: none;
}
@keyframes ring-pulse {
    0%, 100% { transform: translate(-50%,-50%) scale(1); opacity: 0.6; }
    50% { transform: translate(-50%,-50%) scale(1.15); opacity: 1; }
}
.hero-eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; letter-spacing: 0.4em; color: #8b5cf6; text-transform: uppercase; margin-bottom: 0.8rem; }
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 900; line-height: 1; letter-spacing: 0.12em;
    background: linear-gradient(135deg, #c4b5fd 0%, #8b5cf6 35%, #06b6d4 70%, #c4b5fd 100%);
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    animation: shimmer 4s linear infinite;
}
@keyframes shimmer { 0% { background-position: 0% center; } 100% { background-position: 200% center; } }
.hero-sub { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #334155; letter-spacing: 0.2em; text-transform: uppercase; margin-top: 0.8rem; }
.login-card {
    background: linear-gradient(135deg, #080814 0%, #0d0d1a 100%);
    border: 1px solid #1a1a35; border-radius: 20px; padding: 3rem;
    text-align: center; max-width: 480px; margin: 2rem auto;
    position: relative; overflow: hidden;
}
.login-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #6366f1, #a855f7, #38bdf8); }
.login-desc { color: #4f5d7a; font-size: 0.88rem; line-height: 1.7; margin-bottom: 2rem; }
.metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1.5rem 0; }
.m-card {
    position: relative; background: #080814; border: 1px solid #1a1a35;
    border-radius: 18px; padding: 1.5rem 1.2rem; text-align: center; overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.m-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, #8b5cf6, #06b6d4, transparent);
    animation: border-flow 3s linear infinite; background-size: 200% auto;
}
@keyframes border-flow { 0% { background-position: 0% center; } 100% { background-position: 200% center; } }
.m-card:hover { border-color: #8b5cf6; transform: translateY(-6px) scale(1.02); box-shadow: 0 0 0 1px rgba(139,92,246,0.3), 0 20px 60px rgba(139,92,246,0.15); }
.m-icon { font-size: 1.6rem; margin-bottom: 0.5rem; display: block; }
.m-label { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 0.2em; text-transform: uppercase; color: #334155; margin-bottom: 0.6rem; }
.m-value { font-family: 'Orbitron', monospace; font-size: 1.8rem; font-weight: 700; background: linear-gradient(135deg, #c4b5fd, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1; }
.m-card:nth-child(2) .m-value { background: linear-gradient(135deg, #67e8f9, #06b6d4); -webkit-background-clip: text; background-clip: text; }
.m-card:nth-child(3) .m-value { background: linear-gradient(135deg, #86efac, #22c55e); -webkit-background-clip: text; background-clip: text; }
.m-card:nth-child(4) .m-value { background: linear-gradient(135deg, #fda4af, #f43f5e); -webkit-background-clip: text; background-clip: text; }
.sec-head { display: flex; align-items: center; gap: 0.75rem; margin: 2.2rem 0 1.2rem; }
.sec-head-text { font-family: 'Orbitron', monospace; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.25em; text-transform: uppercase; color: #8b5cf6; white-space: nowrap; }
.sec-head-line { flex: 1; height: 1px; background: linear-gradient(90deg, #1a1a35, transparent); }
.sec-head-dot { width: 6px; height: 6px; border-radius: 50%; background: #8b5cf6; box-shadow: 0 0 8px #8b5cf6; animation: dot-blink 2s ease-in-out infinite; }
@keyframes dot-blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
.neon-divider { height: 1px; background: linear-gradient(90deg, transparent, #1a1a35, #8b5cf6, #1a1a35, transparent); margin: 1.5rem 0; position: relative; }
.neon-divider::after { content: ''; position: absolute; top: -1px; left: 50%; transform: translateX(-50%); width: 60px; height: 3px; background: linear-gradient(90deg, #8b5cf6, #06b6d4); border-radius: 2px; filter: blur(2px); }
.user-badge { display: inline-flex; align-items: center; gap: 0.6rem; background: #080814; border: 1px solid #1a1a35; border-radius: 12px; padding: 0.6rem 1.2rem; color: #64748b; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; margin-bottom: 1rem; }
.v-title { font-family: 'Inter', sans-serif; color: #e2e8f0; font-size: 0.95rem; font-weight: 600; line-height: 1.5; margin-bottom: 0.7rem; }
.pill { display: inline-flex; align-items: center; gap: 0.25rem; background: rgba(139,92,246,0.07); border: 1px solid rgba(139,92,246,0.12); color: #64748b; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; padding: 0.25rem 0.65rem; border-radius: 20px; margin: 0.15rem; }
.match-pill { display: inline-flex; align-items: center; gap: 0.3rem; background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(6,182,212,0.15)); border: 1px solid rgba(139,92,246,0.25); color: #a78bfa; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; font-weight: 600; padding: 0.3rem 0.8rem; border-radius: 20px; margin-top: 0.6rem; }
.stTextInput > div > div > input { background: #080814 !important; border: 1px solid #1a1a35 !important; border-radius: 14px !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif !important; font-size: 0.9rem !important; padding: 0.9rem 1.3rem !important; caret-color: #8b5cf6 !important; }
.stTextInput > div > div > input:focus { border-color: #8b5cf6 !important; box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important; }
.stTextInput > div > div > input::placeholder { color: #1e293b !important; }
.stButton > button { background: linear-gradient(135deg, #3730a3, #7c3aed) !important; color: #e2e8f0 !important; border: 1px solid rgba(139,92,246,0.3) !important; border-radius: 10px !important; font-family: 'JetBrains Mono', monospace !important; font-weight: 500 !important; font-size: 0.78rem !important; padding: 0.5rem 1.2rem !important; transition: all 0.3s ease !important; }
.stButton > button:hover { box-shadow: 0 0 25px rgba(139,92,246,0.5) !important; transform: translateY(-2px) !important; }
hr { border: none !important; border-top: 1px solid #1a1a35 !important; margin: 1.5rem 0 !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #00000f; }
::-webkit-scrollbar-thumb { background: #1a1a35; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #8b5cf6; }
</style>
""", unsafe_allow_html=True)

def check_clickbait(title, thumbnail_url):
    try:
        result = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"""You are a YouTube clickbait detector.
Video Title: "{title}"
Thumbnail URL: {thumbnail_url}
Based on the video title alone, determine:
1. Does the title seem sensational, exaggerated, or misleading?
2. Is this genuine content or clickbait?
Reply in this exact format:
VERDICT: Genuine OR Clickbait
REASON: One sentence explaining why."""}],
            max_tokens=100
        )
        text    = result.choices[0].message.content.strip()
        verdict = "Unknown"
        reason  = "No reason returned."
        for line in text.split("\n"):
            if line.startswith("VERDICT:"):
                verdict = line.replace("VERDICT:", "").strip()
            elif line.startswith("REASON:"):
                reason = line.replace("REASON:", "").strip()
        return verdict, reason
    except Exception as e:
        return "Unknown", str(e)

def handle_oauth_callback():
    query_params = st.query_params
    if "code" in query_params and "logged_in" not in st.session_state:
        try:
            code        = query_params["code"]
            credentials = exchange_code_for_token(code)
            st.session_state["credentials"] = credentials
            st.session_state["logged_in"]   = True
            st.query_params.clear()
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")

def show_login():
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-ring"></div>
        <div class="hero-eyebrow">⚡ realtime analytics engine</div>
        <div class="hero-title">PULSEBOARD</div>
        <div class="hero-sub">// youtube intelligence dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="login-card">
            <div style="font-size:3rem; margin-bottom:1rem;">📊</div>
            <div style="font-family:'Orbitron',monospace; font-size:1.1rem; color:#8b5cf6; font-weight:700; margin-bottom:1rem; letter-spacing:0.05em;">
                Welcome to PulseBoard
            </div>
            <div class="login-desc">
                Connect your YouTube channel and get instant access to your
                analytics dashboard — views, likes, comments, smart search,
                and AI-powered clickbait detection.
            </div>
        </div>
        """, unsafe_allow_html=True)

        auth_url = get_auth_url()
        st.markdown(f"""
        <div style="text-align:center; margin-top:1rem;">
            <a href="{auth_url}" target="_self" style="
                display: inline-block;
                background: linear-gradient(135deg, #3730a3, #7c3aed);
                color: white; text-decoration: none;
                padding: 0.9rem 2.2rem; border-radius: 12px;
                font-family: 'JetBrains Mono', monospace;
                font-weight: 600; font-size: 0.88rem; letter-spacing: 0.05em;
                box-shadow: 0 0 40px rgba(139,92,246,0.35);
                border: 1px solid rgba(139,92,246,0.3);">
                🔐 Login with Google
            </a>
        </div>
        """, unsafe_allow_html=True)

def show_dashboard():
    credentials = st.session_state["credentials"]
    youtube     = get_youtube_client(credentials)

    if "channel_data" not in st.session_state:
        with st.spinner("Loading your channel data..."):
            user_info   = get_user_info(credentials)
            channel     = get_channel_info(youtube)
            if not channel:
                st.error("No YouTube channel found for this account.")
                return
            playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
            video_ids   = get_all_videos(youtube, playlist_id)
            df          = get_video_stats(youtube, video_ids)
            st.session_state["channel_data"] = channel
            st.session_state["user_info"]    = user_info
            st.session_state["df"]           = df

    channel   = st.session_state["channel_data"]
    user_info = st.session_state["user_info"]
    df        = st.session_state["df"]
    snippet   = channel.get("snippet", {})

    st.markdown(f"""
    <div class="hero-wrap">
        <div class="hero-ring"></div>
        <div class="hero-eyebrow">⚡ realtime analytics engine</div>
        <div class="hero-title">PULSEBOARD</div>
        <div class="hero-sub">// youtube intelligence dashboard</div>
    </div>
    <div style="text-align:center; margin-bottom:1rem;">
        <span class="user-badge">
            👤 {user_info.get('name', 'User')} &nbsp;•&nbsp;
            📺 {snippet.get('title', 'Your Channel')}
        </span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([4, 1, 1])
    with col3:
        if st.button("🚪 Logout"):
            for key in ["credentials", "logged_in", "channel_data", "user_info", "df"]:
                st.session_state.pop(key, None)
            st.rerun()

    if df.empty:
        st.warning("No videos found on your channel.")
        return

    st.markdown(f"""
    <div class="metric-row">
        <div class="m-card"><span class="m-icon">🎬</span><div class="m-label">Total Videos</div><div class="m-value">{len(df)}</div></div>
        <div class="m-card"><span class="m-icon">👁️</span><div class="m-label">Total Views</div><div class="m-value">{df['views'].sum():,}</div></div>
        <div class="m-card"><span class="m-icon">👍</span><div class="m-label">Total Likes</div><div class="m-value">{df['likes'].sum():,}</div></div>
        <div class="m-card"><span class="m-icon">📊</span><div class="m-label">Avg Views / Video</div><div class="m-value">{df['views'].mean():.1f}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
    st.markdown("""<div class="sec-head"><div class="sec-head-dot"></div><div class="sec-head-text">📈 Views Over Time</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)

    df_sorted = df.sort_values("published_at")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_sorted["published_at"], y=df_sorted["views"],
        marker=dict(color=df_sorted["views"], colorscale=[[0,"#1a1a35"],[0.4,"#4c1d95"],[0.7,"#8b5cf6"],[1,"#06b6d4"]], line=dict(width=0)),
        hovertemplate="<b>%{customdata}</b><br>Views: %{y:,}<extra></extra>",
        customdata=df_sorted["title"]
    ))
    fig.update_layout(
        plot_bgcolor="#00000f", paper_bgcolor="#00000f",
        font=dict(color="#334155", family="JetBrains Mono"), showlegend=False,
        xaxis=dict(showgrid=False, color="#1e293b", zeroline=False),
        yaxis=dict(gridcolor="#0d0d20", color="#1e293b", zeroline=False),
        margin=dict(l=0, r=0, t=10, b=0), height=260, bargap=0.25,
        hoverlabel=dict(bgcolor="#080814", bordercolor="#8b5cf6", font=dict(color="#e2e8f0", family="Inter"))
    )
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
    st.markdown("""<div class="sec-head"><div class="sec-head-dot"></div><div class="sec-head-text">🏆 Top 5 Videos by Views</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)

    top5 = df.nlargest(5, "views")[["title","views","likes","comments","published_at"]].copy()
    top5["published_at"] = top5["published_at"].dt.strftime("%Y-%m-%d")
    st.dataframe(top5, use_container_width=True, hide_index=True, column_config={
        "title": st.column_config.TextColumn("Title", width="large"),
        "views": st.column_config.NumberColumn("👁 Views"),
        "likes": st.column_config.NumberColumn("👍 Likes"),
        "comments": st.column_config.NumberColumn("💬 Comments"),
        "published_at": st.column_config.TextColumn("📅 Published"),
    })

    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
    st.markdown("""<div class="sec-head"><div class="sec-head-dot"></div><div class="sec-head-text">🔍 Semantic Search</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)

    search_query = st.text_input("", placeholder="⌕  Search by meaning — try 'funny fails' or 'haircut reaction'...")

    if search_query:
        with st.spinner("Scanning neural index..."):
            results = semantic_search(search_query, df)

        if results.empty:
            st.warning(f"No videos found matching '{search_query}'")
        else:
            st.success(f"⚡ {len(results)} result(s) found for '{search_query}'")
            st.markdown("<br>", unsafe_allow_html=True)

            for _, row in results.iterrows():
                match_pct = round(row["relevance"] * 100, 1)
                col1, col2 = st.columns([1, 3])
                with col1:
                    if row["thumbnail"]:
                        st.image(row["thumbnail"], use_container_width=True)
                with col2:
                    st.markdown(f"""
                    <div class="v-title">{row['title']}</div>
                    <span class="pill">👁 {row['views']:,}</span>
                    <span class="pill">👍 {row['likes']:,}</span>
                    <span class="pill">💬 {row['comments']:,}</span>
                    <span class="pill">📅 {row['published_at'].strftime('%Y-%m-%d')}</span>
                    <br><span class="match-pill">◈ Match Score: {match_pct}%</span>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🤖 Analyse Clickbait", key=row["video_id"]):
                        with st.spinner("Running AI analysis..."):
                            verdict, reason = check_clickbait(row["title"], row["thumbnail"])
                        if verdict.lower() == "genuine":
                            st.success(f"✅ Genuine — {reason}")
                        elif verdict.lower() == "clickbait":
                            st.error(f"⚠️ Clickbait — {reason}")
                        else:
                            st.warning(f"❓ {verdict} — {reason}")
                st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

    st.markdown("""<div class="sec-head"><div class="sec-head-dot"></div><div class="sec-head-text">📋 All Videos</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)

    display_df = df[["title","views","likes","comments","published_at"]].copy()
    display_df["published_at"] = display_df["published_at"].dt.strftime("%Y-%m-%d")
    st.dataframe(display_df, use_container_width=True, hide_index=True, column_config={
        "title": st.column_config.TextColumn("Title", width="large"),
        "views": st.column_config.NumberColumn("👁 Views"),
        "likes": st.column_config.NumberColumn("👍 Likes"),
        "comments": st.column_config.NumberColumn("💬 Comments"),
        "published_at": st.column_config.TextColumn("📅 Published"),
    })

handle_oauth_callback()

if st.session_state.get("logged_in"):
    show_dashboard()
else:
    show_login()