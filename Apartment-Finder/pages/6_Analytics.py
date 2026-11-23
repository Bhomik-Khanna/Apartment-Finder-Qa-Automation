

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import pandas as pd
from theme import apply_theme, get_colors
from storage import load_feedback

st.set_page_config(
    page_title="Analytics — Apartment Finder",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
c = get_colors()

with st.sidebar:
    st.markdown(f"""<div style="font-size:0.65rem;font-weight:700;color:{c['muted']};
    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px">Pages</div>""",
    unsafe_allow_html=True)
    st.page_link("pages/3_About.py",        label="  About")
    st.page_link("app.py",                  label="  Home")
    st.page_link("pages/1_Compare.py",      label="  Compare")
    st.page_link("pages/2_Manage.py",       label="  Manage")
    st.page_link("pages/4_Near_Me.py",      label="  Near Me")
    st.page_link("pages/5_AI_Assistant.py", label="  AI Assistant")
    st.page_link("pages/6_Analytics.py",    label="  Analytics")
    st.page_link("pages/7_Admin.py",        label="  Admin")
    st.page_link("pages/8_Settings.py",     label="  Settings")


st.markdown("""
<div class="hero">
  <div class="hero-title">Feedback <span class="hero-accent">Analytics</span></div>
  <p class="hero-sub">What users think — ratings, reviews, and suggestions collected by the AI assistant</p>
</div>
""", unsafe_allow_html=True)


feedback = load_feedback()

if not feedback:
    st.markdown(f"""
    <div class="empty">
        <div class="empty-ico">📭</div>
        <div class="empty-ttl">No feedback yet</div>
        <div class="empty-sub">
            Feedback is collected automatically by the AI Assistant when users
            rate their experience. Go to the AI Assistant page and have a
            conversation — the assistant will ask for feedback naturally.
        </div>
    </div>
    <div class="info-card" style="margin-top:1rem">
        <div class="info-title"> How feedback gets collected</div>
        <div class="info-body">
            The AI Assistant collects ratings and suggestions naturally during
            conversations. When a user seems satisfied, the assistant asks:<br><br>
            <i>"How would you rate your experience today? (1-5 stars)"</i><br>
            <i>"Any suggestions for improvement?"</i><br><br>
            Responses are saved automatically to the SQLite database and
            appear here once submitted.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


df = pd.DataFrame(feedback)
df["created_at"] = pd.to_datetime(df["created_at"])
df["date"]       = df["created_at"].dt.date
df["rating"]     = pd.to_numeric(df["rating"], errors="coerce").fillna(0).astype(int)


avg_rating   = round(df["rating"].mean(), 1)
total        = len(df)
five_stars   = len(df[df["rating"] == 5])
pct_positive = round((len(df[df["rating"] >= 4]) / total) * 100) if total > 0 else 0

st.markdown(f"""
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-label">Total responses</div>
    <div class="stat-val">{total}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Average rating</div>
    <div class="stat-val">{avg_rating} <span class="stat-unit">/ 5</span></div>
  </div>
  <div class="stat-card">
    <div class="stat-label">5-star reviews</div>
    <div class="stat-val">{five_stars}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Positive (4-5 stars)</div>
    <div class="stat-val">{pct_positive}<span class="stat-unit">%</span></div>
  </div>
</div>
""", unsafe_allow_html=True)


is_light   = st.session_state.get("theme") == "light"
bg         = "#ffffff" if is_light else "#0f1320"
text_color = "#0f172a" if is_light else "#e5e7eb"
grid_color = "#e2e8f0" if is_light else "#1a2035"
bar_colors = {1: "#ef4444", 2: "#f97316", 3: "#f59e0b", 4: "#10b981", 5: "#3b82f6"}

st.markdown('<div class="section-label" style="margin-top:1rem">Rating breakdown</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)


with col1:
    rating_counts = df["rating"].value_counts().sort_index()
    all_ratings   = {r: int(rating_counts.get(r, 0)) for r in range(1, 6)}

    fig, ax = plt.subplots(figsize=(5, 3.5))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    
    vals_list = list(all_ratings.values())
    bars = ax.bar(
        [f"{r}⭐" for r in all_ratings.keys()],
        vals_list,
        color=[bar_colors[r] for r in all_ratings.keys()],
        edgecolor=bg, linewidth=0.8, zorder=3,
    )
    for bar, val in zip(bars, vals_list):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                    str(val), ha="center", va="bottom",
                    color=text_color, fontsize=9, fontweight="bold")

    ax.set_xlabel("Rating", color=text_color, fontsize=9)
    ax.set_ylabel("Count", color=text_color, fontsize=9)
    ax.set_title("Ratings distribution", color=text_color, fontsize=9, fontweight="bold")
    for spine in ax.spines.values():
        spine.set_edgecolor(grid_color)
    ax.tick_params(colors=text_color, labelsize=8)
    ax.grid(axis="y", color=grid_color, linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


with col2:
    if len(df["date"].unique()) > 1:
        daily_avg = df.groupby("date")["rating"].mean().reset_index()

        fig2, ax2 = plt.subplots(figsize=(5, 3.5))
        fig2.patch.set_facecolor(bg)
        ax2.set_facecolor(bg)

        ax2.plot(daily_avg["date"], daily_avg["rating"],
                 color=c["accent"], linewidth=2, marker="o",
                 markersize=5, zorder=3)
        ax2.fill_between(daily_avg["date"], daily_avg["rating"],
                         alpha=0.15, color=c["accent"])
        ax2.set_ylim(0, 5.5)
        ax2.set_xlabel("Date", color=text_color, fontsize=9)
        ax2.set_ylabel("Avg rating", color=text_color, fontsize=9)
        ax2.set_title("Rating trend over time", color=text_color,
                      fontsize=9, fontweight="bold")
        for spine in ax2.spines.values():
            spine.set_edgecolor(grid_color)
        ax2.tick_params(colors=text_color, labelsize=7)
        ax2.grid(color=grid_color, linewidth=0.5, zorder=0)
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)
    else:
        st.markdown(f"""
        <div class="info-card" style="height:200px;display:flex;
        align-items:center;justify-content:center;text-align:center">
            <div>
                <div style="font-size:1.5rem;margin-bottom:8px">📈</div>
                <div class="info-title">Trend chart available soon</div>
                <div class="info-body">Collect feedback on more than one day
                to see the rating trend over time.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


st.markdown('<div class="section-label" style="margin-top:1.5rem">Recent reviews</div>',
            unsafe_allow_html=True)

recent = df.sort_values("created_at", ascending=False).head(10)

for _, row in recent.iterrows():
    rating  = int(row["rating"])
    stars   = "⭐" * rating + "☆" * (5 - rating)
    review  = row.get("review", "") or "No review text"
    suggest = row.get("suggestions", "") or ""
    date    = row["created_at"].strftime("%d %b %Y, %I:%M %p")
    score_c = c["green"] if rating >= 4 else c["amber"] if rating == 3 else c["red"]

    st.markdown(f"""
    <div class="info-card" style="margin-bottom:10px">
        <div style="display:flex;justify-content:space-between;
        align-items:center;margin-bottom:6px">
            <div style="font-size:1rem;color:{score_c}">{stars}</div>
            <div style="font-size:0.72rem;color:{c['muted']}">{date}</div>
        </div>
        <div class="info-body" style="margin-bottom:{"6px" if suggest else "0"}">
            {review}
        </div>
        {f'<div style="font-size:0.78rem;color:{c["muted"]};margin-top:6px">💡 Suggestion: {suggest}</div>' if suggest else ""}
    </div>
    """, unsafe_allow_html=True)


suggestions = df[df["suggestions"].str.strip().str.len() > 0]["suggestions"].tolist()
if suggestions:
    st.markdown('<div class="section-label" style="margin-top:1.5rem">All suggestions</div>',
                unsafe_allow_html=True)
    for i, sug in enumerate(suggestions, 1):
        st.markdown(f"""
        <div style="padding:8px 14px;background:{c['surface']};
        border:1px solid {c['border']};border-radius:8px;
        margin-bottom:6px;font-size:0.83rem;color:{c['text2']}">
            {i}. {sug}
        </div>
        """, unsafe_allow_html=True)


with st.expander(" View raw feedback data"):
    display_df = df[["rating", "review", "suggestions", "created_at"]].copy()
    display_df.columns = ["Rating", "Review", "Suggestions", "Submitted At"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)