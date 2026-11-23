"""
theme.py

Shared CSS and theme logic used by every page.
Import and call apply_theme() at the top of each page file.
"""

import sys
from pathlib import Path
import streamlit as st

# Ensure current directory is in sys.path
_CURRENT_DIR = str(Path(__file__).resolve().parent)
if _CURRENT_DIR not in sys.path:
    sys.path.insert(0, _CURRENT_DIR)


DARK = {
    "bg":          "#08090d",   # Deep Midnight Obsidian
    "surface":     "#11131a",   # Smoky Charcoal-Slate card surface
    "surface2":    "#181b24",   # Elevated slate surface for tables & hover
    "border":      "#222634",   # Bronze-tinted graphite border
    "border2":     "#2e3344",   # Secondary border & outlines
    "text":        "#f4f3ef",   # Pearl White (soft on eyes, luxurious)
    "text2":       "#a8a69e",   # Warm Stone Gray body copy
    "muted":       "#6c6a64",   # Subtle captions & metadata
    "accent":      "#d4af37",   # Champagne Gold / Brushed Brass
    "accent_bg":   "#28200d",   # Dark Warm Gold Tint for active states
    "green":       "#34d399",   # Luminous Emerald / Mint for top scores
    "green_bg":    "#06281b",   # Deep Emerald Surface
    "amber":       "#d4af37",   # Champagne Gold
    "red":         "#e56748",   # Warm Terracotta
    "purple":      "#b89dfc",   # Muted Amethyst
    "purple_bg":   "#1e1634",   # Deep Amethyst Surface
    "blue_tag_bg": "#28200d",   # Rent Chip: Dark Amber Gold
    "blue_tag":    "#e5c07b",   # Rent Chip Text: Luminous Champagne Gold
}

# ── Warm Linen & Antique Bronze (Editorial Light Theme) ────────────────────────
LIGHT = {
    "bg":          "#f5f4f0",   # Warm Alabaster / Linen
    "surface":     "#ffffff",   # Crisp White card surface
    "surface2":    "#eceae4",   # Soft Putty / Bone
    "border":      "#d5d2c8",   # Warm parchment border
    "border2":     "#c4c0b4",   # Deeper parchment outline
    "text":        "#0f0e0c",   # Deep Espresso Black
    "text2":       "#2e2c26",   # Warm Charcoal body text
    "muted":       "#68645c",   # Stone Taupe
    "accent":      "#8b6914",   # Antique Gold / Bronze
    "accent_bg":   "#fef3c7",   # Soft Gold Tint
    "green":       "#1e6d42",   # Deep Forest Emerald
    "green_bg":    "#d1fae5",   # Soft Mint
    "amber":       "#8b6914",   # Antique Amber
    "red":         "#b85028",   # Warm Terracotta
    "purple":      "#4c1d95",   # Royal Violet
    "purple_bg":   "#ede9fe",   # Soft Lavender
    "blue_tag_bg": "#fef3c7",   # Rent Chip: Pale Amber
    "blue_tag":    "#853606",   # Rent Chip Text: Caramel Brown
}

AREA_FILTERS = [
    "All",
    # Gurgaon Sectors & Localities
    "Sector 14",
    "Sector 15 Part 2",
    "Sector 17",
    "Sector 21, Gurgaon",
    "Sector 22",
    "Sector 23",
    "Sector 23A",
    "Sector 28",
    "Sector 31",
    "Sector 38",
    "Sector 39",
    "Sector 40",
    "Sector 42",
    "Sector 43",
    "Sector 44",
    "Sector 45",
    "Sector 46",
    "Sector 47",
    "Sector 48",
    "DLF Phase 2",
    "DLF Phase 3",
    "Ambience Island",
    "Palam Vihar",
    "Saraswati Vihar",
    "Chakkarpur",
    # Faridabad Localities
    "Old Faridabad",
    "NIT Faridabad",
    "Sector 15 Market",
    "Sector 21C",
    "Badkhal",
    "Ballabhgarh",
]

ORIGIN_ADDRESS = "Faridabad Railway Station, Faridabad, Haryana"


def get_colors():
    return LIGHT if st.session_state.get("theme") == "light" else DARK


def apply_theme():
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"
    if "area_filter" not in st.session_state:
        st.session_state["area_filter"] = "All"

    c = get_colors()
    is_light = st.session_state["theme"] == "light"
    btn_text_color = "#ffffff" if is_light else "#08090d"

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,700;0,9..144,900;1,9..144,400&family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@700;800&display=swap');

/* ── Typography & Global Font ── */
html, body, [class*="css"], .stMarkdown, p, div, label, input, textarea {{
    font-family: 'Inter', Arial, sans-serif;
    box-sizing: border-box;
}}

