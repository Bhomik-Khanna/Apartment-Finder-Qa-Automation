




import os
import streamlit as st
import requests
from theme import apply_theme, load_tracker, get_colors

st.set_page_config(
    page_title="AI Assistant — Apartment Finder",
    page_icon="🤖",
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

    st.markdown(f"""<div style="font-size:0.75rem;font-weight:600;
    color:{c['text']};margin-bottom:8px"> Chat options</div>""",
    unsafe_allow_html=True)

    if st.button("🗑 Clear conversation", use_container_width=True):
        st.session_state["chat_history"] = []
        st.session_state["feedback_collected"] = False
        st.rerun()

    st.markdown("---")
    st.markdown(f"""
    <div class="info-card" style="padding:12px 14px">
      <div class="info-title">What I can help with</div>
      <div class="info-body">
         Suggest apartments<br>
         Explain your match score<br>
         Compare areas<br>
         Answer app questions<br>
         Collect your feedback<br>
         Add new listings directly
      </div>
    </div>
    """, unsafe_allow_html=True)


def build_apartment_context():
    if not tracker.apartments:
        return "No apartments currently in the database."
    lines = [f"Total apartments in database: {len(tracker.apartments)}\n"]
    lines.append("APARTMENT LISTINGS:")
    lines.append("-" * 40)
    for apt in tracker.apartments:
        commute = f"{apt.commute_minutes} min" if apt.commute_minutes else "unknown"
        score   = apt.score()
        lines.append(
            f"Name: {apt.name}\n"
            f"  Address: {apt.address}\n"
            f"  Rent: Rs.{apt.rent:,}/month\n"
            f"  Bedrooms: {apt.bedrooms} BHK\n"
            f"  Commute from Faridabad Railway Station: {commute}\n"
            f"  Match score: {score}/100\n"
            f"  Notes: {apt.notes or 'None'}\n"
        )
    return "\n".join(lines)



def save_feedback(rating, review, suggestions):
    from storage import save_feedback as db_save
    return db_save(rating, review, suggestions)



def add_apartment_directly(apt_data):
    from storage import get_connection, apartment_exists
    from distance_api import get_commute_minutes
    from theme import ORIGIN_ADDRESS

    name     = apt_data.get("name", "").strip()
    address  = apt_data.get("address", "").strip()
    rent     = int(apt_data.get("rent", 0))
    bedrooms = int(apt_data.get("bedrooms", 0))
    notes    = apt_data.get("notes", "").strip()

    if not name or not address:
        return False, "Name and address are required"

    if apartment_exists(name, address):
        return False, f"'{name}' at this address already exists in the database"

    # Auto-fetch commute time
    commute = get_commute_minutes(ORIGIN_ADDRESS, address)

    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO apartments (name, address, rent, bedrooms, notes, commute_minutes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, address, rent, bedrooms, notes, commute))
        conn.commit()

        # Force tracker reload across all pages (safe string type check)
        for key in list(st.session_state.keys()):
            if key == "tracker" or (isinstance(key, str) and key.startswith("near_me_results_")):
                del st.session_state[key]

        comm_str = f"{commute} min" if commute else "unknown"
        return True, f"Added successfully with commute time {comm_str}"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()



def parse_response(text):
    feedback_data  = None
    apartment_data = None
    clean          = text

    if "FEEDBACK_COLLECTED:" in text:
        try:
            parts = text.split("FEEDBACK_COLLECTED:")
            clean = parts[0].strip()
            line  = parts[1].strip().split("\n")[0]

            def extract(key, src):
                if key + "=" not in src:
                    return ""
                val = src.split(key + "=")[1]
                other_keys = [k for k in ["rating", "review", "suggestions"]
                              if k != key and k + "=" in val]
                if other_keys:
                    val = val.split(other_keys[0] + "=")[0]
                return val.strip()

            feedback_data = {
                "rating":      int(extract("rating", line) or 0),
                "review":      extract("review", line),
                "suggestions": extract("suggestions", line),
            }
        except Exception:
            pass

    if "NEW_APARTMENT:" in text:
        try:
            parts = text.split("NEW_APARTMENT:")
            clean = parts[0].strip()
            line  = parts[1].strip().split("\n")[0]

            def extract(key, src):
                if key + "=" not in src:
                    return ""
                val = src.split(key + "=")[1]
                other_keys = [k for k in ["name", "address", "rent", "bedrooms", "notes"]
                              if k != key and k + "=" in val]
                if other_keys:
                    val = val.split(other_keys[0] + "=")[0]
                return val.strip()

            apartment_data = {
                "name":     extract("name", line),
                "address":  extract("address", line),
                "rent":     int(extract("rent", line) or 0),
                "bedrooms": int(extract("bedrooms", line) or 0),
                "notes":    extract("notes", line),
            }
        except Exception:
            pass

    return clean, feedback_data, apartment_data


