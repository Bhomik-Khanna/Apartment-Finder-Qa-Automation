Apartment Finder QA Automation Framework



Automated and manual QA for Apartment Finder, a Streamlit app that ranks rental apartments in Delhi NCR by balancing monthly rent against driving commute time. This repository contains the app and a five-layer test suite around it: 36 automated tests, 5 documented and regression-guarded defects, and a manual QA package (test plan, 25 test cases, bug reports).

At a glance
Metric	Value	How to verify
Automated tests	36	pytest --collect-only -q
Offline tests (unit, data, regression, AppTest)	33, about 6.1 s	pytest -m "not e2e"
Browser E2E tests (Playwright, Chromium)	3, about 24.7 s (headed)	pytest -m e2e --headed
Result	36 passed, 0 failed	same commands
Stability	No flaky failures in 10 consecutive local runs	repeat the offline command 10 times
Code coverage	<XX>%	pytest -m "not e2e" --cov=Apartment-Finder --cov-report=term-missing
Defects found and root-caused	5	docs/bug_reports.md
Manual test cases	25	docs/manual_test_cases.md

No real API keys are needed to run the tests. External services are mocked and the test fixtures use dummy keys (see tests/conftest.py).

About the application

Apartment Finder starts on a landing page and unlocks a dashboard (?enter=1). Listings are scored from 0 to 100 using rent and the driving commute from Faridabad Railway Station, with a slider that shifts the weight between the two:

score = ((1 - rent / max_rent) * rent_weight + (1 - commute / max_commute) * commute_weight) * 100
max_rent = 80,000 INR     max_commute = 120 minutes     rent_weight + commute_weight = 1

Pages: Compare, Manage (add listings), About, Near Me (re-rank by your own address), AI Assistant (Google Gemini), Analytics, Admin (password protected), Settings. Data: apartments.json for listings and SQLite for feedback. External services: OpenRouteService (geocoding and commute times) and Google Gemini. Stack: Python 3.11+, Streamlit, Matplotlib.

Test strategy
Layer	Tooling	What it covers
1. Unit	pytest, responses	Scoring math and boundaries, commute and geocoding logic, Gemini action-tag parsing (malformed tags, missing fields, junk values), SQLite feedback storage, entry gate and Admin password logic
2. Regression	pytest	One guard test per documented defect (BUG-001 to BUG-005)
3. Data checks	pytest, jsonschema	Required fields, types, realistic NCR rent and commute ranges, duplicate names in apartments.json
4. AppTest	Streamlit AppTest	Every page runs without exceptions; multi-step flows: add apartment, duplicate rejection, Compare highlighting, Near Me re-ranking
5. Browser E2E	Playwright (Chromium)	Landing page to dashboard transition and navigation, through page objects
Why AppTest for the API-dependent flows

Playwright drives a browser against a separate Streamlit server process, so an HTTP mocking library running in the test process cannot intercept the app's calls to OpenRouteService. Streamlit's AppTest runs the app in the same process, so responses can serve fake geocoding and routing responses. Those flows run offline, deterministically, and without using up the free-tier request quota.

Design
Adapter layer (tests/adapter.py): the unit, data and AppTest layers import app functions, UI labels, file paths and data contracts from one file. If an app function or label is renamed, that file is the place to update.
Page Object Model (tests/e2e/pages/): LandingPage and HomePage hold the locators and actions for the browser tests, so the E2E tests contain no raw selectors.
Deterministic mocks (tests/ors_mocks.py): fake OpenRouteService geocoding, matrix and directions responses.
Isolated data: tests that modify listings or the database work on temporary copies, so real data is never touched.
Defects found
ID	Symptom	Root cause	Fix	Guard test
BUG-001	Different Gurgaon sectors showed a 0-minute commute	Geocoder query had no state or country bounding, so origin and destination resolved to the same city-centre point	Added state and country context to geocoding queries	test_bug_001_distinct_sectors_do_not_yield_zero_commute
BUG-002	Sector-level precision lost; broad city centroid returned	Parser accepted low-confidence locality results without checking for sector-level properties	Added sector-property verification when picking a geocoding result	test_bug_002_geocoder_preserves_sector_precision
BUG-003	"palm grove" accepted next to "Palm Grove"	Duplicate check compared raw strings	Normalise names with .strip().lower() before comparing	test_bug_003_case_insensitive_duplicate_detection
BUG-004	Negative rent (-15,000) produced a match score of 118.75%	Normalisation was unclamped and negative values were accepted	Reject rent <= 0 and clamp scores to 0-100	test_bug_004_negative_rent_boundary_rejection
BUG-005	A whitespace-only name created an invisible listing card	if name: is true for strings of spaces	Reject names that are empty after .strip()	test_bug_005_whitespace_only_name_rejection

