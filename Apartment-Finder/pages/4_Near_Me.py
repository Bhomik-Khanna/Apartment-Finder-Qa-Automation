

import streamlit as st
from theme import apply_theme, load_tracker, get_colors, score_color_class, listing_links_html # type: ignore
from distance_api import get_commute_minutes

st.set_page_config(
    page_title="Near Me — Apartment Finder",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
tracker = load_tracker()
c = get_colors()

# ── Sidebar nav ────────────────────────────────────────────────────────────────
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
    st.page_link("pages/8_Settings.py", label=" Settings")
    st.markdown("---")

    st.markdown(f"""<div style="font-size:0.75rem;font-weight:600;
    color:{c['text']};margin-bottom:8px">🔍 Filters</div>""",
    unsafe_allow_html=True)
    max_rent     = st.slider("Max rent (₹)", 0, 80000, 80000, step=1000)
    min_bedrooms = st.selectbox("Min bedrooms", [0, 1, 2, 3], index=0)
    max_commute  = st.slider("Max commute (min)", 0, 120, 120, step=5)

    st.markdown("---")
    st.markdown(f"""<div style="font-size:0.75rem;font-weight:600;
    color:{c['text']};margin-bottom:8px">🎛 Score weights</div>""",
    unsafe_allow_html=True)
    rent_weight    = float(st.slider("Rent priority", 0.1, 0.9, 0.4, 0.1,
                               help="Lower = commute matters more on this page"))
    commute_weight = round(1.0 - rent_weight, 1)
    c1, c2 = st.columns(2)
    c1.caption(f" **{int(rent_weight*100)}%**")
    c2.caption(f" **{int(commute_weight*100)}%**")

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">Near <span class="hero-accent">Me</span></div>
  <p class="hero-sub">Enter your location — we'll rank every apartment by commute time from there</p>
</div>
""", unsafe_allow_html=True)

# ── Location input ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Your location</div>', unsafe_allow_html=True)

col_input, col_btn = st.columns([0.78, 0.22])
with col_input:
    user_location = st.text_input(
        "Your current address",
        placeholder="e.g. Sector 15, Faridabad, Haryana",
        label_visibility="collapsed",
    )
with col_btn:
    search_clicked = st.button(
        "🔍  Find apartments",
        use_container_width=True,
        type="primary",
    )


st.markdown(f"""
<div class="info-card" style="margin-bottom:1rem">
  <div class="info-title"> Areas we have apartment data for</div>
  <div class="info-body">
    We currently have listings across these areas in <b>Gurgaon</b> and
    <b>Faridabad</b>. Enter any address below — your college, workplace,
    or home — and we'll show you how long it takes to commute to apartments
    in each of these areas.<br><br>
    <b>Gurgaon:</b> Sector 44 · Sector 45 · Sector 46 · Sector 47 · Sector 48<br>
    <b>Faridabad:</b> Old Faridabad · NIT Faridabad · Sector 15 · Sector 21 · Badkhal · Ballabhgarh<br><br>
    <span style="color:{c['muted']}">
    💡 Tip: Be specific with your address — include area, city, and state
    (e.g. "Sector 15, Faridabad, Haryana") for accurate results.
    </span>
  </div>
</div>
""", unsafe_allow_html=True)


st.markdown(f"""
<div style="font-size:0.72rem;font-weight:600;color:{c['muted']};
text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px">
  Or choose a common starting point
</div>
""", unsafe_allow_html=True)

quick_locations = {
    " NIT Faridabad":     "NIT Faridabad, Faridabad, Haryana",
    " Faridabad Stn":     "Faridabad Railway Station, Faridabad, Haryana",
    " Sector 15 Fbd":    "Sector 15 Market, Faridabad, Haryana",
    " Cyber City":        "Cyber City, Gurugram, Haryana",
    " Connaught Place":  "Connaught Place, New Delhi",
    " Huda City Centre":  "Huda City Centre, Gurugram, Haryana",
}

q_cols = st.columns(len(quick_locations))
for i, (label, address) in enumerate(quick_locations.items()):
    if q_cols[i].button(label, key=f"quick_{i}", use_container_width=True):
        st.session_state["near_me_location"] = address
        st.session_state["near_me_label"] = label
        st.rerun()

if "near_me_location" in st.session_state and not user_location:
    user_location = st.session_state["near_me_location"]
    st.markdown(f"""
    <div style="font-size:0.8rem;color:{c['accent']};
    margin:6px 0 0;padding:6px 10px;background:{c['accent_bg']};
    border-radius:6px;display:inline-block">
        📍 Searching from: <b>{st.session_state.get('near_me_label', user_location)}</b>
        — <a href="#" style="color:{c['muted']}">change</a>
    </div>
    """, unsafe_allow_html=True)


if not user_location and not search_clicked:
    st.markdown(f"""
    <div class="info-card">
        <div class="info-title"> How commute scoring works</div>
        <div class="info-body">
            Once you enter your location, we call the OpenRouteService API to
            calculate real driving time from your address to every apartment
            in our dataset — <b>{len(tracker)} apartments</b> across Gurgaon
            and Faridabad.<br><br>
            Results are scored using:<br>
            <b>Match score</b> = (rent score × rent weight) + (commute score × commute weight)<br><br>
            On this page the default is 40% rent / 60% commute, since you're
            specifically looking for what's closest to you. Adjust in the sidebar.
            <br><br>
            <span style="color:{c['muted']}">
            ⏱ Fetching takes 20-40 seconds for the full dataset.
            Results are cached so filters update instantly after the first search.
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


if user_location:
    cache_key = f"near_me_results_{user_location}"

    if cache_key not in st.session_state:
        results = []
        progress = st.progress(0, text="Fetching commute times...")
        for i, apt in enumerate(tracker.apartments):
            commute = get_commute_minutes(user_location, apt.address)
            results.append((apt, commute))
            progress.progress(
                (i + 1) / len(tracker.apartments),
                text=f"Checked {i+1}/{len(tracker.apartments)}: {apt.name}"
            )
        progress.empty()
        st.session_state[cache_key] = results
        
        # Safe string check to avoid 'startswith' on int error
        for key in list(st.session_state.keys()):
            if isinstance(key, str) and key.startswith("near_me_results_") and key != cache_key:
                del st.session_state[key]

    results = st.session_state[cache_key]


    filtered = [
        (apt, commute) for apt, commute in results
        if apt.rent <= max_rent
        and apt.bedrooms >= min_bedrooms
        and commute is not None
        and commute <= max_commute
    ]

    def live_score(apt, commute):
        if commute is None:
            return 0.0
        rent_s    = max(0.0, min(1.0, 1.0 - apt.rent / (max_rent or 80000)))
        commute_s = max(0.0, min(1.0, 1.0 - commute / (max_commute or 120)))
        return round((rent_s * rent_weight + commute_s * commute_weight) * 100, 1)

    ranked = sorted(filtered, key=lambda x: live_score(x[0], x[1]), reverse=True)

    
    valid_commutes = [comm for _, comm in ranked if comm is not None]
    best_score  = live_score(ranked[0][0], ranked[0][1]) if ranked else 0
    med_commute = sorted(valid_commutes)[len(valid_commutes)//2] if valid_commutes else "—"
    avg_rent    = int(sum(a.rent for a, _ in ranked) / len(ranked)) if ranked else 0

    st.markdown(f"""
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Matches found</div>
        <div class="stat-val">{len(ranked)} <span class="stat-unit">/ {len(tracker)}</span></div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Best match</div>
        <div class="stat-val">{best_score}<span class="stat-unit">%</span></div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Median commute</div>
        <div class="stat-val">{med_commute}<span class="stat-unit"> min</span></div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Avg rent</div>
        <div class="stat-val">₹{avg_rent:,}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not ranked:
        st.markdown("""<div class="empty">
            <div class="empty-ico">🔍</div>
            <div class="empty-ttl">No matches from this location</div>
            <div class="empty-sub">Try loosening the rent or commute filters,
            or make your address more specific (include city and state).</div>
        </div>""", unsafe_allow_html=True)
        st.stop()

    st.markdown(
        f'<div class="section-label">Ranked from: {user_location}</div>',
        unsafe_allow_html=True
    )

    for i, (apt, commute) in enumerate(ranked):
        score = live_score(apt, commute)
        sc    = score_color_class(score)
        rc    = "rank-top" if i < 3 else ""
        top   = "apt-card-top" if i < 3 else ""
        comm  = f"{commute} min" if commute is not None else "N/A"
        note  = f'<div class="apt-notes">📝 {apt.notes}</div>' if apt.notes else ""
        links = listing_links_html(apt, c)

        st.markdown(f"""
        <div class="apt-card {top}">
          <div class="rank-badge {rc}">#{i+1}</div>
          <div class="apt-body">
            <div class="apt-name">{apt.name}</div>
            <div class="apt-addr">📍 {apt.address}</div>
            <div class="tags">
              <span class="tag t-rent">₹{apt.rent:,}/mo</span>
              <span class="tag t-commute">🚗 {comm}</span>
              <span class="tag t-beds">🛏 {apt.bedrooms} BHK</span>
            </div>
            {note}
            {links}
          </div>
          <div class="score-col">
            <div class="score-num {sc}">{score}</div>
            <div class="score-lbl">match</div>
          </div>
        </div>
        """, unsafe_allow_html=True)