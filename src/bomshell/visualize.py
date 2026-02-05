"""Visualization utilities for BOM spatial data."""

import os
import webbrowser

import folium
import geopandas as gpd

from . import settings

# Spatial types configuration
# "point" for marker-based, "polygon" for shape-based
SPATIAL_CONFIGS = {
    "radar_location": {
        "file": "IDR00007",
        "type": "point",
        "lat": "Latitude",
        "lon": "Longitude",
        "name": "Full_Name",
        "popup_fields": ["Full_Name", "State", "Type", "Status"],
        "color": "red",
        "icon": "signal",
    },
    "radar_coverage": {
        "file": "IDR00006",
        "type": "point",
        "lat": "LATITUDE",
        "lon": "LONGITUDE",
        "name": "FULL_NAME",
        "popup_fields": ["FULL_NAME", "STATE", "TYPE", "STATUS"],
        "color": "blue",
        "icon": "signal",
    },
    "point_places": {
        "file": "IDM00013",
        "type": "point",
        "lat": "LAT",
        "lon": "LON",
        "name": "PT_NAME",
        "popup_fields": ["PT_NAME", "STATE_NAME", "ELEVATION"],
        "color": "green",
        "icon": "cloud",
    },
    "forecast_districts": {
        "file": "IDM00001",
        "type": "polygon",
        "name": "DIST_NAME",
        "popup_fields": ["AAC", "DIST_NAME", "STATE_CODE"],
        "fill_color": "YlOrRd",
        "line_color": "blue",
    },
    "marine_zones": {
        "file": "IDM00003",
        "type": "polygon",
        "name": "DIST_NAME",
        "popup_fields": ["AAC", "DIST_NAME", "STATE_CODE", "TYPE"],
        "fill_color": "YlGnBu",
        "line_color": "navy",
    },
    "fire_districts": {
        "file": "IDM00007",
        "type": "polygon",
        "name": "DIST_NAME",
        "popup_fields": ["AAC", "DIST_NAME", "STATE_CODE"],
        "fill_color": "OrRd",
        "line_color": "darkred",
    },
    "rainfall_districts": {
        "file": "IDM00004",
        "type": "polygon",
        "name": "DIST_NAME",
        "popup_fields": ["DIST_NAME", "STATE"],
        "fill_color": "Blues",
        "line_color": "blue",
    },
    "cyclone_areas": {
        "file": "IDM00005",
        "type": "polygon",
        "name": "Name",
        "popup_fields": ["Name"],
        "fill_color": "PuRd",
        "line_color": "purple",
    },
    "high_sea_areas": {
        "file": "IDM00006",
        "type": "polygon",
        "name": "NAME",
        "popup_fields": ["NAME"],
        "fill_color": "GnBu",
        "line_color": "darkblue",
    },
    "metros": {
        "file": "IDM00014",
        "type": "polygon",
        "name": "DIST_NAME",
        "popup_fields": ["AAC", "DIST_NAME", "STATE_CODE", "DESCRIPTN"],
        "fill_color": "Purples",
        "line_color": "purple",
    },
    "ocean_wind_warning": {
        "file": "IDM00015",
        "type": "polygon",
        "name": "NAME",
        "popup_fields": ["NAME"],
        "fill_color": "BuPu",
        "line_color": "indigo",
    },
}

# Australia center coordinates
AUSTRALIA_CENTER = [-25.0, 135.0]
DEFAULT_ZOOM = 4


def get_visualizable_types() -> list[str]:
    """Return list of spatial types that can be visualized."""
    return sorted(SPATIAL_CONFIGS.keys())


def _build_popup_html(record: dict, fields: list[str]) -> str:
    """Build HTML popup content from record fields."""
    lines = []
    for field in fields:
        value = record.get(field, "")
        if value:
            lines.append(f"<b>{field}:</b> {value}")
    return "<br>".join(lines)


