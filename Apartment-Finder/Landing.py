"""
Landing.py — Landing page entry point
Run with: streamlit run Landing.py
"""
import streamlit as st

def render_landing():
    
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"

    is_light = st.session_state["theme"] == "light"

   
    if is_light:
        BG         = "#f5f4f0"
        BG2        = "#eceae4"
        TEXT       = "#0f0e0c"
        TEXT2      = "#2e2c26"
        MUTED      = "#68645c"
        BORDER     = "#d5d2c8"
        SURFACE    = "#ffffff"
        CARD_BG    = "rgba(255,255,255,0.94)"
        NOISE_OP   = "0.04"
        ORB1       = "rgba(180,140,80,0.22)"
        ORB2       = "rgba(120,100,160,0.15)"
        ORB3       = "rgba(60,140,100,0.12)"
        GRAD_TEXT  = "linear-gradient(135deg,#a07507 0%,#7a4e2c 50%,#465c22 100%)"
        ACCENT     = "#8b6914"
        BTN_BG     = "linear-gradient(135deg,#8b6914,#6b4f2a)"
        BTN_GLOW   = "rgba(139,105,20,0.4)"
        PAIN_BG    = "rgba(180,80,40,0.08)"
        PAIN_BORD  = "rgba(180,80,40,0.24)"
        PAIN_NUM   = "#b85028"
        FEAT_BG    = "rgba(255,255,255,0.85)"
        FEAT_BORD  = "rgba(139,105,20,0.22)"
        SCORE_HI   = "#1e6d42"
        SCORE_MID  = "#8b6914"
        DIVIDER    = "rgba(0,0,0,0.08)"
        STAT_NUM   = "#0f0e0c"
        EYEBROW_P  = "#b85028"
        EYEBROW_S  = "#8b6914"
        SCROLL_C   = "#b8b4ab"
        TAG_RENT_B = "#fef3c7"
        TAG_RENT_T = "#853606"
        TAG_COM_B  = "#d1fae5"
        TAG_COM_T  = "#044e39"
        TAG_BED_B  = "#ede9fe"
        TAG_BED_T  = "#4c1d95"
    else:
        BG         = "#08090d"   # Deep Midnight Obsidian
        BG2        = "#11131a"   # Elevated Slate
        TEXT       = "#f4f3ef"   # Pearl White
        TEXT2      = "#a8a69e"   # Warm Stone Gray
        MUTED      = "#6c6a64"   # Muted Bronze Graphite
        BORDER     = "#222634"   # Refined Obsidian Border
        SURFACE    = "#11131a"
        CARD_BG    = "rgba(17,19,26,0.96)"
        NOISE_OP   = "0.03"
        ORB1       = "rgba(212,175,55,0.18)"   # Warm Gold Ambient Halo
        ORB2       = "rgba(140,110,60,0.14)"   # Muted Amber Glow
        ORB3       = "rgba(52,211,153,0.08)"   # Subtle Emerald Shimmer
        GRAD_TEXT  = "linear-gradient(135deg,#fcedb6 0%,#d4af37 50%,#8b6914 100%)"
        ACCENT     = "#d4af37"   # Champagne Gold
        BTN_BG     = "linear-gradient(135deg,#d4af37,#9e7d23)"
        BTN_GLOW   = "rgba(212,175,55,0.45)"
        PAIN_BG    = "rgba(229,103,72,0.08)"
        PAIN_BORD  = "rgba(229,103,72,0.22)"
        PAIN_NUM   = "#e56748"
        FEAT_BG    = "rgba(17,19,26,0.85)"
        FEAT_BORD  = "rgba(212,175,55,0.18)"
        SCORE_HI   = "#34d399"   # Luminous Emerald
        SCORE_MID  = "#d4af37"   # Champagne Gold
        DIVIDER    = "rgba(255,255,255,0.06)"
        STAT_NUM   = "#f4f3ef"
        EYEBROW_P  = "#e56748"
        EYEBROW_S  = "#d4af37"
        SCROLL_C   = "#3a3a44"
        TAG_RENT_B = "#28200d"
        TAG_RENT_T = "#e5c07b"
        TAG_COM_B  = "#06281b"
        TAG_COM_T  = "#34d399"
        TAG_BED_B  = "#1e1634"
        TAG_BED_T  = "#b89dfc"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,700;0,9..144,900;1,9..144,400&family=DM+Sans:wght@400;500;600;700&display=swap');

    #MainMenu, footer, header {{ visibility: hidden !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    .stApp {{ background: {BG} !important; }}
    [data-testid="stAppViewContainer"] {{ background: {BG} !important; }}
    div[data-testid="stVerticalBlock"] {{ gap: 0 !important; }}
    .block-container {{ padding: 0 !important; max-width: 100% !important; }}

    /* Hide Streamlit header anchor links */
    a.header-anchor, [data-testid="stHeaderActionElements"] {{ display: none !important; }}

    html {{ scroll-behavior: smooth; }}
    * {{ box-sizing: border-box; }}

    .orb {{ position: fixed; border-radius: 50%; filter: blur(100px); pointer-events: none; z-index: 0; }}
    .o1 {{ width: 720px; height: 720px; background: radial-gradient(circle, {ORB1}, transparent); top: -200px; right: -150px; animation: orb 12s ease-in-out infinite; }}
    .o2 {{ width: 540px; height: 540px; background: radial-gradient(circle, {ORB2}, transparent); bottom: -100px; left: -100px; animation: orb 16s ease-in-out infinite reverse; }}
    .o3 {{ width: 420px; height: 420px; background: radial-gradient(circle, {ORB3}, transparent); top: 40%; left: 20%; animation: orb 10s ease-in-out infinite 5s; }}
    .o4 {{ width: 360px; height: 360px; background: radial-gradient(circle, {ORB1}, transparent); bottom: 10%; right: 8%; animation: orb 14s ease-in-out infinite 2s; }}
    @keyframes orb {{
      0%, 100% {{ transform: translate(0,0) scale(1); }}
      50% {{ transform: translate(30px, -40px) scale(1.12); }}
    }}

    .grid-floor {{
      position: fixed; left: 0; right: 0; bottom: 0; height: 60vh;
      z-index: 0; pointer-events: none;
      background-image:
        linear-gradient(to right, {DIVIDER} 1px, transparent 1px),
        linear-gradient(to bottom, {DIVIDER} 1px, transparent 1px);
      background-size: 64px 64px;
      transform: perspective(600px) rotateX(62deg);
      transform-origin: bottom;
      -webkit-mask-image: linear-gradient(to top, rgba(0,0,0,0.7), transparent 85%);
      mask-image: linear-gradient(to top, rgba(0,0,0,0.7), transparent 85%);
    }}

    .hero {{
      position: relative; z-index: 1;
      min-height: 94vh;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      padding: 100px 32px 60px;
      text-align: center !important;
    }}

    .hero-kicker {{
      display: inline-flex; align-items: center; justify-content: center; gap: 10px;
      font-size: 0.86rem; font-weight: 600;
      letter-spacing: 0.16em; text-transform: uppercase;
      color: {TEXT2};
      margin-bottom: 30px;
      text-align: center !important;
      animation: zoomInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}

    
    .hero-h1 {{
      font-family: 'Fraunces', serif !important;
      font-size: clamp(3.2rem, 7.8vw, 6.5rem) !important;
      font-weight: 900 !important;
      letter-spacing: -0.04em !important;
      line-height: 0.98 !important;
      max-width: 1050px !important;
      margin: 0 auto 16px !important;
      text-align: center !important;
      display: block !important;
      color: {TEXT} !important;
      animation: zoomInUp 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.1s both;
    }}
    .hero-h1 .w1 {{
      font-family: 'Fraunces', serif !important;
      font-size: inherit !important;
      font-weight: 900 !important;
      color: {TEXT} !important;
      display: block !important;
      text-align: center !important;
    }}
    .hero-h1 .w2 {{
      font-family: 'Fraunces', serif !important;
      font-size: inherit !important;
      display: block !important;
      font-style: italic !important;
      font-weight: 400 !important;
      background: {GRAD_TEXT} !important;
      -webkit-background-clip: text !important;
      -webkit-text-fill-color: transparent !important;
      background-clip: text !important;
      text-align: center !important;
    }}

    .hero-sub {{
      font-size: clamp(1.15rem, 2.3vw, 1.38rem);
      color: {TEXT2} !important;
      max-width: 660px;
      line-height: 1.72;
      margin: 30px auto 44px !important;
      font-weight: 450;
      text-align: center !important;
      animation: zoomInUp 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both;
    }}

    .hero-btn {{
      display: inline-flex; align-items: center; justify-content: center; gap: 12px;
      background: {BTN_BG};
      color: #fff !important;
      font-family: 'DM Sans', sans-serif;
      font-size: 1.05rem; font-weight: 600;
      padding: 18px 42px;
      border-radius: 100px;
      text-decoration: none !important;
      box-shadow: 0 0 50px {BTN_GLOW};
      transition: transform 0.28s cubic-bezier(0.2, 0.9, 0.3, 1.2), box-shadow 0.28s ease;
      animation: zoomInUp 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both;
    }}
    .hero-btn:hover {{
      transform: translateY(-4px) scale(1.05);
      box-shadow: 0 0 75px {BTN_GLOW};
    }}

   
    .stage {{
      perspective: 1500px;
      margin-top: 60px;
      width: 100%; max-width: 1060px;
      height: 350px;
      position: relative;
      animation: zoomInUp 1s cubic-bezier(0.16, 1, 0.3, 1) 0.4s both;
    }}

    .fcard {{
      position: absolute;
      background: {CARD_BG};
      border: 1px solid {BORDER};
      border-radius: 20px;
      padding: 26px 30px;
      backdrop-filter: blur(28px);
      box-shadow: 0 16px 40px rgba(0,0,0,0.12);
      transition: transform 0.4s cubic-bezier(0.2, 0.9, 0.3, 1.2), box-shadow 0.4s ease, border-color 0.4s ease;
      cursor: pointer;
    }}

    /* Left Card */
    .fcard.fc1 {{
      width: 310px; left: 2%; top: 20px;
      transform: rotateY(16deg) rotateX(6deg) translateZ(-10px);
      animation: f1 7s ease-in-out infinite;
      border-color: {'rgba(139,105,20,0.45)' if is_light else 'rgba(91,141,239,0.35)'};
    }}
    .fcard.fc1:hover {{
      animation-play-state: paused !important;
      transform: rotateY(10deg) rotateX(2deg) translateZ(60px) translateY(-14px) scale(1.06) !important;
      box-shadow: 0 30px 75px rgba(0,0,0,0.32) !important;
      z-index: 50 !important;
    }}

    /* Center Card (Preserves translateX(-50%) so it never shifts sideways!) */
    .fcard.fc2 {{
      width: 350px; left: 50%; top: 0;
      transform: translateX(-50%) rotateX(-4deg) translateZ(50px) scale(1.05);
      animation: f2 8s ease-in-out infinite;
      border-color: {'rgba(120,80,160,0.6)' if is_light else 'rgba(167,139,250,0.5)'};
      background: {'rgba(255,255,255,0.98)' if is_light else 'rgba(14,18,34,0.98)'};
      z-index: 2;
    }}
    .fcard.fc2:hover {{
      animation-play-state: paused !important;
      transform: translateX(-50%) rotateX(-1deg) translateZ(110px) translateY(-18px) scale(1.08) !important;
      box-shadow: 0 34px 85px rgba(0,0,0,0.38) !important;
      z-index: 50 !important;
    }}

    /* Right Card */
    .fcard.fc3 {{
      width: 300px; right: 2%; top: 30px;
      transform: rotateY(-16deg) rotateX(6deg) translateZ(-10px);
      animation: f3 9s ease-in-out infinite;
      border-color: {'rgba(60,140,100,0.45)' if is_light else 'rgba(74,222,128,0.35)'};
    }}
    .fcard.fc3:hover {{
      animation-play-state: paused !important;
      transform: rotateY(-10deg) rotateX(2deg) translateZ(60px) translateY(-14px) scale(1.06) !important;
      box-shadow: 0 30px 75px rgba(0,0,0,0.32) !important;
      z-index: 50 !important;
    }}

    @keyframes f1 {{
      0%, 100% {{ transform: rotateY(16deg) rotateX(6deg) translateZ(-10px) translateY(0) scale(1); }}
      50% {{ transform: rotateY(12deg) rotateX(4deg) translateZ(20px) translateY(-16px) scale(1.03); }}
    }}
    @keyframes f2 {{
      0%, 100% {{ transform: translateX(-50%) rotateX(-4deg) translateZ(50px) translateY(0) scale(1.05); }}
      50% {{ transform: translateX(-50%) rotateX(-7deg) translateZ(90px) translateY(-22px) scale(1.10); }}
    }}
    @keyframes f3 {{
      0%, 100% {{ transform: rotateY(-16deg) rotateX(6deg) translateZ(-10px) translateY(0) scale(1); }}
      50% {{ transform: rotateY(-12deg) rotateX(4deg) translateZ(20px) translateY(-14px) scale(1.03); }}
    }}

    /* Card Details */
    .cr {{ font-size: 0.78rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: {ACCENT}; margin-bottom: 8px; text-align: left; }}
    .cn {{ font-size: 1.15rem; font-weight: 700; color: {TEXT}; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: left; }}
    .ca {{ font-size: 0.88rem; color: {MUTED}; margin-bottom: 14px; text-align: left; font-weight: 500; }}
    .ct {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }}
    .ctag {{ font-size: 0.78rem; font-weight: 700; padding: 5px 12px; border-radius: 24px; }}
    .t-r {{ background: {TAG_RENT_B}; color: {TAG_RENT_T}; }}
    .t-c {{ background: {TAG_COM_B}; color: {TAG_COM_T}; }}
    .t-b {{ background: {TAG_BED_B}; color: {TAG_BED_T}; }}
    .cs {{ display: flex; justify-content: space-between; align-items: flex-end; }}
    .cnum {{ font-family: 'Fraunces', serif; font-size: 2.3rem; font-weight: 900; line-height: 1; }}
    .clbl {{ font-size: 0.72rem; color: {MUTED}; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 3px; font-weight: 600; }}
    .cbadge {{ font-size: 0.78rem; font-weight: 700; padding: 5px 12px; border-radius: 24px; }}

    .s-divider {{
      height: 1px;
      background: linear-gradient(to right, transparent, {DIVIDER}, {DIVIDER}, {DIVIDER}, transparent);
      position: relative; z-index: 1;
    }}

    section.inner {{
      position: relative; z-index: 1;
      padding: 120px 32px;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      text-align: center !important;
    }}

    .eyebrow {{
      font-size: 0.84rem; font-weight: 700;
      letter-spacing: 0.18em; text-transform: uppercase;
      margin-bottom: 22px;
      text-align: center !important;
    }}

    
    .section-h, .cta-h {{
      font-family: 'Fraunces', serif !important;
      font-size: clamp(3.2rem, 7.8vw, 6.5rem) !important;
      font-weight: 900 !important;
      letter-spacing: -0.04em !important;
      line-height: 1.0 !important;
      text-align: center !important;
      width: 100% !important;
      color: {TEXT} !important;
      max-width: 950px !important;
      margin: 0 auto 26px !important;
      display: block !important;
    }}

    .section-h .grad, .cta-h .grad {{
      background: {GRAD_TEXT} !important;
      -webkit-background-clip: text !important;
      -webkit-text-fill-color: transparent !important;
      background-clip: text !important;
      font-style: italic !important;
      font-weight: 400 !important;
      display: block !important;
      text-align: center !important;
    }}

    .section-p, .cta-sub {{
      font-size: 1.25rem !important;
      color: {TEXT2} !important;
      text-align: center !important;
      max-width: 660px !important;
      margin: 0 auto 52px !important;
      line-height: 1.72 !important;
      font-weight: 450 !important;
      display: block !important;
    }}

    .problem-grid {{
      display: grid; grid-template-columns: repeat(3, 1fr);
      gap: 24px; max-width: 980px; width: 100%;
      margin-top: 20px;
    }}
    .prob-card {{
      background: {PAIN_BG};
      border: 1px solid {PAIN_BORD};
      border-radius: 20px;
      padding: 36px 30px;
      text-align: left;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    .prob-card:hover {{
      transform: translateY(-8px) scale(1.03);
      box-shadow: 0 16px 44px rgba(0,0,0,0.12);
    }}
    .prob-num {{
      font-family: 'Fraunces', serif;
      font-size: 3.4rem; font-weight: 900; line-height: 1;
      color: {PAIN_NUM}; margin-bottom: 12px;
    }}
    .prob-title {{ font-size: 1.15rem; font-weight: 700; color: {TEXT}; margin-bottom: 10px; }}
    .prob-desc {{ font-size: 0.98rem; color: {TEXT2}; line-height: 1.65; font-weight: 400; }}

    .feat-grid {{
      display: grid; grid-template-columns: repeat(3, 1fr);
      gap: 24px; max-width: 1060px; width: 100%;
      margin-top: 20px;
    }}
    .feat-card {{
      background: {FEAT_BG};
      border: 1px solid {FEAT_BORD};
      border-radius: 22px;
      padding: 34px 30px;
      text-align: left;
      transition: transform 0.3s cubic-bezier(0.2, 0.9, 0.3, 1.2), border-color 0.3s, box-shadow 0.3s;
    }}
    .feat-card:hover {{
      transform: translateY(-8px) scale(1.04);
      border-color: {ACCENT};
      box-shadow: 0 20px 50px {BTN_GLOW};
    }}
    .feat-ico {{
      width: 52px; height: 52px;
      border-radius: 14px;
      display: flex; align-items: center; justify-content: center;
      font-size: 1.45rem; margin-bottom: 20px;
      background: {'rgba(139,105,20,0.14)' if is_light else 'rgba(91,141,239,0.14)'};
    }}
    .feat-name {{
      font-family: 'Fraunces', serif;
      font-size: 1.22rem; font-weight: 700;
      color: {TEXT}; margin-bottom: 12px;
    }}
    .feat-desc {{ font-size: 0.98rem; color: {TEXT2}; line-height: 1.68; font-weight: 400; }}

    .cta-section {{
      padding: 140px 32px 110px;
      text-align: center !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: center !important;
      position: relative; z-index: 1;
      width: 100% !important;
    }}

    .cta-btn {{
      display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 14px !important;
      background: {BTN_BG} !important; color: #fff !important;
      font-family: 'DM Sans', sans-serif !important;
      font-size: 1.18rem !important; font-weight: 600 !important;
      padding: 22px 56px !important; border-radius: 100px !important;
      text-decoration: none !important;
      box-shadow: 0 0 65px {BTN_GLOW} !important;
      transition: transform 0.28s cubic-bezier(0.2, 0.9, 0.3, 1.2), box-shadow 0.28s ease !important;
      cursor: pointer !important;
      margin: 0 auto !important;
    }}
    .cta-btn:hover {{
      transform: translateY(-5px) scale(1.05) !important;
      box-shadow: 0 0 95px {BTN_GLOW} !important;
    }}

    .proof-row {{
      display: flex !important; gap: 64px !important; justify-content: center !important; align-items: center !important;
      margin-top: 80px !important; padding-top: 60px !important;
      border-top: 1px solid {BORDER} !important;
      width: 100% !important; max-width: 860px !important;
    }}
    .proof-item {{ text-align: center !important; }}
    .proof-n {{
      font-family: 'Fraunces', serif;
      font-size: 2.8rem; font-weight: 900;
      color: {STAT_NUM}; line-height: 1;
      text-align: center !important;
    }}
    .proof-l {{
      font-size: 0.88rem; color: {MUTED};
      margin-top: 6px; text-transform: uppercase; letter-spacing: 0.08em;
      text-align: center !important; font-weight: 600;
    }}

    button[key="landing_theme"] {{
      position: fixed !important;
      bottom: 24px !important;
      right: 24px !important;
      z-index: 99999 !important;
      background: {SURFACE} !important;
      border: 1px solid {BORDER} !important;
      color: {TEXT} !important;
      border-radius: 100px !important;
      padding: 12px 24px !important;
      font-size: 0.92rem !important;
      font-weight: 600 !important;
      white-space: nowrap !important;
      width: auto !important;
      box-shadow: 0 6px 28px rgba(0,0,0,0.22) !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      transition: transform 0.2s ease !important;
    }}
    button[key="landing_theme"]:hover {{
      transform: scale(1.05) !important;
    }}

    @keyframes zoomInUp {{
      0% {{ opacity: 0; transform: translateY(35px) scale(0.93); }}
      100% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}

    /* ── SCROLL-DRIVEN POP-IN ANIMATIONS ─────────────────────────────────────── */
    @supports (animation-timeline: view()) {{
      @keyframes scrollPop {{
        0% {{
          opacity: 0;
          transform: translateY(60px) scale(0.88);
          filter: blur(5px);
        }}
        100% {{
          opacity: 1;
          transform: translateY(0) scale(1);
          filter: blur(0px);
        }}
      }}

      @keyframes scrollPopStagger1 {{
        0% {{ opacity: 0; transform: translateY(60px) scale(0.86); }}
        100% {{ opacity: 1; transform: translateY(0) scale(1); }}
      }}

      @keyframes scrollPopStagger2 {{
        0% {{ opacity: 0; transform: translateY(75px) scale(0.84); }}
        100% {{ opacity: 1; transform: translateY(0) scale(1); }}
      }}

      @keyframes scrollPopStagger3 {{
        0% {{ opacity: 0; transform: translateY(90px) scale(0.82); }}
        100% {{ opacity: 1; transform: translateY(0) scale(1); }}
      }}

      .pop-in {{
        animation: scrollPop ease-out both;
        animation-timeline: view();
        animation-range: entry 5% cover 30%;
      }}

      .pop-card-1 {{
        animation: scrollPopStagger1 ease-out both;
        animation-timeline: view();
        animation-range: entry 4% cover 28%;
      }}
      .pop-card-2 {{
        animation: scrollPopStagger2 ease-out both;
        animation-timeline: view();
        animation-range: entry 8% cover 32%;
      }}
      .pop-card-3 {{
        animation: scrollPopStagger3 ease-out both;
        animation-timeline: view();
        animation-range: entry 12% cover 36%;
      }}

      .pop-feat {{
        animation: scrollPop ease-out both;
        animation-timeline: view();
        animation-range: entry 6% cover 32%;
      }}

      .pop-cta {{
        animation: scrollPop ease-out both;
        animation-timeline: view();
        animation-range: entry 8% cover 34%;
      }}

      .pop-proof {{
        animation: scrollPop ease-out both;
        animation-timeline: view();
        animation-range: entry 4% cover 24%;
      }}
    }}

    @media(max-width: 768px) {{
      .problem-grid, .feat-grid {{ grid-template-columns: 1fr; }}
      .proof-row {{ flex-wrap: wrap; gap: 32px; }}
      .stage {{ display: none; }}
      .hero {{ padding-top: 60px; }}
      section.inner {{ padding: 70px 20px; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    
    raw_html = f"""<div class="orb o1"></div>
<div class="orb o2"></div>
<div class="orb o3"></div>
<div class="orb o4"></div>
<div class="grid-floor"></div>
<section class="hero">
<div class="hero-kicker">Built for Gurgaon &amp; Faridabad and Delhi-NCR &nbsp;·&nbsp; 100+ verified listings &nbsp;·&nbsp; Zero broker calls</div>
<h1 class="hero-h1"><span class="w1">Stop scrolling.</span><span class="w2">Start moving in.</span></h1>
<p class="hero-sub">Forty tabs, a dozen broker calls, and still no idea what your commute would look like. We killed that. One score per apartment — rent, commute, everything that matters — so the right flat finds you first.</p>
<a class="hero-btn" href="#problem">See how it works <span class="arr">↓</span></a>
<div class="stage">
<div class="fcard fc1">
<div class="cr">#2 match</div>
<div class="cn">Green View Apartments</div>
<div class="ca">📍 Sector 46, Gurgaon</div>
<div class="ct"><span class="ctag t-r">₹35,000/mo</span><span class="ctag t-c">🚗 9 min</span><span class="ctag t-b">🛏 2 BHK</span></div>
<div class="cs"><div><div class="cnum" style="color:{SCORE_MID}">79.2</div><div class="clbl">match score</div></div></div>
</div>
<div class="fcard fc2">
<div class="cr" style="color:{'#6b4f2a' if is_light else '#a78bfa'}">✦ best match</div>
<div class="cn">Sector 46 PG Single Room</div>
<div class="ca">📍 Sector 46, Gurgaon, Haryana</div>
<div class="ct"><span class="ctag t-r">₹9,000/mo</span><span class="ctag t-c">🚗 9 min</span><span class="ctag t-b">🛏 1 BHK</span></div>
<div class="cs"><div><div class="cnum" style="color:{SCORE_HI}">90.3</div><div class="clbl">match score</div></div><span class="cbadge" style="background:{'#d1fae5' if is_light else '#052e1c'};color:{SCORE_HI}">Best value ↑</span></div>
</div>
<div class="fcard fc3">
<div class="cr" style="color:{'#2d7a4f' if is_light else '#4ade80'}">#3 match</div>
<div class="cn">NIT Faridabad 2BHK</div>
<div class="ca">📍 NIT Faridabad, Haryana</div>
<div class="ct"><span class="ctag t-r">₹13,000/mo</span><span class="ctag t-c">🚗 34 min</span><span class="ctag t-b">🛏 2 BHK</span></div>
<div class="cs"><div><div class="cnum" style="color:{SCORE_MID}">71.8</div><div class="clbl">match score</div></div></div>
</div>
</div>
</section>
<div class="s-divider"></div>
<section class="inner" id="problem">
<div class="eyebrow pop-in" style="color:{EYEBROW_P}">The real problem</div>
<h2 class="section-h pop-in">Every listing site in NCR <span class="grad">forgot you have a life.</span></h2>
<p class="section-p pop-in">Ten tabs open, three brokers on hold, and still no clue what the commute actually costs you. We got tired of hunting for a flat like it was a part-time job — so we built the tool that does the hunting for you.</p>
<div class="problem-grid">
<div class="prob-card pop-card-1">
<div class="prob-num">40+</div>
<div class="prob-title">Hours lost per search</div>
<div class="prob-desc">The average NCR apartment search takes 6 weeks and over 40 hours of tab-switching, calling, and revisiting the same listings.</div>
</div>
<div class="prob-card pop-card-2">
<div class="prob-num">0</div>
<div class="prob-title">Sites show your commute</div>
<div class="prob-desc">Not one major listing platform calculates real driving time from your office or college to each apartment. We do.</div>
</div>
<div class="prob-card pop-card-3">
<div class="prob-num">No</div>
<div class="prob-title">Way to rank by fit</div>
<div class="prob-desc">Rent is visible. Commute is invisible. Tradeoffs are impossible. We score every apartment on what actually matters to you.</div>
</div>
</div>
</section>
<div class="s-divider"></div>
<section class="inner" id="features">
<div class="eyebrow pop-in" style="color:{EYEBROW_S}">What we built</div>
<h2 class="section-h pop-in">Everything you need to decide, <span class="grad">nothing you don't.</span></h2>
<p class="section-p pop-in">Not another listing site to scroll through. A decision engine — built for students and professionals who want the answer, not another tab.</p>
<div class="feat-grid">
<div class="feat-card pop-feat">
<div class="feat-ico">📊</div>
<div class="feat-name">Match Score</div>
<div class="feat-desc">Every apartment gets a 0–100 score. Drag the slider to say whether rent or commute matters more — the ranking updates instantly.</div>
</div>
<div class="feat-card pop-feat">
<div class="feat-ico">🤖</div>
<div class="feat-name">AI Assistant</div>
<div class="feat-desc">Tell it what you need in plain language. "2BHK under ₹20k near Cyber City." It searches, explains, and recommends — conversationally.</div>
</div>
<div class="feat-card pop-feat">
<div class="feat-ico">📍</div>
<div class="feat-name">Near Me</div>
<div class="feat-desc">Enter your college or office. We call a live maps API and re-rank every apartment by real driving time from your exact location.</div>
</div>
<div class="feat-card pop-feat">
<div class="feat-ico">⚖️</div>
<div class="feat-name">Compare Side by Side</div>
<div class="feat-desc">Pick any 2 or 3 apartments. See rent, commute, bedrooms, score, and notes in one table — best value highlighted automatically.</div>
</div>
<div class="feat-card pop-feat">
<div class="feat-ico">🔗</div>
<div class="feat-name">One-Click Listings</div>
<div class="feat-desc">Every card links directly to 99acres, MagicBricks, NoBroker, and Google Maps. Verify and contact — without leaving the flow.</div>
</div>
<div class="feat-card pop-feat">
<div class="feat-ico">🌙</div>
<div class="feat-name">Built to Last</div>
<div class="feat-desc">SQLite database, dark and light mode, multi-page architecture, and an admin panel. Production-quality, not a weekend prototype.</div>
</div>
</div>
</section>
<div class="s-divider"></div>
<section class="cta-section" id="cta">
<div class="eyebrow pop-in" style="color:{EYEBROW_S}">No login. No broker. No waiting.</div>
<h2 class="cta-h pop-in">Your next flat <span class="grad">is one search away.</span></h2>
<p class="cta-sub pop-in">35+ apartments across NCR, ranked instantly by what you care about. Free, open, and ready right now.</p>
<a class="cta-btn pop-cta" href="?enter=1" target="_self">Find your apartment <span class="arr">→</span></a>
<div class="proof-row pop-proof">
<div class="proof-item"><div class="proof-n">100+</div><div class="proof-l">Apartments listed</div></div>
<div class="proof-item"><div class="proof-n">Live</div><div class="proof-l">Commute data</div></div>
<div class="proof-item"><div class="proof-n">9</div><div class="proof-l">Pages of tools</div></div>
<div class="proof-item"><div class="proof-n">Free</div><div class="proof-l">No account needed</div></div>
</div>
</section>"""

    st.markdown(raw_html, unsafe_allow_html=True)

   
    theme_label = "☀️ Light" if not is_light else "🌙 Dark"
    if st.button(theme_label, key="landing_theme"):
        st.session_state["theme"] = "light" if not is_light else "dark"
        st.rerun()

if __name__ == "__main__":
    try:
        st.set_page_config(
            page_title="Apartment Finder — NCR",
            page_icon="Image.png",
            layout="wide",
            initial_sidebar_state="collapsed",
        )
    except Exception:
        pass
    render_landing()