"""Visualization utilities for BOM spatial data."""

import os
import webbrowser
from typing import Any

import folium
import geopandas as gpd

from . import settings

# Spatial types configuration
# "point" for marker-based, "polygon" for shape-based
# Icons from Font Awesome (fa prefix) - https://fontawesome.com/v4/icons/
SPATIAL_CONFIGS: dict[str, dict[str, Any]] = {
    "radar_location": {
        "file": "IDR00007",
        "type": "point",
        "lat": "Latitude",
        "lon": "Longitude",
        "name": "Full_Name",
        "popup_fields": ["Full_Name", "State", "Type", "Status"],
        "color": "darkred",
        "icon": "bullseye",  # Radar dish representation
        "label": "Radar Locations",
        "cluster": False,  # Few points, no clustering needed
    },
    "radar_coverage": {
        "file": "IDR00006",
        "type": "point",
        "lat": "LATITUDE",
        "lon": "LONGITUDE",
        "name": "FULL_NAME",
        "popup_fields": ["FULL_NAME", "STATE", "TYPE", "STATUS"],
        "color": "cadetblue",
        "icon": "rss",  # Signal/broadcast icon
        "label": "Radar Coverage",
        "cluster": False,
    },
    "point_places": {
        "file": "IDM00013",
        "type": "point",
        "lat": "LAT",
        "lon": "LON",
        "name": "PT_NAME",
        "popup_fields": ["PT_NAME", "STATE_NAME", "ELEVATION"],
        "color": "green",
        "icon": "tint",  # Raindrop - weather related
        "label": "Weather Stations",
        "cluster": True,  # Many points, use clustering
    },
    "forecast_districts": {
        "file": "IDM00001",
        "type": "polygon",
        "name": "DIST_NAME",
        "popup_fields": ["AAC", "DIST_NAME", "STATE_CODE"],
        "fill_color": "YlOrRd",
        "line_color": "blue",
        "label": "Forecast Districts",
    },
    "marine_zones": {
        "file": "IDM00003",
        "type": "polygon",
        "name": "DIST_NAME",
        "popup_fields": ["AAC", "DIST_NAME", "STATE_CODE", "TYPE"],
        "fill_color": "YlGnBu",
        "line_color": "navy",
        "label": "Marine Zones",
    },
    "fire_districts": {
        "file": "IDM00007",
        "type": "polygon",
        "name": "DIST_NAME",
        "popup_fields": ["AAC", "DIST_NAME", "STATE_CODE"],
        "fill_color": "OrRd",
        "line_color": "darkred",
        "label": "Fire Districts",
    },
    "rainfall_districts": {
        "file": "IDM00004",
        "type": "polygon",
        "name": "DIST_NAME",
        "popup_fields": ["DIST_NAME", "STATE"],
        "fill_color": "Blues",
        "line_color": "blue",
        "label": "Rainfall Districts",
    },
    "cyclone_areas": {
        "file": "IDM00005",
        "type": "polygon",
        "name": "Name",
        "popup_fields": ["Name"],
        "fill_color": "PuRd",
        "line_color": "purple",
        "label": "Cyclone Areas",
    },
    "high_sea_areas": {
        "file": "IDM00006",
        "type": "polygon",
        "name": "NAME",
        "popup_fields": ["NAME"],
        "fill_color": "GnBu",
        "line_color": "darkblue",
        "label": "High Sea Areas",
    },
    "metros": {
        "file": "IDM00014",
        "type": "polygon",
        "name": "DIST_NAME",
        "popup_fields": ["AAC", "DIST_NAME", "STATE_CODE", "DESCRIPTN"],
        "fill_color": "Purples",
        "line_color": "purple",
        "label": "Metro Areas",
    },
    "ocean_wind_warning": {
        "file": "IDM00015",
        "type": "polygon",
        "name": "NAME",
        "popup_fields": ["NAME"],
        "fill_color": "BuPu",
        "line_color": "indigo",
        "label": "Ocean Wind Warning",
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


def _add_point_layer(feature_group: folium.FeatureGroup, config: dict, shp_path: str) -> None:
    """Add point markers to a feature group."""
    import dbfread
    from folium.plugins import MarkerCluster

    dbf_path = shp_path.replace(".shp", ".dbf")
    records = list(dbfread.DBF(dbf_path))

    # Use marker cluster for large datasets
    use_cluster = config.get("cluster", False) and len(records) > 50
    if use_cluster:
        marker_target = MarkerCluster(name=config["label"])
        marker_target.add_to(feature_group)
    else:
        marker_target = feature_group

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
        ).add_to(marker_target)


def _add_polygon_layer(feature_group: folium.FeatureGroup, config: dict, shp_path: str) -> None:
    """Add polygon shapes to a feature group."""
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

    geojson = folium.GeoJson(
        gdf,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=[name_field] if name_field in gdf.columns else [],
            aliases=["Name:"] if name_field in gdf.columns else [],
        ),
    )

    geojson.add_to(feature_group)