/* Restore Streamlit Icon fonts */
[data-testid="stIconMaterial"], 
[data-testid="stExpanderToggleIcon"], 
.material-icons, 
.material-symbols-rounded, 
.material-symbols-outlined,
[class*="material-symbols"] {{
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
}}

/* Hide floating 'Press Enter to apply' instruction */
div[data-testid="InputInstructions"] {{
    display: none !important;
}}

/* Unified Backgrounds */
.stApp, 
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
section.main,
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"] {{
    background: {c["bg"]} !important;
    color: {c["text"]} !important;
}}

[data-testid="stBottom"] > div {{
    background: {c["bg"]} !important;
}}
[data-testid="stChatInput"] {{
    background: {c["surface"]} !important;
    border: 1px solid {c["border"]} !important;
    border-radius: 12px !important;
}}
[data-testid="stChatInput"] textarea {{
    color: {c["text"]} !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {c["surface"]} !important;
    border-right: 1px solid {c["border"]} !important;
}}
#MainMenu, footer {{ visibility: hidden; }}
[data-testid="stSidebarHeader"] {{ display: none !important; }}
button[data-testid="baseButton-headerNoPadding"] {{ display: none !important; }}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span:not(.st-emotion-cache-hidden),
[data-testid="stSidebar"] .stMarkdown {{ color: {c["text2"]} !important; }}

[data-testid="stSidebar"] [data-testid="stSlider"] div[data-testid="stTickBar"] {{
    color: {c["muted"]} !important;
}}
[data-testid="stSidebar"] [data-testid="stSlider"] .st-emotion-cache-1dp5vir {{
    background: {c["accent"]} !important;
}}

/* ── Selectbox styling ── */
div[data-testid="stSelectbox"] > div > div {{
    background: {c["surface2"]} !important;
    border: 1px solid {c["border"]} !important;
    color: {c["text"]} !important;
    border-radius: 8px !important;
}}
div[data-testid="stSelectbox"] svg {{
    fill: {c["text2"]} !important;
}}

/* ── Text Input Styling ── */
div[data-testid="stTextInput"] input {{
    background: {c["surface2"]} !important;
    border: 1px solid {c["border"]} !important;
    color: {c["text"]} !important;
    border-radius: 8px !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: {c["surface"]} !important;
    color: {c["text"]} !important;
    border: 1px solid {c["border"]} !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease !important;
}}
.stButton > button:hover {{
    border-color: {c["accent"]} !important;
    color: {c["accent"]} !important;
    background: {c["surface2"]} !important;
}}
.stButton > button[kind="primary"] {{
    background: {c["accent"]} !important;
    color: {btn_text_color} !important;
    border-color: {c["accent"]} !important;
    font-weight: 700 !important;
}}
.stButton > button[kind="primary"]:hover {{
    background: {c["accent"]} !important;
    color: {btn_text_color} !important;
    opacity: 0.92;
    box-shadow: 0 0 20px rgba(212, 175, 55, 0.35) !important;
}}

/* ── Expander Styling ── */
[data-testid="stExpander"] {{
    background: {c["surface"]} !important;
    border: 1px solid {c["border"]} !important;
    border-radius: 10px !important;
    overflow: hidden;
}}
[data-testid="stExpander"] summary {{
    color: {c["text"]} !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
}}

/* ── Sidebar nav ── */
[data-testid="stSidebarNav"] {{ display: none !important; }}
section[data-testid="stSidebar"] > div {{
    padding: 1.2rem 1rem !important;
}}
[data-testid="stSidebar"] hr {{
    border-color: {c["border"]} !important;
    margin: 12px 0 !important;
}}

