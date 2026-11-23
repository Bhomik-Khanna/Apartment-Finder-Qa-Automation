# Formal Defect & Bug Reports Log

---

### BUG-001: Distinct Gurgaon Sector Addresses Resolve to 0-Minute Commute
- **Bug ID**: BUG-001
- **Severity**: Critical (P1)
- **Status**: Resolved & Guarded
- **Affected Page**: `pages/2_Manage.py`, `distance_api.py`
- **Regression Guard**: `tests/unit/test_commute.py::test_bug_001_distinct_sectors_do_not_yield_zero_commute`
- **Symptom**: When calculating commute between distinct addresses (e.g. Faridabad Station and Sector 56, Gurgaon), the duration returned was `0 minutes`.
- **Root Cause**: The geocoder query did not include the state and district boundary, causing OpenRouteService to truncate the query and return identical city-centroid coordinates for both origin and destination.
- **Fix Implemented**: Appended locality qualification (`"Faridabad/Gurgaon, Haryana, India"`) to address strings before dispatching geocoding requests.
- **Verification**: Mock directions test asserts driving duration is strictly $> 0$ minutes.

---

### BUG-002: Geocoder Drops Sector Precision in Favor of Broad City Center
- **Bug ID**: BUG-002
- **Severity**: High (P2)
- **Status**: Resolved & Guarded
- **Affected Page**: `distance_api.py`
- **Regression Guard**: `tests/unit/test_geocoding.py::test_bug_002_geocoder_preserves_sector_precision`
- **Symptom**: Querying "Sector 48, Faridabad" returned the Faridabad city center coordinates `(77.318, 28.411)` rather than the Sector 48 coordinates `(77.2915, 28.3682)`.
- **Root Cause**: Confidence scoring threshold did not inspect whether `locality` vs `neighbourhood/street` level precision was returned by the GeoJSON properties.
- **Fix Implemented**: Added explicit validation checking `locality` and sector identifiers in feature properties.
- **Verification**: Coordinates are asserted to not equal city center centroid.

---

### BUG-003: Case-Sensitive Duplicate Name Bypass Allows Duplicate Listings
- **Bug ID**: BUG-003
- **Severity**: Medium (P2)
- **Status**: Resolved & Guarded
- **Affected Page**: `pages/2_Manage.py`, `storage.py`
- **Regression Guard**: `tests/unit/test_bug_probes.py::test_bug_003_case_insensitive_duplicate_detection`
- **Symptom**: When "Palm Grove Residency" already existed, a user could add `"palm grove residency"` (lowercase) or `"  Palm Grove Residency  "` (trailing spaces) without triggering duplicate rejection.
- **Root Cause**: The duplicate check performed a literal string equality comparison `new_name == existing.name` without normalization.
- **Fix Implemented**: Normalized both existing and input names using `.strip().lower()` before comparing.
- **Verification**: Test checks that lowercase and padded strings are flagged as duplicates.

---

### BUG-004: Negative Rent Input Produces Absurd Match Score Greater Than 100%
- **Bug ID**: BUG-004
- **Severity**: High (P2)
- **Status**: Resolved & Guarded
- **Affected Page**: `apartment.py`, `pages/2_Manage.py`
- **Regression Guard**: `tests/unit/test_bug_probes.py::test_bug_004_negative_rent_boundary_rejection`
- **Symptom**: Entering a negative rent like `-15,000` resulted in a rent score of `(1 - (-15000)/80000) * 100 = 118.75%`, corrupting ranking order.
- **Root Cause**: Lack of boundary validation on input fields and normalization math.
- **Fix Implemented**: Added input validation `rent > 0` and clamped normalization scores with `max(0.0, min(100.0, score))`.
- **Verification**: Score is strictly asserted to never exceed `100.0`.

---

### BUG-005: Whitespace-Only Apartment Names Create Ghost Cards
- **Bug ID**: BUG-005
- **Severity**: Medium (P3)
- **Status**: Resolved & Guarded
- **Affected Page**: `pages/2_Manage.py`
- **Regression Guard**: `tests/unit/test_bug_probes.py::test_bug_005_whitespace_only_name_rejection`
- **Symptom**: A user could enter `"   "` (spaces) as a name and submit the form, creating a blank, unclickable card on the dashboard.
- **Root Cause**: Input validated `if name:` which evaluates to `True` for non-empty space strings.
- **Fix Implemented**: Updated validation to `if not name or not name.strip(): raise ValidationError`.
- **Verification**: Test asserts whitespace-only names are rejected with validation warning.