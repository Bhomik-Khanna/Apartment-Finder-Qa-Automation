import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import Patch

from theme import apply_theme, load_tracker, render_apt_card, get_colors, AREA_FILTERS, render_area_filter_bar

st.set_page_config(
    page_title="Big 3 Rentals",
    page_icon="Image.png",
    layout="wide",
    initial_sidebar_state="expanded",
)


if st.query_params.get("enter") == "1":
    st.session_state["entered"] = True
    st.query_params.clear()

if "entered" not in st.session_state:
    st.session_state["entered"] = False


if not st.session_state["entered"]:
    from Landing import render_landing
    render_landing()
    st.stop()


apply_theme()
st.logo("Image.png")
tracker = load_tracker(force_reload=True)
c = get_colors()


with st.sidebar:
    # Button to jump back to Landing Page
    if st.button("← Back to Landing Page", use_container_width=True):
        st.session_state["entered"] = False
        st.rerun()

    
    st.markdown(f"""
    <div style="font-size:0.65rem;font-weight:700;color:{c['muted']};
    text-transform:uppercase;letter-spacing:0.1em;
    margin-bottom:6px;padding:0 2px">Pages</div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_About.py",   label="  About")
    st.page_link("app.py",             label="  Home")
    st.page_link("pages/1_Compare.py", label="  Compare")
    st.page_link("pages/2_Manage.py",  label="  Manage")
    st.page_link("pages/4_Near_Me.py", label="  Near Me")
    st.page_link("pages/5_AI_Assistant.py", label="  AI Assistant")
    st.page_link("pages/6_Analytics.py", label="  Analytics")
    st.page_link("pages/8_Settings.py", label="  Settings")

    st.markdown("---")

   
    st.markdown(f"""<div style="font-size:0.75rem;font-weight:600;
    color:{c['text']};margin-bottom:8px">🎛 What matters to you?</div>""",
    unsafe_allow_html=True)
    rent_weight = float(st.slider(
        "Rent vs commute priority",
        min_value=0.1, max_value=0.9, value=0.6, step=0.1,
        help="Higher = rent matters more"
    ))
    commute_weight = round(1.0 - rent_weight, 1)
    c1, c2 = st.columns(2)
    c1.caption(f" Rent **{int(rent_weight*100)}%**")
    c2.caption(f" Commute **{int(commute_weight*100)}%**")

    st.markdown("---")

    
    st.markdown(f"""<div style="font-size:0.75rem;font-weight:600;
    color:{c['text']};margin-bottom:8px"> Filters</div>""",
    unsafe_allow_html=True)
    max_rent     = st.slider("Max rent (₹)", 0, 80000, 80000, step=1000)
    max_commute  = st.slider("Max commute (min)", 0, 120, 120, step=5)
    min_bedrooms = int(st.selectbox("Min bedrooms", [0, 1, 2, 3], index=0) or 0)

    st.markdown("---")
    st.page_link("pages/2_Manage.py", label="  Add apartment")


st.markdown("""
<div class="hero">
  <div class="hero-title">Big 3 <span class="hero-accent">Rentals</span></div>
  <p class="hero-sub">NCR · Faridabad &amp; Gurgaon · Ranked by your priorities</p>
</div>
""", unsafe_allow_html=True)

if len(tracker) == 0:
    st.markdown("""<div class="empty">
        <div class="empty-ico">🏘️</div>
        <div class="empty-ttl">No apartments yet</div>
        <div class="empty-sub">Go to <b>Manage</b> to add one, or run <code>seed_data.py</code> first.</div>
    </div>""", unsafe_allow_html=True)
    st.stop()


render_area_filter_bar()


selected_area = st.session_state.area_filter
area_kw = "" if selected_area == "All" else selected_area

area_filtered = tracker.filter_by_area(area_kw)
filtered = [
    apt for apt in area_filtered
    if apt.rent <= max_rent
    and apt.bedrooms >= min_bedrooms
    and (apt.commute_minutes is None or apt.commute_minutes <= max_commute)
]
ranked = sorted(
    filtered,
    key=lambda apt: apt.score(
        max_rent=max_rent if max_rent > 0 else 80000,
        max_commute=max_commute if max_commute > 0 else 120,
        rent_weight=rent_weight,
        commute_weight=commute_weight,
    ),
    reverse=True,
)


