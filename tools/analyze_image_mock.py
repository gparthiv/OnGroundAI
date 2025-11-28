def analyze_image_mock(image_id: str) -> dict:
    """Mock analysis: return realistic metadata for an image."""
    # Based on image_id you can vary the output (simple demo).
    if image_id == "img_001":
        return {
            "status": "success",
            "gps": {"lat": 12.9716, "lon": 77.5946},
            "timestamp": "2025-11-28T09:34:00",
            "reuse_score": 0.15,
            "note": "Looks fresh, GPS matches nearby area"
        }
    return {"status": "success", "gps": None, "timestamp": None, "reuse_score": 0.5, "note": "unknown"}
