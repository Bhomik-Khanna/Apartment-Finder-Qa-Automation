

import streamlit as st
from theme import apply_theme, get_colors, ORIGIN_ADDRESS

st.set_page_config(
    page_title="Settings — Apartment Finder",
    page_icon="⚙️",
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
  <div class="hero-title">App <span class="hero-accent">Settings</span></div>
  <p class="hero-sub">Customize your experience</p>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="section-label">Appearance</div>', unsafe_allow_html=True)

current_theme = st.session_state.get("theme", "dark")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="info-card" style="cursor:pointer;
    border-color:{'#3b82f6' if current_theme == 'dark' else 'transparent'}">
        <div class="info-title"> Dark mode</div>
        <div class="info-body">Easy on the eyes, great for night use.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Use dark mode", use_container_width=True,
                 type="primary" if current_theme == "dark" else "secondary"):
        st.session_state["theme"] = "dark"
        st.rerun()

with col2:
    st.markdown(f"""
    <div class="info-card" style="cursor:pointer;
    border-color:{'#2563eb' if current_theme == 'light' else 'transparent'}">
        <div class="info-title"> Light mode</div>
        <div class="info-body">Clean and bright, great for daytime use.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Use light mode", use_container_width=True,
                 type="primary" if current_theme == "light" else "secondary"):
        st.session_state["theme"] = "light"
        st.rerun()


st.markdown('<div class="section-label" style="margin-top:1.5rem">Default scoring weights</div>',
            unsafe_allow_html=True)

st.markdown(f"""
<div class="info-card">
  <div class="info-body">
    These weights control how the match score is calculated on the Home page.
    Higher rent weight = cheaper apartments rank higher.
    Higher commute weight = shorter commutes rank higher.
  </div>
</div>
""", unsafe_allow_html=True)

default_rent = st.slider(
    "Default rent weight",
    min_value=0.1, max_value=0.9,
    value=st.session_state.get("default_rent_weight", 0.6),
    step=0.1,
    help="This becomes the default on the Home page"
)
if st.button("Save scoring defaults", type="primary"):
    st.session_state["default_rent_weight"] = default_rent
    st.session_state["default_commute_weight"] = round(1.0 - default_rent, 1)
    st.success(f"Saved — Home page will default to {int(default_rent*100)}% rent / {int((1-default_rent)*100)}% commute")


st.markdown('<div class="section-label" style="margin-top:1.5rem">Origin address</div>',
            unsafe_allow_html=True)

st.markdown(f"""
<div class="info-card">
  <div class="info-title">📍 Current origin address</div>
  <div class="info-body">
    <div style="font-size:1rem;font-weight:600;color:{c['accent']};
    margin-bottom:8px">{ORIGIN_ADDRESS}</div>
    This is the fixed address all default commute times are measured from.
    Every apartment's commute time on the Home page is the driving time
    from this address to that apartment's location.<br><br>
    <b>To change it:</b> update <code>ORIGIN_ADDRESS</code> in
    <code>theme.py</code>, then re-run <code>seed_data.py</code>
    to recalculate all commute times with the new origin.
  </div>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="section-label" style="margin-top:1.5rem">Session</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("🗑 Clear all session data", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key not in ["theme", "admin_authenticated"]:
                del st.session_state[key]
        st.success("Session cleared — cached data reset")
with col2:
    if st.button(" Reload apartments from database", use_container_width=True):
        if "tracker" in st.session_state:
            del st.session_state["tracker"]
        st.success("Apartments will reload on next page visit")