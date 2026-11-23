"""
Side-by-side apartment comparison
"""

import streamlit as st
from theme import apply_theme, load_tracker, get_colors, score_color_class

st.set_page_config(
    page_title="Compare — Apartment Finder",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
tracker = load_tracker()
c = get_colors()

st.markdown("""
<div class="hero">
  <div class="hero-title">Compare <span class="hero-accent">Apartments</span></div>
  <p class="hero-sub">Pick two or three to see them side by side</p>
</div>
""", unsafe_allow_html=True)

if len(tracker) < 2:
    st.markdown("""<div class="empty">
        <div class="empty-ico">⚖️</div>
        <div class="empty-ttl">Need at least 2 apartments</div>
        <div class="empty-sub">Go to Manage to add more listings first.</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

names = [a.name for a in tracker.apartments]

col1, col2, col3 = st.columns(3)
with col1:
    pick1 = st.selectbox("Apartment A", names, index=0, key="cmp1")
with col2:
    pick2 = st.selectbox("Apartment B", names, index=min(1, len(names)-1), key="cmp2")
with col3:
    options = ["None"] + names
    pick3 = st.selectbox("Apartment C (optional)", options, index=0, key="cmp3")

with st.sidebar:
    # Navigation
    c = get_colors()
    st.markdown(f"""<div style="font-size:0.65rem;font-weight:700;color:{c['muted']};
    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px">Pages</div>""",
    unsafe_allow_html=True)
    st.page_link("pages/3_About.py",   label="  About")
    st.page_link("app.py",             label="  Home")
    st.page_link("pages/1_Compare.py", label="  Compare")
    st.page_link("pages/2_Manage.py",  label="  Manage")
    st.page_link("pages/4_Near_Me.py", label="  Near Me")
    st.page_link("pages/5_AI_Assistant.py", label="  AI Assistant")
    st.page_link("pages/6_Analytics.py", label="  Analytics")
    st.page_link("pages/7_Admin.py",        label="  Admin")
    st.page_link("pages/8_Settings.py", label="  Settings")
    st.markdown("---")
    st.markdown("### 🎛 Scoring weights")
    rent_weight = float(st.slider("Rent priority", 0.1, 0.9, 0.6, 0.1,
                            help="Higher = rent matters more."))
    commute_weight = round(1.0 - rent_weight, 1)
    c1, c2 = st.columns(2)
    c1.caption(f"💰 **{int(rent_weight*100)}%**")
    c2.caption(f"🚗 **{int(commute_weight*100)}%**")

# Explicitly annotate type as list[str] to prevent Pylance inferring list[None]
selected_names: list[str] = [str(pick1), str(pick2)]
if pick3 and str(pick3) != "None":
    selected_names.append(str(pick3))

apts_ordered = []
for name in selected_names:
    for a in tracker.apartments:
        if a.name == name:
            apts_ordered.append(a)
            break

if len(apts_ordered) < 2:
    st.warning("Please select different apartments to compare.")
    st.stop()

scores = [
    a.score(rent_weight=rent_weight, commute_weight=commute_weight)
    for a in apts_ordered
]
best_score = max(scores)

st.markdown('<div class="section-label" style="margin-top:1rem">Side by side</div>', unsafe_allow_html=True)

cols = st.columns(len(apts_ordered))
for i, (apt, score) in enumerate(zip(apts_ordered, scores)):
    sc    = score_color_class(score)
    comm  = f"{apt.commute_minutes} min" if apt.commute_minutes is not None else "N/A"
    badge = "🏆 Best match" if score == best_score else ""
    with cols[i]:
        st.markdown(f"""
        <div class="apt-card apt-card-top" style="flex-direction:column;gap:10px">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div class="apt-name">{apt.name}</div>
            <div class="score-col">
              <div class="score-num {sc}">{score}</div>
              <div class="score-lbl">match</div>
            </div>
          </div>
          <div class="apt-addr">📍 {apt.address}</div>
          <div class="tags">
            <span class="tag t-rent">₹{apt.rent:,}/mo</span>
            <span class="tag t-commute">🚗 {comm}</span>
            <span class="tag t-beds">🛏 {apt.bedrooms} BHK</span>
          </div>
          {"<div style='color:#f59e0b;font-size:0.8rem;font-weight:600;margin-top:4px'>" + badge + "</div>" if badge else ""}
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="section-label" style="margin-top:1.5rem">Detailed comparison</div>', unsafe_allow_html=True)

def winner_class(values, lower_is_better=True):
    valid = [(v, i) for i, v in enumerate(values) if v is not None]
    if not valid:
        return [""] * len(values)
    best_val = min(v for v, _ in valid) if lower_is_better else max(v for v, _ in valid)
    return ["cmp-winner" if v == best_val else "" for v in values]

rows = [
    ("Monthly rent (₹)",   [f"₹{a.rent:,}" for a in apts_ordered],      winner_class([a.rent for a in apts_ordered], lower_is_better=True)),
    ("Commute (min)",      [f"{a.commute_minutes}" if a.commute_minutes else "N/A" for a in apts_ordered], winner_class([a.commute_minutes for a in apts_ordered], lower_is_better=True)),
    ("Bedrooms",           [str(a.bedrooms) for a in apts_ordered],      winner_class([a.bedrooms for a in apts_ordered], lower_is_better=False)),
    ("Match score",        [str(s) for s in scores],                     winner_class(scores, lower_is_better=False)),
    ("Notes",              [a.notes or "—" for a in apts_ordered],       [""] * len(apts_ordered)),
]

header_cells = "".join(f"<th>{a.name}</th>" for a in apts_ordered)
body_rows = ""
for label, values, classes in rows:
    cells = "".join(f'<td class="{cls}">{val}</td>' for val, cls in zip(values, classes))
    body_rows += f"<tr><th style='width:160px'>{label}</th>{cells}</tr>"

st.markdown(f"""
<table class="cmp-table">
  <thead><tr><th></th>{header_cells}</tr></thead>
  <tbody>{body_rows}</tbody>
</table>
""", unsafe_allow_html=True)