def _add_layer(m: folium.Map, spatial_type: str, show: bool = True) -> None:
    """Add a spatial layer to the map."""
    config = SPATIAL_CONFIGS[spatial_type]
    shp_path = os.path.join(settings.SPATIAL_CACHE, f"{config['file']}.shp")
    dbf_path = os.path.join(settings.SPATIAL_CACHE, f"{config['file']}.dbf")

    # Check for required files
    if config["type"] == "polygon" and not os.path.exists(shp_path):
        raise FileNotFoundError(f"Shapefile not found: {shp_path}. Run 'bomshell spatial fetch' first.")
    if not os.path.exists(dbf_path):
        raise FileNotFoundError(f"Data file not found: {dbf_path}. Run 'bomshell spatial fetch' first.")

    # Create feature group for this layer
    feature_group = folium.FeatureGroup(name=config["label"], show=show)

    # Add appropriate layer based on type
    if config["type"] == "point":
        _add_point_layer(feature_group, config, shp_path)
    else:
        _add_polygon_layer(feature_group, config, shp_path)

    feature_group.add_to(m)


def create_map(spatial_types: str | list[str], output_path: str | None = None) -> str:
    """
    Create a folium map for one or more spatial types.

    :param spatial_types: Single type or list of spatial data types to visualize
    :param output_path: Output HTML file path (default: based on types in cache)
    :return: Path to the generated HTML file
    """
    # Normalize to list
    if isinstance(spatial_types, str):
        spatial_types = [spatial_types]

    # Validate all types
    for spatial_type in spatial_types:
        if spatial_type not in SPATIAL_CONFIGS:
            raise ValueError(f"Unknown spatial type: {spatial_type}. Available: {get_visualizable_types()}")

    # Create map centered on Australia
    m = folium.Map(location=AUSTRALIA_CENTER, zoom_start=DEFAULT_ZOOM, tiles="OpenStreetMap")

    # Add each layer (polygons first, then points on top)
    polygon_types = [t for t in spatial_types if SPATIAL_CONFIGS[t]["type"] == "polygon"]
    point_types = [t for t in spatial_types if SPATIAL_CONFIGS[t]["type"] == "point"]

    for spatial_type in polygon_types + point_types:
        _add_layer(m, spatial_type, show=True)

    # Add layer control if multiple layers
    if len(spatial_types) > 1:
        folium.LayerControl(collapsed=False).add_to(m)

    # Determine output path
    if output_path is None:
        if len(spatial_types) == 1:
            output_path = os.path.join(settings.CACHE, f"{spatial_types[0]}.html")
        else:
            output_path = os.path.join(settings.CACHE, "combined_map.html")

    m.save(output_path)
    return output_path


def open_in_browser(file_path: str) -> None:
    """Open a file in the default web browser."""
    webbrowser.open(f"file://{os.path.abspath(file_path)}")
