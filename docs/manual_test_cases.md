# Apartment Finder — 25 Manual QA Test Cases

| TC ID | Module / Page | Test Case Description | Preconditions | Test Steps | Test Data | Expected Result | Priority |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Landing Gate | Access root without gate parameter | Fresh browser session | 1. Open `http://localhost:8501`.<br>2. Observe rendered page. | URL: `/` | 3D isometric landing page displays; dashboard is hidden. | High |
| **TC-02** | Landing Gate | Transition through gate | On Landing Page | 1. Click "Find your apartment →". | Click event | URL updates to `?enter=1`; dashboard unlocks. | Critical |
| **TC-03** | Landing Gate | Return to Landing Page | Main Dashboard | 1. In sidebar, click "← Back to Landing Page". | Click event | User returns to landing page; dashboard re-locks. | Medium |
| **TC-04** | Dashboard | Rent vs Commute slider shift | Dashboard loaded | 1. Drag slider to 90% Rent.<br>2. Note top apartment.<br>3. Drag slider to 90% Commute. | Slider: `0.9` & `0.1` | Rankings re-order dynamically; top listing updates. | Critical |
| **TC-05** | Dashboard | Area filter buttons | Dashboard loaded | 1. Click "Sector 15 Market" button.<br>2. Check listings. | Area: `Sector 15` | Only Sector 15 listings render; other sectors hidden. | High |
| **TC-06** | Dashboard | Max Rent filter boundary | Dashboard loaded | 1. Adjust Max Rent slider to ₹15,000. | Max Rent: `15000` | No apartments with rent > ₹15,000 appear. | High |
| **TC-07** | Dashboard | Max Commute filter boundary | Dashboard loaded | 1. Adjust Max Commute slider to 20 min. | Max Commute: `20` | No apartments with commute > 20 min appear. | High |
| **TC-08** | Dashboard | Zero search results empty state | Dashboard loaded | 1. Set Max Rent to ₹1,000. | Max Rent: `1000` | Clean empty state card with icon & guidance renders. | Medium |
| **TC-09** | Dashboard | Matplotlib chart score coloring | Dashboard loaded | 1. Scroll to "Top apartments at a glance". | 2+ listings | Bars colored Green (≥65), Amber (≥40), Red (<40). | Medium |
| **TC-10** | Compare | Minimum apartments guard | < 2 apartments saved | 1. Navigate to `1_Compare.py`. | Database with 1 apt | Warning: "Need at least 2 apartments" displays. | Medium |
| **TC-11** | Compare | Compare 2 apartments side-by-side | 2+ listings saved | 1. Select Apt A and Apt B from selectboxes. | Apt A & Apt B | Side-by-side cards display with matching badges. | High |
| **TC-12** | Compare | Highlight winner metric cells | Compare loaded | 1. Observe comparison table. | Differing rents/times | Cheaper rent, shorter commute, higher score highlighted in green (`cmp-winner`). | High |
| **TC-13** | Compare | Optional Apartment C selection | Compare loaded | 1. Select Apt C from third dropdown. | Apt C | Table expands to 3 columns with winner re-calculated. | Medium |
| **TC-14** | Manage | Add valid apartment | On `2_Manage.py` | 1. Fill Name, Address, Rent, Beds.<br>2. Click Add. | Valid inputs | Commute auto-calculates; listing appears in table. | Critical |
| **TC-15** | Manage | Duplicate name rejection | Existing apt present | 1. Enter identical existing name.<br>2. Click Add. | Name: `"Palm Grove"` | Warning: "Already exists"; duplicate entry blocked. | High |
| **TC-16** | Manage | Case-insensitive duplicate rejection | Existing apt present | 1. Enter lowercase existing name.<br>2. Click Add. | Name: `"palm grove"` | Duplicate blocked regardless of casing. | High |
| **TC-17** | Manage | Negative rent rejection | On `2_Manage.py` | 1. Enter Rent: `-15000`.<br>2. Click Add. | Rent: `-15000` | Form validation error; entry blocked. | High |
| **TC-18** | Manage | Whitespace-only name rejection | On `2_Manage.py` | 1. Enter Name: `"   "`.<br>2. Click Add. | Name: `"   "` | Error: "Name cannot be empty"; entry blocked. | Medium |
| **TC-19** | Near Me | Quick location selection | On `4_Near_Me.py` | 1. Click "NIT Faridabad" button. | Quick-pick click | Address auto-populates; commute times calculated. | High |
| **TC-20** | Near Me | Custom address ranking | On `4_Near_Me.py` | 1. Type "Cyber City, Gurugram".<br>2. Click Find. | Custom location | Re-ranks apartments by live commute from Cyber City. | Critical |
| **TC-21** | AI Assistant | Chat recommendation query | On `5_AI_Assistant.py` | 1. Type "Find a 2BHK under ₹25k". | Natural text query | Assistant recommends existing listings from dataset. | High |
| **TC-22** | AI Assistant | Direct apartment addition via chat | On `5_AI_Assistant.py` | 1. Tell assistant to add an apartment.<br>2. Confirm details. | Conversational flow | Assistant emits `NEW_APARTMENT:`; listing saved. | High |
| **TC-23** | AI Assistant | Anonymous feedback collection | Conversation winding down | 1. Provide rating "5" and review text. | Feedback flow | Assistant emits `FEEDBACK_COLLECTED:`; saved to SQLite. | Medium |
| **TC-24** | Theme | Dark & Light theme toggle | Settings / Theme switch | 1. Switch between Dark and Light mode. | Toggle event | Obsidian/Gold switches to Linen/Bronze; high contrast maintained. | Medium |
| **TC-25** | Admin | Password protected access | On `7_Admin.py` | 1. Enter wrong password.<br>2. Enter correct password. | `admin123` | Access denied on wrong password; granted on correct. | High |