BUG-001 and BUG-002 are separate defects with separate fixes. BUG-001 is a query problem (missing bounding made two addresses collapse to one point), while BUG-002 is a result-selection problem (the parser accepted a city-level result when a sector-level one was needed).

Do the tests actually catch bugs? Manual mutation checks

I deliberately broke the code twice and confirmed the relevant tests failed.

Inverted rent scoring in apartment.py (higher rent gave a higher score). test_slider_weight_sensitivity failed with an assertion error.
Route collapse in mock data: Sector 56 coordinates set equal to the origin in tests/ors_mocks.py. The BUG-001 guard failed with "Distinct sector address resolved to 0-minute commute".

This was done by hand on two cases, not with an automated mutation-testing tool.

Manual QA package
docs/test_plan.md: scope, strategy, environments, risks, exit criteria
docs/manual_test_cases.md: 25 manual test cases
docs/bug_reports.md: formal reports and root-cause analyses for BUG-001 to BUG-005
Getting started

Prerequisites: Python 3.11 or newer and Git.

bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

pip install -r Apartment-Finder/requirements.txt   # the app's dependencies (adjust path if different)
pip install -r requirements-test.txt
playwright install chromium
Run the tests
Goal	Command	Time
Offline suite	pytest -m "not e2e"	~6 s
One layer	pytest -m unit, -m regression, -m data, -m apptest	seconds
Browser E2E (visible)	pytest -m e2e --headed --slowmo 500	~25 s
Coverage	pytest -m "not e2e" --cov=Apartment-Finder --cov-report=term-missing	~6 s
Run the app (optional)

Create .streamlit/secrets.toml (this file is git-ignored; never commit it):

toml
ORS_API_KEY = "your-openrouteservice-key"
GEMINI_API_KEY = "your-gemini-key"
bash
streamlit run Apartment-Finder/app.py
Continuous integration

GitHub Actions (.github/workflows/tests.yml) runs on every push and pull request to main:

Offline suite: unit, data, regression and AppTest layers on Ubuntu with Python 3.11.
Browser E2E: the Playwright tests in headless Chromium.

Test results are uploaded as workflow artifacts.

Known limitations
The live Gemini API is not exercised in CI (cost and non-deterministic output). The action-tag parser is tested instead.
The live OpenRouteService API is mocked, so real network latency, rate limits and API changes are not covered.
Chart rendering is checked for exceptions only. There is no visual (pixel) regression testing.
Admin login through the browser UI is covered by manual test TC-25, not by Playwright. The Admin password logic is unit tested.
Only 3 browser E2E tests exist, and they run on Chromium only. Other browsers are not tested.
Mutation checks were run by hand on two cases.
Repository structure
.
|-- Apartment-Finder/              the Streamlit app under test
|-- tests/
|   |-- adapter.py                 app bindings, UI labels, data contracts
|   |-- ors_mocks.py               fake OpenRouteService responses
|   |-- conftest.py                shared fixtures, dummy keys, seed data
|   |-- data/seed_apartments.json
|   |-- unit/                      scoring, commute, geocoding, Gemini parsing, SQLite, gate security, bug probes
|   |-- data_checks/               apartments.json contract tests
|   |-- apptest/                   headless Streamlit page and user-flow tests
|   `-- e2e/                       Playwright tests and page objects
|-- docs/                          test plan, manual test cases, bug reports
|-- tools/inventory.py             lists functions and pages to keep the adapter in sync
|-- .github/workflows/tests.yml    CI
|-- pytest.ini                     markers and settings
`-- requirements-test.txt
