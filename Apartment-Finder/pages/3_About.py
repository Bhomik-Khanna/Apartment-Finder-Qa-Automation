


import streamlit as st
from theme import apply_theme, get_colors

st.set_page_config(
    page_title="About — Apartment Finder",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
c = get_colors()
with st.sidebar:
    st.markdown(f"""<div style="font-size:0.65rem;font-weight:700;color:{c['muted']};
    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px">Pages</div>""",
    unsafe_allow_html=True)
    try:
        st.page_link("pages/3_About.py",        label="  About")
        st.page_link("app.py",                  label="  Home")
        st.page_link("pages/1_Compare.py",      label="  Compare")
        st.page_link("pages/2_Manage.py",       label="  Manage")
        st.page_link("pages/4_Near_Me.py",      label="  Near Me")
        st.page_link("pages/5_AI_Assistant.py", label="  AI Assistant")
        st.page_link("pages/6_Analytics.py",    label="  Analytics")
        st.page_link("pages/7_Admin.py",        label="  Admin")
        st.page_link("pages/8_Settings.py",     label="  Settings")
    except Exception:
        pass

st.markdown("""
<div class="hero">
  <div class="hero-title">How it <span class="hero-accent">Works</span></div>
  <p class="hero-sub">The scoring logic, data sources, and tech stack explained</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
  <div class="info-title"> What this tool does</div>
  <div class="info-body">
    Apartment Finder helps you compare and rank rental apartments in the NCR region
    (Gurgaon and Faridabad) based on two factors that actually matter: how much it costs,
    and how long it takes to get to your college or workplace from there.<br><br>
    Each apartment gets a <b>Match score from 0–100</b> based on your own priorities.
    You control how much rent vs commute matters to you using the slider on the home page.
  </div>
</div>

<div class="info-card">
  <div class="info-title"> How the score is calculated</div>
  <div class="info-body">
    The scoring formula has two components:<br><br>
    <b>Rent score</b> = 1 − (apartment rent ÷ max rent in your filters)<br>
    <b>Commute score</b> = 1 − (commute minutes ÷ max commute in your filters)<br><br>
    Both are normalized to a 0–1 scale so they can be fairly combined.
    Lower rent = higher rent score. Shorter commute = higher commute score.<br><br>
    <b>Final score</b> = (rent score × rent weight) + (commute score × commute weight)<br><br>
    Default weights are 60% rent, 40% commute — but you can drag the slider to
    change this to whatever fits your actual priorities.
  </div>
</div>

<div class="info-card">
  <div class="info-title"> Where commute times come from</div>
  <div class="info-body">
    Commute times are fetched automatically from the
    <b>OpenRouteService API</b> (free, open-source routing based on OpenStreetMap data)
    when you add a new apartment. The calculation is driving time from your
    origin address (Faridabad Railway Station by default) to the apartment's address.<br><br>
    <b>Important:</b> commute times are estimates based on road network data,
    not real-time traffic. They give a reliable relative comparison across apartments,
    but may differ slightly from Google Maps, which uses live traffic patterns.
  </div>
</div>

<div class="info-card">
  <div class="info-title"> Data source</div>
  <div class="info-body">
    Apartment listings were manually collected from public rental platforms
    (99acres, MagicBricks, NoBroker) for the Gurgaon and Faridabad areas.
    This approach was chosen deliberately over automated scraping, since
    rental sites actively block scrapers and the data can break unexpectedly —
    a stable, curated dataset produces more reliable comparisons than a fragile
    live scraper that might fail during a demo.
  </div>
</div>

<div class="info-card">
  <div class="info-title">🛠 Tech stack</div>
  <div class="info-body">
    <b>Language:</b> Python 3<br>
    <b>UI framework:</b> Streamlit<br>
    <b>Data handling:</b> pandas, JSON file storage<br>
    <b>Visualization:</b> matplotlib<br>
    <b>API integration:</b> OpenRouteService (geocoding + directions)<br>
    <b>Architecture:</b> OOP across 5 separated files
    (apartment.py, tracker.py, distance_api.py, storage.py, theme.py)<br><br>
    Each file has one responsibility. The UI (app.py) imports from the logic
    files but the logic files don't know the UI exists —
    clean separation of concerns throughout.
  </div>
</div>
""", unsafe_allow_html=True)