/* ── st.page_link styling ── */
[data-testid="stSidebar"] [data-testid="stPageLink"] a {{
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 7px 12px !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: {c["text2"]} !important;
    text-decoration: none !important;
    transition: background 0.15s !important;
}}
[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {{
    background: {c["surface2"]} !important;
    color: {c["text"]} !important;
}}
[data-testid="stSidebar"] [data-testid="stPageLink-active"] a {{
    background: {c["accent_bg"]} !important;
    color: {c["accent"]} !important;
    font-weight: 600 !important;
}}

/* ── Hero ── */
.hero {{ margin-bottom: 1.8rem; }}
.hero-title {{
    font-family: 'Fraunces', serif !important;
    font-size: 2.8rem; font-weight: 900;
    color: {c["text"]}; letter-spacing: -0.04em;
    line-height: 1; margin: 0 0 8px;
}}
.hero-accent {{ color: {c["accent"]}; font-style: italic; }}
.hero-sub {{ font-size: 0.95rem; color: {c["muted"]}; margin: 0; font-weight: 500; }}

/* ── Stat cards ── */
.stats-grid {{
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 12px; margin-bottom: 1.8rem;
}}
.stat-card {{
    background: {c["surface"]}; border: 1px solid {c["border"]};
    border-radius: 14px; padding: 16px 20px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}}
.stat-label {{
    font-size: 0.7rem; font-weight: 700; color: {c["muted"]};
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;
}}
.stat-val {{ 
    font-family: 'Fraunces', serif !important;
    font-size: 2rem; font-weight: 900; color: {c["text"]}; line-height: 1; 
}}
.stat-unit {{ font-size: 0.9rem; color: {c["muted"]}; font-weight: 500; }}

/* ── Section label ── */
.section-label {{
    font-size: 0.72rem; font-weight: 700; color: {c["muted"]};
    text-transform: uppercase; letter-spacing: 0.14em;
    padding-bottom: 8px; border-bottom: 1px solid {c["border"]};
    margin-bottom: 14px;
}}

/* ── Apartment cards ── */
.apt-card {{
    display: flex; align-items: flex-start; gap: 16px;
    background: {c["surface"]}; border: 1px solid {c["border"]};
    border-radius: 16px; padding: 18px 22px; margin-bottom: 12px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    transition: border-color 0.2s, transform 0.15s, box-shadow 0.2s;
}}
.apt-card:hover {{ 
    border-color: {c["accent"]}; 
    transform: translateY(-2px); 
    box-shadow: 0 10px 30px rgba(0,0,0,0.22);
}}
.apt-card-top {{ 
    border-color: {c["accent_bg"]}; 
    background: {c["surface"]}; 
}}

.rank-badge {{
    font-family: 'Fraunces', serif !important;
    font-size: 1.5rem; font-weight: 900;
    min-width: 44px; text-align: center;
    color: {c["border2"]}; padding-top: 2px; line-height: 1;
}}
.rank-top {{ color: {c["accent"]}; }}

.apt-body {{ flex: 1; min-width: 0; }}
.apt-name {{
    font-size: 1.05rem; font-weight: 700; color: {c["text"]};
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    margin-bottom: 4px;
}}
.apt-addr {{ font-size: 0.82rem; color: {c["muted"]}; margin-bottom: 12px; font-weight: 500; }}
.tags {{ display: flex; gap: 8px; flex-wrap: wrap; }}
.tag {{
    font-size: 0.74rem; font-weight: 700;
    padding: 4px 11px; border-radius: 20px;
}}
.t-rent    {{ background: {c["blue_tag_bg"]}; color: {c["blue_tag"]}; }}
.t-commute {{ background: {c["green_bg"]};    color: {c["green"]}; }}
.t-beds    {{ background: {c["purple_bg"]};   color: {c["purple"]}; }}
.apt-notes {{
    font-size: 0.78rem; color: {c["muted"]};
    margin-top: 8px; font-style: italic;
}}

/* ── Score badge ── */
.score-col {{ text-align: center; min-width: 66px; }}
.score-num {{
    font-family: 'Fraunces', serif !important;
    font-size: 1.8rem; font-weight: 900; line-height: 1;
}}
.score-lbl {{
    font-size: 0.62rem; color: {c["muted"]};
    text-transform: uppercase; letter-spacing: 0.1em; margin-top: 3px; font-weight: 600;
}}
.s-hi {{ color: {c["green"]}; }}
.s-md {{ color: {c["amber"]}; }}
.s-lo {{ color: {c["red"]}; }}

/* ── Compare table ── */
.cmp-table {{
    width: 100%; border-collapse: collapse; font-size: 0.88rem;
}}
.cmp-table th {{
    background: {c["surface2"]}; color: {c["muted"]};
    font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    padding: 12px 16px; text-align: left;
    border-bottom: 1px solid {c["border"]};
}}
.cmp-table td {{
    padding: 12px 16px;
    border-bottom: 1px solid {c["border"]};
    color: {c["text2"]};
}}
.cmp-table tr:last-child td {{ border-bottom: none; }}
.cmp-winner {{ color: {c["green"]}; font-weight: 700; }}

/* ── Info cards ── */
.info-card {{
    background: {c["surface"]}; border: 1px solid {c["border"]};
    border-radius: 14px; padding: 22px 24px; margin-bottom: 16px;
}}
.info-title {{
    font-family: 'Fraunces', serif !important;
    font-size: 1.05rem; font-weight: 700;
    color: {c["text"]}; margin-bottom: 8px;
}}
.info-body {{
    font-size: 0.88rem; color: {c["text2"]}; line-height: 1.7;
}}

/* ── Empty state ── */
.empty {{ text-align: center; padding: 60px 24px; }}
.empty-ico {{ font-size: 2.8rem; margin-bottom: 12px; }}
.empty-ttl {{ font-size: 1.1rem; font-weight: 700; color: {c["text2"]}; margin-bottom: 6px; }}
.empty-sub {{ font-size: 0.88rem; color: {c["muted"]}; }}
</style>
""", unsafe_allow_html=True)


def render_area_filter_bar():
    st.markdown('<div class="section-label">Browse by area</div>', unsafe_allow_html=True)

    bar_col1, bar_col2 = st.columns([1, 4])
    with bar_col1:
        is_all = st.session_state.get("area_filter", "All") == "All"
        if st.button("🌐 All Areas", use_container_width=True, type="primary" if is_all else "secondary"):
            st.session_state.area_filter = "All"
            st.rerun()

    with bar_col2:
        current_area = st.session_state.get("area_filter", "All")
        current_idx = AREA_FILTERS.index(current_area) if current_area in AREA_FILTERS else 0
        selected = st.selectbox(
            "Select Area or Sector",
            AREA_FILTERS,
            index=current_idx,
            label_visibility="collapsed",
        )
        if selected != st.session_state.get("area_filter"):
            st.session_state.area_filter = selected
            st.rerun()


def load_tracker(force_reload: bool = False):
    """Safely loads or instantiates ApartmentTracker without static type conflicts."""
    tracker_cls = None
    try:
        import tracker  # type: ignore
        tracker_cls = getattr(tracker, "ApartmentTracker", None)
    except Exception:
        pass

    if tracker_cls is None:
        try:
            import apartment  # type: ignore
            tracker_cls = getattr(apartment, "ApartmentTracker", None)
        except Exception:
            pass

    if tracker_cls is None:
        class _FallbackTracker:
            def __init__(self):
                self.apartments = []
            def add_apartment(self, apt):
                self.apartments.append(apt)
            def filter_by_area(self, area):
                if not area or area == "All":
                    return self.apartments
                return [a for a in self.apartments if area.lower() in getattr(a, "address", "").lower()]
            def __len__(self):
                return len(self.apartments)
        tracker_cls = _FallbackTracker

    if "tracker" not in st.session_state or force_reload:
        t = tracker_cls()
        try:
            from storage import load_from_file  # type: ignore
            for apt in load_from_file():
                t.add_apartment(apt)
        except Exception:
            pass
        st.session_state.tracker = t
    return st.session_state.tracker


# Explicitly export module symbols for Pylance / IDE static analysis
__all__ = [
    "DARK",
    "LIGHT",
    "AREA_FILTERS",
    "ORIGIN_ADDRESS",
    "get_colors",
    "apply_theme",
    "render_area_filter_bar",
    "load_tracker",
    "score_color_class",
    "render_apt_card",
    "listing_links_html",
]


def score_color_class(score):
    if score >= 65:
        return "s-hi"
    elif score >= 40:
        return "s-md"
    return "s-lo"


def render_apt_card(apt, rank, rent_weight, commute_weight, max_rent=80000, max_commute=120):
    score = apt.score(
        max_rent=max_rent, max_commute=max_commute,
        rent_weight=rent_weight, commute_weight=commute_weight,
    )
    sc   = score_color_class(score)
    rc   = "rank-top" if rank <= 3 else ""
    top  = "apt-card-top" if rank <= 3 else ""
    comm = f"{apt.commute_minutes} min" if apt.commute_minutes is not None else "N/A"
    note = f'<div class="apt-notes">📝 {apt.notes}</div>' if apt.notes else ""
    c    = get_colors()
    links = listing_links_html(apt, c)

    st.markdown(f"""
    <div class="apt-card {top}">
      <div class="rank-badge {rc}">#{rank}</div>
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


def listing_links_html(apt, c):
    query = f"{apt.name} {apt.address}".replace(" ", "+")
    area  = apt.address.split(",")[0].strip().replace(" ", "+")

    links = [
        ("99acres",     f"https://www.99acres.com/search/property/rent/{area}"),
        ("MagicBricks", f"https://www.magicbricks.com/property-for-rent/search?keyword={query}"),
        ("NoBroker",    f"https://www.nobroker.in/property/rent/{area}"),
        ("📍 Maps",     f"https://www.google.com/maps/search/{query}"),
    ]

    link_html = " · ".join([
        f'<a href="{url}" target="_blank" style="color:{c["muted"]};'
        f'font-size:0.75rem;text-decoration:none;font-weight:600;'
        f'transition:color 0.15s" '
        f'onmouseover="this.style.color=\'{c["accent"]}\'" '
        f'onmouseout="this.style.color=\'{c["muted"]}\'">'
        f'{label}</a>'
        for label, url in links
    ])

    return f'''
    <div style="margin-top:10px;padding-top:8px;
    border-top:1px solid {c["border"]};font-size:0.75rem;
    color:{c["muted"]}">
        🔗 View on: {link_html}
    </div>
    '''