def _add_point_layer(m: folium.Map, config: dict, shp_path: str) -> None:
    """Add point markers to map."""
    import dbfread

    dbf_path = shp_path.replace(".shp", ".dbf")
    records = list(dbfread.DBF(dbf_path))

    for record in records:
        lat = record.get(config["lat"])
        lon = record.get(config["lon"])

        if lat is None or lon is None:
            continue

        popup_html = _build_popup_html(record, config["popup_fields"])
        tooltip = str(record.get(config["name"], ""))

        folium.Marker(
            location=[float(lat), float(lon)],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=tooltip,
            icon=folium.Icon(color=config["color"], icon=config["icon"], prefix="fa"),
        ).add_to(m)


def _add_polygon_layer(m: folium.Map, config: dict, shp_path: str) -> None:
    """Add polygon shapes to map."""
    gdf = gpd.read_file(shp_path)

    # Convert to WGS84 if needed
    if gdf.crs and gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    # Create a GeoJson layer with styling
    def style_function(_feature: dict) -> dict:
        return {
            "fillColor": config.get("line_color", "blue"),
            "color": config.get("line_color", "blue"),
            "weight": 2,
            "fillOpacity": 0.3,
        }

    def highlight_function(_feature: dict) -> dict:
        return {
            "fillColor": config.get("line_color", "blue"),
            "color": config.get("line_color", "blue"),
            "weight": 3,
            "fillOpacity": 0.6,
        }

    # Add GeoJson layer
    name_field = config["name"]
    popup_fields = config["popup_fields"]

    geojson = folium.GeoJson(
        gdf,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=[name_field] if name_field in gdf.columns else [],
            aliases=["Name:"] if name_field in gdf.columns else [],
        ),
    )

    # Add popups
    for _, row in gdf.iterrows():
        popup_lines = []
        for field in popup_fields:
            if field in row.index and row[field]:
                popup_lines.append(f"<b>{field}:</b> {row[field]}")
        if popup_lines:
            popup_html = "<br>".join(popup_lines)
            centroid = row.geometry.centroid
            folium.Popup(popup_html, max_width=300).add_to(
                folium.Marker(
                    location=[centroid.y, centroid.x],
                    icon=folium.DivIcon(html=""),
                )
            )

    geojson.add_to(m)


def create_map(spatial_type: str, output_path: str | None = None) -> str:
    """
    Create a folium map for the given spatial type.

    :param spatial_type: Type of spatial data to visualize
    :param output_path: Output HTML file path (default: <spatial_type>.html in cache)
    :return: Path to the generated HTML file
    """
    if spatial_type not in SPATIAL_CONFIGS:
        raise ValueError(f"Unknown spatial type: {spatial_type}. Available: {get_visualizable_types()}")

    config = SPATIAL_CONFIGS[spatial_type]
    shp_path = os.path.join(settings.SPATIAL_CACHE, f"{config['file']}.shp")
    dbf_path = os.path.join(settings.SPATIAL_CACHE, f"{config['file']}.dbf")

    # Check for required files
    if config["type"] == "polygon" and not os.path.exists(shp_path):
        raise FileNotFoundError(f"Shapefile not found: {shp_path}. Run 'bomshell spatial fetch' first.")
    if not os.path.exists(dbf_path):
        raise FileNotFoundError(f"Data file not found: {dbf_path}. Run 'bomshell spatial fetch' first.")

    # Create map centered on Australia
    m = folium.Map(location=AUSTRALIA_CENTER, zoom_start=DEFAULT_ZOOM, tiles="OpenStreetMap")

    # Add appropriate layer based on type
    if config["type"] == "point":
        _add_point_layer(m, config, shp_path)
    else:
        _add_polygon_layer(m, config, shp_path)

    # Determine output path
    if output_path is None:
        output_path = os.path.join(settings.CACHE, f"{spatial_type}.html")

    m.save(output_path)
    return output_path


def open_in_browser(file_path: str) -> None:
    """Open a file in the default web browser."""
    webbrowser.open(f"file://{os.path.abspath(file_path)}")
