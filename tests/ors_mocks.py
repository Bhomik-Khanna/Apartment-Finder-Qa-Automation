

import re
import responses

ORS_GEOCODE_URL = re.compile(r"https://api\.openrouteservice\.org/geocode/search.*")
ORS_DIRECTIONS_URL = re.compile(r"https://api\.openrouteservice\.org/v2/directions/driving-car.*")
ORS_MATRIX_URL = re.compile(r"https://api\.openrouteservice\.org/v2/matrix/driving-car.*")

COORDINATES_MAP = {
    "Faridabad Railway Station": (77.3178, 28.4112),
    "Sector 48, Faridabad": (77.2915, 28.3682),
    "Sector 21C, Faridabad": (77.3021, 28.4230),
    "Sector 15, Faridabad": (77.3245, 28.4050),
    "Sector 56, Gurgaon": (77.1025, 28.4228),
    "Sector 43, Gurgaon": (77.0850, 28.4550),
}


def build_geocode_response(query: str, lon: float = 77.3178, lat: float = 28.4112, confidence: float = 0.9):
    """Builds a realistic GeoJSON feature collection matching ORS response spec."""
    return {
        "geocoding": {"query": query},
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": {
                    "label": f"Resolved: {query}",
                    "confidence": confidence,
                    "locality": "Faridabad",
                },
            }
        ],
    }


def build_directions_response(duration_seconds: float = 1080.0, distance_meters: float = 7200.0):
    """Builds a dual-format response satisfying both GeoJSON features and standard routes."""
    summary = {
        "duration": duration_seconds,
        "distance": distance_meters,
    }
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "summary": summary,
                    "segments": [{"duration": duration_seconds, "distance": distance_meters}],
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[77.3178, 28.4112], [77.2915, 28.3682]],
                },
            }
        ],
        "routes": [
            {
                "summary": summary,
                "segments": [{"duration": duration_seconds, "distance": distance_meters}],
            }
        ],
        "durations": [[0, int(duration_seconds)]],
        "distances": [[0, int(distance_meters)]],
    }


def register_standard_mocks(rsps: responses.RequestsMock):
    """Registers standard success mocks for ORS endpoints."""
    rsps.add_callback(
        responses.GET,
        ORS_GEOCODE_URL,
        callback=lambda req: (
            200,
            {},
            __import__("json").dumps(build_geocode_response(str(req.url or ""))),
        ),
    )
    rsps.add_callback(
        responses.GET,
        ORS_DIRECTIONS_URL,
        callback=lambda req: (
            200,
            {},
            __import__("json").dumps(build_directions_response(1080.0, 7200.0)),
        ),
    )
    rsps.add_callback(
        responses.POST,
        ORS_MATRIX_URL,
        callback=lambda req: (
            200,
            {},
            __import__("json").dumps({"durations": [[0, 1080]], "distances": [[0, 7200]]}),
        ),
    )