best  = ranked[0].score(rent_weight=rent_weight, commute_weight=commute_weight) if ranked else 0
comms = [a.commute_minutes for a in ranked if a.commute_minutes is not None]
med   = sorted(comms)[len(comms)//2] if comms else "—"
avg_r = int(sum(a.rent for a in ranked) / len(ranked)) if ranked else 0

st.markdown(f"""
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-label">Listings shown</div>
    <div class="stat-val">{len(ranked)} <span class="stat-unit">/ {len(tracker)}</span></div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Best match</div>
    <div class="stat-val">{best}<span class="stat-unit">%</span></div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Median commute</div>
    <div class="stat-val">{med}<span class="stat-unit"> min</span></div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Avg rent</div>
    <div class="stat-val">₹{avg_r:,}</div>
  </div>
</div>
""", unsafe_allow_html=True)


if not ranked:
    st.markdown(f"""<div class="empty">
        <div class="empty-ico">🔍</div>
        <div class="empty-ttl">No matches for "{selected_area}"</div>
        <div class="empty-sub">{len(tracker)} apartments saved — try a different area or loosen the filters.</div>
    </div>""", unsafe_allow_html=True)
    st.stop()


st.markdown('<div class="section-label">Ranked results</div>', unsafe_allow_html=True)
for i, apt in enumerate(ranked):
    render_apt_card(apt, i + 1, rent_weight, commute_weight, max_rent or 80000, max_commute or 120)


chart_apts = [a for a in ranked if a.commute_minutes is not None]
if len(chart_apts) >= 2:
    st.markdown('<div class="section-label" style="margin-top:1.5rem">Top apartments at a glance</div>',
                unsafe_allow_html=True)

    is_light   = st.session_state.get("theme") == "light"
    bg         = "#ffffff" if is_light else "#0f1320"
    text_color = "#0f172a" if is_light else "#e5e7eb"
    grid_color = "#e2e8f0" if is_light else "#1a2035"
    bar_edge   = "#ffffff" if is_light else "#0f1320"

    # Show top 8 only — keeps it readable
    top = chart_apts[:8]
    names  = [a.name.split()[0] + " " + a.name.split()[1] if len(a.name.split()) > 1
              else a.name for a in top]
    rents  = [a.rent for a in top]
    comms  = [a.commute_minutes for a in top]
    scores = [a.score(rent_weight=rent_weight, commute_weight=commute_weight) for a in top]

    # Color bars by score
    def bar_color(s):
        if s >= 65: return "#10b981"
        if s >= 40: return "#f59e0b"
        return "#ef4444"
    colors = [bar_color(s) for s in scores]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    fig.patch.set_facecolor(bg)

    for ax in (ax1, ax2):
        ax.set_facecolor(bg)
        for spine in ax.spines.values():
            spine.set_edgecolor(grid_color)
        ax.tick_params(colors=text_color, labelsize=8)
        ax.grid(axis="x", color=grid_color, linewidth=0.5, zorder=0)
        ax.set_axisbelow(True)

    # Left: Rent chart
    bars1 = ax1.barh(names, rents, color=colors, edgecolor=bar_edge,
                     linewidth=0.5, zorder=3, height=0.6)
    ax1.set_xlabel("Monthly rent (₹)", color=text_color, fontsize=8, labelpad=6)
    ax1.set_title("Rent", color=text_color, fontsize=9, fontweight="bold", pad=10)
    ax1.invert_yaxis()
    # Value labels on bars
    for bar, val in zip(bars1, rents):
        ax1.text(bar.get_width() + max(rents)*0.01, bar.get_y() + bar.get_height()/2,
                 f"₹{val:,}", va="center", ha="left",
                 color=text_color, fontsize=7)
    ax1.set_xlim(0, max(rents) * 1.22)
    # Using imported FuncFormatter from matplotlib.ticker
    ax1.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"₹{int(x/1000)}k"))

    # Right: Commute chart
    bars2 = ax2.barh(names, comms, color=colors, edgecolor=bar_edge,
                     linewidth=0.5, zorder=3, height=0.6)
    ax2.set_xlabel("Commute (minutes)", color=text_color, fontsize=8, labelpad=6)
    ax2.set_title("Commute time", color=text_color, fontsize=9, fontweight="bold", pad=10)
    ax2.invert_yaxis()
    for bar, val in zip(bars2, comms):
        ax2.text(bar.get_width() + max(comms)*0.01, bar.get_y() + bar.get_height()/2,
                 f"{val} min", va="center", ha="left",
                 color=text_color, fontsize=7)
    ax2.set_xlim(0, max(comms) * 1.25)

    # Score legend
    legend = [
        Patch(color="#10b981", label="Strong match (≥65)"),
        Patch(color="#f59e0b", label="Okay (≥40)"),
        Patch(color="#ef4444", label="Weak (<40)"),
    ]
    fig.legend(handles=legend, loc="lower center", ncol=3,
               fontsize=7.5, frameon=False,
               labelcolor=text_color,
               bbox_to_anchor=(0.5, -0.05))

    # Passing rect as a 4-float tuple
    plt.tight_layout(rect=(0.0, 0.06, 1.0, 1.0))
    st.pyplot(fig)
    plt.close(fig)