# ── Call Gemini API ────────────────────────────────────────────────────────────
def call_gemini(messages):
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "GEMINI_API_KEY not found in your .env file. Please add it and restart Streamlit."

    system = f"""You are an AI assistant for the Apartment Finder app helping
students and professionals find apartments in the NCR region (Gurgaon and Faridabad).

PERSONALITY: Friendly, helpful, concise. You know the NCR rental market well.
Never ask for the user name — all interactions are fully anonymous.

THE APP HAS 9 PAGES:
1. Home — ranked list with filters and area buttons
2. Compare — pick 2-3 apartments side by side
3. Manage — add apartments (users cannot delete listings)
4. Near Me — enter your location, get real commute times from there
5. About — explains scoring and tech stack
6. AI Assistant — you are here
7. Analytics — feedback ratings and trends dashboard
8. Admin — for app owner only, password protected
9. Settings — theme and preferences

HOW SCORING WORKS:
Score 0-100 = (rent score x rent weight) + (commute score x commute weight)
Rent score = 1 minus rent divided by max rent in filters
Commute score = 1 minus commute minutes divided by max commute in filters
Default weights: 60 percent rent, 40 percent commute.
Green = 65 and above, Yellow = 40 to 64, Red = below 40.

AREAS WITH APARTMENT DATA:
Gurgaon: Sector 44, Sector 45, Sector 46, Sector 47, Sector 48
Faridabad: Old Faridabad, NIT Faridabad, Sector 15, Sector 21, Badkhal, Ballabhgarh

CURRENT APARTMENT DATABASE:
{build_apartment_context()}

YOUR FOUR TASKS:

TASK 1 - SUGGEST APARTMENTS:
When users describe what they want (budget, bedrooms, area, commute preference),
look through the apartment data above and recommend specific ones by name.
Always include: name, rent, commute time, match score, and why you recommend it.
Only suggest apartments that actually exist in the data above. Never make up listings.

TASK 2 - ANSWER APP QUESTIONS:
Explain how features work, how to navigate pages, how scoring is calculated, etc.

TASK 3 - ADD NEW APARTMENTS DIRECTLY TO DATABASE:
If a user mentions a society or apartment not in the database and wants to add it,
collect these details conversationally one step at a time:
  - Society or apartment name
  - Full address including area, city, and state — be specific for accurate GPS
  - Monthly rent in rupees — number only
  - Number of bedrooms
  - Any notes such as furnished or unfurnished, amenities, nearby metro, etc.
Confirm all details with the user before submitting.
Once they confirm, at the VERY END of your message on its own line write exactly:
NEW_APARTMENT: name=<name> address=<address> rent=<number> bedrooms=<number> notes=<notes>
The apartment goes directly into the live database — not for admin review.
Tell the user it has been added and they can see it on the Home page right now.

TASK 4 - COLLECT ANONYMOUS FEEDBACK AND RATING:
After helping someone successfully, or when the conversation is winding down,
ask for feedback in a natural friendly way — never as a formal survey.
Example: "Before you go — how would you rate your experience today? Just 1 to 5."
After they rate, ask: "Thanks! Anything we could do better?"
Never ask for their name or any personal details. Everything is anonymous.
Once you have a rating and their response, at the VERY END of your message on its own line write:
FEEDBACK_COLLECTED: rating=<number> review=<their exact words> suggestions=<their suggestions>
The feedback appears in Analytics and Admin automatically.

IMPORTANT RULES:
- Never invent apartment data. Only suggest what exists in the database above.
- Keep responses short and conversational. No long paragraphs.
- Use bullet points when listing apartments.
- All feedback is completely anonymous. Never store or mention personal details."""

    gemini_messages = []
    for msg in messages:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_messages.append({
            "role":  role,
            "parts": [{"text": msg["content"]}]
        })

    try:
        response = requests.post(
           f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
            headers={"Content-Type": "application/json"},
            json={
                "system_instruction": {"parts": [{"text": system}]},
                "contents":           gemini_messages,
                "generationConfig":   {
                    "maxOutputTokens": 1000,
                    "temperature":     0.7,
                },
            },
            timeout=60,
            verify=False,
        )
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except requests.exceptions.HTTPError as e:
        try:
            return f"API Error {e.response.status_code}: {e.response.json()}"
        except Exception:
            return f"API Error: {str(e)}"
    except (KeyError, IndexError):
        return "Unexpected response from Gemini. Please try again."
    except Exception as e:
        return f"Something went wrong: {str(e)}"



