# Apartment Finder QA Test Plan

## 1. Introduction
This test plan defines the testing strategy, tools, scope, and quality criteria for the **Apartment Finder ("Big 3 Rentals")** web application.

## 2. Test Scope
- **In-Scope**:
  - Algorithmic scoring accuracy (Rent vs. Commute balance).
  - OpenRouteService geospatial API integrations (reverse geocoding & matrix duration).
  - Multi-page routing, session persistence, and gate access controls (`?enter=1`, Admin auth).
  - Database CRUD operations and anonymous feedback collection.
  - Cross-browser compatibility (Chromium & Firefox).
- **Out-of-Scope**:
  - Enterprise load testing beyond 500 concurrent sessions.
  - Third-party listing platform uptime (99acres, MagicBricks).

## 3. Test Strategy & Quality Gates
- **Pyramid Distribution**:
  - 65% Unit & Data Tests (Instant feedback, pure math, offline ORS mocks).
  - 25% Headless AppTests (Streamlit runtime graph, widget events).
  - 10% Playwright E2E Tests (Visual verification in real browser engines).

## 4. Release Quality Criteria
1. **Pass Rate**: 100% on Unit, Data, Regression, and AppTest suites.
2. **Regression Guards**: All documented defects (BUG-001 through BUG-005) verified with automated tests.
3. **Zero Runtime Exceptions**: Zero unhandled Python tracebacks during user flows.
4. **CI Build Status**: Green builds on both Chromium and Firefox in GitHub Actions.