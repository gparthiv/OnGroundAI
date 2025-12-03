def analyze_image_mock(image_id: str) -> dict:
    """Mock analysis for image metadata. Used in MCP-style image processing."""

    mapping = {
        "img_siteok_001": {
            "status": "success",
            "gps": {"lat": 12.9311, "lon": 77.6234},
            "timestamp": "2025-11-28T10:06:00",
            "reuse_score": 0.10,
            "note": "Fresh image, location matches assigned task."
        },
        "img_reused_003": {
            "status": "success",
            "gps": None,
            "timestamp": None,
            "reuse_score": 0.92,
            "note": "Image looks reused or forwarded, metadata missing."
        },
        "img_wrongloc_002": {
            "status": "success",
            "gps": {"lat": 12.9716, "lon": 77.5946},
            "timestamp": "2025-11-28T09:26:00",
            "reuse_score": 0.25,
            "note": "Location does not match assigned task; worker may be at wrong site."
        },
        "img_meter_004": {
            "status": "success",
            "gps": {"lat": 12.9104, "lon": 77.6441},
            "timestamp": "2025-11-28T11:06:00",
            "reuse_score": 0.08,
            "note": "Meter image looks authentic and recent."
        },
        "img_accidentspot_006": {
            "status": "success",
            "gps": {"lat": 12.9352, "lon": 77.6121},
            "timestamp": "2025-11-28T09:23:00",
            "reuse_score": 0.03,
            "note": "Accident visible in picture, immediate attention recommended."
        },
        "img_deliveryproof_007": {
            "status": "success",
            "gps": {"lat": 12.9121, "lon": 77.6324},
            "timestamp": "2025-11-28T10:05:00",
            "reuse_score": 0.11,
            "note": "Delivery proof captured successfully."
        },
        "img_pickup_008": {
            "status": "success",
            "gps": {"lat": 12.9333, "lon": 77.6532},
            "timestamp": "2025-11-28T11:40:00",
            "reuse_score": 0.18,
            "note": "Package pickup confirmed."
        }
    }

    # default fallback
    return mapping.get(image_id, {
        "status": "success",
        "gps": None,
        "timestamp": None,
        "reuse_score": 0.55,
        "note": "Unknown image ID."
    })
