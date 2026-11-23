

import streamlit as st
import pandas as pd
import datetime
import os
from theme import apply_theme, get_colors, load_tracker
from storage import get_connection, load_feedback, load_from_file, save_to_file
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Admin — Apartment Finder",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
c = get_colors()

# ── Sidebar nav ────────────────────────────────────────────────────────────────
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
    st.markdown("---")
    st.markdown(f"""
    <div class="info-card" style="padding:10px 12px">
      <div class="info-title"> Admin only</div>
      <div class="info-body" style="font-size:0.75rem">
        Restricted access.<br>
        Set ADMIN_PASSWORD in .env to change the default password.
      </div>
    </div>
    """, unsafe_allow_html=True)

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

if "admin_authenticated" not in st.session_state:
    st.session_state["admin_authenticated"] = False

if not st.session_state["admin_authenticated"]:
    st.markdown("""
    <div class="hero">
      <div class="hero-title">Admin <span class="hero-accent">Panel</span></div>
      <p class="hero-sub">Restricted access — enter password to continue</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])
    with col2:
        st.markdown(f"""
        <div class="info-card" style="text-align:center;padding:28px 24px;margin-bottom:16px">
          <div style="font-size:2rem;margin-bottom:8px">🔐</div>
          <div class="info-title">Admin login</div>
          <div class="info-body">Enter your admin password below.</div>
        </div>
        """, unsafe_allow_html=True)
        password = st.text_input(
            "Password",
            type="password",
            key="admin_pw",
            placeholder="Enter admin password",
            label_visibility="collapsed",
        )
        if st.button("Login →", type="primary", use_container_width=True):
            if password == ADMIN_PASSWORD:
                st.session_state["admin_authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect password. Try again.")
        st.markdown(f"""
        <div style="font-size:0.72rem;color:{c['muted']};
        text-align:center;margin-top:10px;line-height:1.6">
            Default: <code>admin123</code><br>
            Set <code>ADMIN_PASSWORD</code> in your <code>.env</code> file to change it.
        </div>
        """, unsafe_allow_html=True)
    st.stop()


st.markdown("""
<div class="hero">
  <div class="hero-title">Admin <span class="hero-accent">Panel</span></div>
  <p class="hero-sub">Database management, feedback review, and data export</p>
</div>
""", unsafe_allow_html=True)

col_title, col_logout = st.columns([0.88, 0.12])
with col_logout:
    if st.button(" Logout", use_container_width=True):
        st.session_state["admin_authenticated"] = False
        st.rerun()


apartments   = load_from_file()
all_feedback = load_feedback()

avg_rating = round(
    sum(f["rating"] for f in all_feedback) / len(all_feedback), 1
) if all_feedback else 0


st.markdown(f"""
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-label">Total apartments</div>
    <div class="stat-val">{len(apartments)}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Feedback entries</div>
    <div class="stat-val">{len(all_feedback)}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Avg rating</div>
    <div class="stat-val">{avg_rating} <span class="stat-unit">/ 5</span></div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Database</div>
    <div class="stat-val" style="font-size:1rem;padding-top:4px">SQLite</div>
  </div>
</div>
""", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs([" Apartments", " Feedback", " Export"])


with tab1:
    st.markdown(f"""
    <div style="font-size:0.82rem;color:{c['muted']};margin-bottom:12px">
        {len(apartments)} apartments in database.
        Use the search to filter. Delete is admin-only.
    </div>
    """, unsafe_allow_html=True)

    search = st.text_input(
        "Search apartments",
        placeholder="Name or area...",
        key="admin_search",
        label_visibility="collapsed",
    )

    filtered_apts = [
        a for a in apartments
        if not search
        or search.lower() in a.name.lower()
        or search.lower() in a.address.lower()
    ]

    if not filtered_apts:
        st.markdown(f"""
        <div class="empty">
            <div class="empty-ico">🔍</div>
            <div class="empty-ttl">No matches for "{search}"</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for apt in filtered_apts:
            comm = f"{apt.commute_minutes} min" if apt.commute_minutes else "N/A"
            col_info, col_del = st.columns([0.9, 0.1])
            with col_info:
                st.markdown(f"""
                <div style="display:flex;gap:12px;align-items:center;
                padding:10px 14px;background:{c['surface']};
                border:1px solid {c['border']};border-radius:10px;
                margin-bottom:6px">
                  <div style="flex:1;min-width:0">
                    <div style="font-size:0.88rem;font-weight:600;
                    color:{c['text']};margin-bottom:2px">{apt.name}</div>
                    <div style="font-size:0.75rem;color:{c['muted']}">
                      📍 {apt.address}
                    </div>
                  </div>
                  <div style="font-size:0.78rem;color:{c['text2']};
                  white-space:nowrap">₹{apt.rent:,}</div>
                  <div style="font-size:0.78rem;color:{c['text2']};
                  white-space:nowrap">🚗 {comm}</div>
                  <div style="font-size:0.78rem;color:{c['text2']};
                  white-space:nowrap">🛏 {apt.bedrooms} BHK</div>
                </div>
                """, unsafe_allow_html=True)
            with col_del:
                if st.button("🗑", key=f"del_{apt.name}_{apt.address}",
                             help=f"Delete {apt.name}"):
                    conn = get_connection()
                    conn.execute(
                        "DELETE FROM apartments WHERE name=? AND address=?",
                        (apt.name, apt.address)
                    )
                    conn.commit()
                    conn.close()
                    if "tracker" in st.session_state:
                        del st.session_state["tracker"]
                    st.success(f"Deleted '{apt.name}'")
                    st.rerun()


with tab2:
    if not all_feedback:
        st.markdown("""
        <div class="empty">
            <div class="empty-ico">⭐</div>
            <div class="empty-ttl">No feedback yet</div>
            <div class="empty-sub">
                Feedback is collected anonymously by the AI Assistant
                when users rate their experience.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        df_fb = pd.DataFrame(all_feedback)
        df_fb["created_at"] = pd.to_datetime(df_fb["created_at"])
        df_fb = df_fb.sort_values("created_at", ascending=False)

        for _, row in df_fb.iterrows():
            rating  = int(row.get("rating", 0))
            stars   = "⭐" * rating + "☆" * (5 - rating)
            review  = row.get("review", "") or "—"
            suggest = row.get("suggestions", "") or "—"
            date    = row["created_at"].strftime("%d %b %Y, %I:%M %p")
            score_c = (c["green"] if rating >= 4
                       else c["amber"] if rating == 3
                       else c["red"])

            st.markdown(f"""
            <div class="info-card" style="margin-bottom:10px">
              <div style="display:flex;justify-content:space-between;
              align-items:center;margin-bottom:8px">
                <div style="color:{score_c};font-size:1rem">{stars}</div>
                <div style="font-size:0.72rem;color:{c['muted']}">{date}</div>
              </div>
              <div style="font-size:0.82rem;color:{c['text2']};
              margin-bottom:4px"><b>Review:</b> {review}</div>
              <div style="font-size:0.82rem;color:{c['muted']}">
                <b>Suggestion:</b> {suggest}
              </div>
            </div>
            """, unsafe_allow_html=True)


with tab3:
    st.markdown(f"""
    <div style="font-size:0.85rem;color:{c['text2']};margin-bottom:16px">
        Download your data as CSV for analysis, backup, or reporting.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if apartments:
            apt_data = [{
                "Name":             a.name,
                "Address":          a.address,
                "Rent":             a.rent,
                "Bedrooms":         a.bedrooms,
                "Commute (min)":    a.commute_minutes,
                "Notes":            a.notes,
            } for a in apartments]
            csv_apt = pd.DataFrame(apt_data).to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download apartments CSV",
                csv_apt,
                file_name=f"apartments_{datetime.date.today()}.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary",
            )
            st.caption(f"{len(apartments)} apartments")
        else:
            st.button("📥 Download apartments CSV",
                      disabled=True, use_container_width=True)

    with col2:
        if all_feedback:
            csv_fb = pd.DataFrame(all_feedback).to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download feedback CSV",
                csv_fb,
                file_name=f"feedback_{datetime.date.today()}.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary",
            )
            st.caption(f"{len(all_feedback)} feedback entries")
        else:
            st.button("📥 Download feedback CSV",
                      disabled=True, use_container_width=True)
            st.caption("No feedback collected yet")