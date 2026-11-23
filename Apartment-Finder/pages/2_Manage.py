"""
Add and delete apartments
"""

import streamlit as st
from theme import apply_theme, load_tracker, get_colors, ORIGIN_ADDRESS
from apartment import Apartment
from distance_api import get_commute_minutes
from storage import save_to_file, apartment_exists

st.set_page_config(
    page_title="Manage — Apartment Finder",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
tracker = load_tracker()
c = get_colors()
with st.sidebar:
    st.markdown(f"""<div style="font-size:0.65rem;font-weight:700;color:{c['muted']};
    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px">Pages</div>""",
    unsafe_allow_html=True)
    st.page_link("pages/3_About.py",   label="  About")
    st.page_link("app.py",             label="  Home")
    st.page_link("pages/1_Compare.py", label="  Compare")
    st.page_link("pages/2_Manage.py",  label="  Manage")
    st.page_link("pages/4_Near_Me.py", label="  Near Me")
    st.page_link("pages/5_AI_Assistant.py", label="  AI Assistant")
    st.page_link("pages/6_Analytics.py", label=" Analytics")
    st.page_link("pages/7_Admin.py",        label="  Admin")
    st.page_link("pages/8_Settings.py", label="Settings")

st.markdown("""
<div class="hero">
  <div class="hero-title">Manage <span class="hero-accent">Listings</span></div>
  <p class="hero-sub">Add new apartments or remove existing ones</p>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="section-label">Add apartment</div>', unsafe_allow_html=True)

with st.form("add_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name    = st.text_input("Name / Society", placeholder="Unitech Greenwood 2BHK")
        address = st.text_input("Address", placeholder="Sector 45, Gurgaon, Haryana")
        notes   = st.text_area("Notes (optional)", height=80)
    with col2:
        rent     = st.number_input("Monthly rent (₹)", min_value=0, step=500)
        bedrooms = st.number_input("Bedrooms", min_value=0, step=1)
        st.markdown(f"""
        <div class="info-card" style="margin-top:8px">
          <div class="info-title">📍 Origin address</div>
          <div class="info-body">{ORIGIN_ADDRESS}<br><br>
          Commute time is calculated automatically from this address when you add a listing.
          </div>
        </div>
        """, unsafe_allow_html=True)
    submitted = st.form_submit_button("Add and score →", use_container_width=True)

if submitted:
    if not name or not address:
        st.error("Name and address are required.")
    elif len(name.strip()) < 3:
        st.error("Name must be at least 3 characters.")
    elif rent <= 0:
        st.error("Rent must be greater than 0.")
    elif bedrooms <= 0:
        st.error("Bedrooms must be at least 1.")
    elif apartment_exists(name.strip(), address.strip()):
        st.warning(f"'{name}' at '{address}' already exists in the database. No duplicate added.")
    else:
        with st.spinner("Fetching commute time from API..."):
            commute = get_commute_minutes(ORIGIN_ADDRESS, address)
        apt = Apartment(name.strip(), address.strip(), int(rent), int(bedrooms), notes, commute)
        tracker.add_apartment(apt)
        save_to_file(tracker.apartments)
        if commute is None:
            st.warning(f"Added '{name}' — but couldn't get commute time. Check your API key or try a more specific address.")
        else:
            st.success(f"Added '{name}' ✓  Commute: {commute} min")


st.markdown('<div class="section-label" style="margin-top:1.5rem">All listings</div>',
            unsafe_allow_html=True)

if len(tracker) == 0:
    st.markdown("""<div class="empty">
        <div class="empty-ico">📭</div>
        <div class="empty-ttl">No apartments saved yet</div>
        <div class="empty-sub">Add one above, or run <code>seed_data.py</code> from the terminal.</div>
    </div>""", unsafe_allow_html=True)
else:
    st.caption(f"{len(tracker)} apartments in database · Listings can only be removed by an admin")
    for apt in tracker.apartments:
        comm = f"{apt.commute_minutes} min" if apt.commute_minutes is not None else "N/A"
        st.markdown(f"""
        <div class="apt-card" style="margin-bottom:6px">
          <div class="apt-body">
            <div class="apt-name">{apt.name}</div>
            <div class="apt-addr">📍 {apt.address}</div>
            <div class="tags">
              <span class="tag t-rent">₹{apt.rent:,}/mo</span>
              <span class="tag t-commute">🚗 {comm}</span>
              <span class="tag t-beds">🛏 {apt.bedrooms} BHK</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)