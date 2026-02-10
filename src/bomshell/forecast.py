from datetime import datetime

import requests

BOM_API_BASE = "https://api.weather.bom.gov.au/v1"
_SESSION = requests.Session()
_SESSION.headers.update({"Accept": "application/json"})


def search_location(query: str) -> list[dict]:
    """Search BOM for a location by name."""
    resp = _SESSION.get(f"{BOM_API_BASE}/locations", params={"search": query})
    resp.raise_for_status()
    data = resp.json().get("data", [])
    return [
        {
            "geohash": loc["geohash"],
            "name": loc["name"],
            "postcode": loc.get("postcode", ""),
            "state": loc.get("state", ""),
        }
        for loc in data
    ]


def get_daily_forecast(geohash: str) -> dict:
    """Fetch the 7-day daily forecast for a location geohash."""
    resp = _SESSION.get(f"{BOM_API_BASE}/locations/{geohash}/forecasts/daily")
    resp.raise_for_status()
    return resp.json()


def format_forecast(location: dict, forecast_data: dict) -> str:
    """Format a 7-day forecast for terminal display."""
    name = location["name"]
    state = location.get("state", "")
    postcode = location.get("postcode", "")

    header = name
    if state:
        header += f", {state}"
    if postcode:
        header += f" {postcode}"

    lines = [header, ""]

    for day in forecast_data.get("data", []):
        date_str = day.get("date", "")
        try:
            dt = datetime.fromisoformat(date_str)
            day_label = dt.strftime("%a %d %b")
        except (ValueError, TypeError):
            day_label = date_str

        short_text = day.get("short_text", "")
        extended_text = day.get("extended_text", "")
        temp_max = day.get("temp_max")
        temp_min = day.get("temp_min")

        temp_str = ""
        if temp_max is not None and temp_min is not None:
            temp_str = f" ({temp_max}\u00b0/{temp_min}\u00b0)"
        elif temp_max is not None:
            temp_str = f" ({temp_max}\u00b0)"

        headline = f"{day_label} \u2014 {short_text}{temp_str}" if short_text else day_label
        lines.append(headline)

        details = []
        rain = day.get("rain", {})
        rain_chance = rain.get("chance")
        if rain_chance is not None:
            details.append(f"Rain: {rain_chance}% chance")

        uv = day.get("uv", {})
        uv_cat = uv.get("category")
        uv_max = uv.get("max_index")
        if uv_cat:
            uv_str = f"UV: {uv_cat}"
            if uv_max is not None:
                uv_str += f" ({uv_max})"
            details.append(uv_str)

        fire_danger = day.get("fire_danger")
        if fire_danger:
            details.append(f"Fire: {fire_danger}")

        if details:
            lines.append(f"  {' | '.join(details)}")

        if extended_text:
            lines.append(f"  {extended_text}")

        lines.append("")

    return "\n".join(lines)