st.markdown("""
<div class="hero">
  <div class="hero-title">AI <span class="hero-accent">Assistant</span></div>
  <p class="hero-sub">Find apartments, get recommendations, add new listings — just by chatting</p>
</div>
""", unsafe_allow_html=True)


st.markdown(
    f'<div style="font-size:0.72rem;color:{c["muted"]};margin-bottom:8px">Try asking:</div>',
    unsafe_allow_html=True
)

suggestions = [
    "Find me a 2BHK under ₹25,000",
    "Which area has shortest commute?",
    "How is match score calculated?",
    "Best apartment for students",
    "I want to add a new apartment",
]

sug_cols = st.columns(len(suggestions))
for i, sug in enumerate(suggestions):
    if sug_cols[i].button(sug, key=f"sug_{i}", use_container_width=True):
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        st.session_state["pending_message"] = sug
        st.rerun()

st.markdown("---")


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "feedback_collected" not in st.session_state:
    st.session_state["feedback_collected"] = False

user_bg  = c["accent_bg"]
user_txt = c["accent"]
bot_bg   = c["surface"]
bot_txt  = c["text2"]


if not st.session_state["chat_history"]:
    st.markdown(f"""
    <div style="display:flex;justify-content:flex-start;margin-bottom:10px">
      <div style="background:{bot_bg};color:{bot_txt};padding:10px 14px;
      border:1px solid {c['border']};border-radius:14px 14px 14px 4px;
      max-width:75%;font-size:0.88rem;line-height:1.6">
        <span style="font-size:0.7rem;color:{c['muted']};display:block;margin-bottom:4px">
           AI Assistant
        </span>
        Hi! I'm your Apartment Finder assistant. I know all <b>{len(tracker)}</b> apartments
        in our database and can help you find the right one.<br><br>
        You can ask me things like:<br>
        • <b>"Find me a 1BHK under Rs.15,000 with short commute"</b><br>
        • <b>"Which area is best for students?"</b><br>
        • <b>"I want to add a new apartment to the database"</b><br><br>
        What are you looking for?
      </div>
    </div>
    """, unsafe_allow_html=True)


for msg in st.session_state["chat_history"]:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style="display:flex;justify-content:flex-end;margin-bottom:10px">
          <div style="background:{user_bg};color:{user_txt};padding:10px 14px;
          border-radius:14px 14px 4px 14px;max-width:70%;font-size:0.88rem;
          font-weight:500;line-height:1.5">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display:flex;justify-content:flex-start;margin-bottom:10px">
          <div style="background:{bot_bg};color:{bot_txt};padding:10px 14px;
          border:1px solid {c['border']};border-radius:14px 14px 14px 4px;
          max-width:75%;font-size:0.88rem;line-height:1.6">
            <span style="font-size:0.7rem;color:{c['muted']};display:block;margin-bottom:4px">
               AI Assistant
            </span>
            {msg["content"].replace(chr(10), "<br>")}
          </div>
        </div>
        """, unsafe_allow_html=True)


user_input = st.chat_input("Ask about apartments, add a listing, or anything else...")

if "pending_message" in st.session_state:
    user_input = st.session_state.pop("pending_message")


if user_input:
    st.session_state["chat_history"].append({
        "role": "user", "content": user_input
    })

    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state["chat_history"]
    ]

    with st.spinner("Thinking..."):
        raw = call_gemini(api_messages)

    clean, feedback_data, apartment_data = parse_response(raw)

    
    if feedback_data and not st.session_state["feedback_collected"]:
        if save_feedback(
            feedback_data.get("rating", 0),
            feedback_data.get("review", ""),
            feedback_data.get("suggestions", ""),
        ):
            st.session_state["feedback_collected"] = True
            clean += "\n\n✅ Your anonymous feedback has been saved — thank you!"

    
    if apartment_data:
        ok, msg = add_apartment_directly(apartment_data)
        if ok:
            clean += (
                f"\n\n✅ **{apartment_data.get('name', 'The apartment')}** "
                f"has been added to the database! "
                f"Find it on the Home page now."
            )
        else:
            clean += f"\n\n⚠️ Couldn't add the listing: {msg}"

    st.session_state["chat_history"].append({
        "role": "assistant", "content": clean
    })
    st.rerun()