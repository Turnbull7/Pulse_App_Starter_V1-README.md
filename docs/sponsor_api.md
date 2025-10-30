
# Sponsor Insights API (Public Contract — v0.1)

**Endpoint:** `POST /sponsor/insights`

**Request:**
```json
{
  "segment": "ALL_USERS",
  "metric": "sponsor_cta_click_per_hour"
}
```

**Response:**
```json
{
  "segment": "ALL_USERS",
  "metric": "sponsor_cta_click_per_hour",
  "series": [
    { "t": "2025-10-28T18:00:00Z", "value": 124, "n": 124 },
    { "t": "2025-10-28T19:00:00Z", "value": 201, "n": 201 }
  ]
}
```

Notes:
- `n` must be >= 50 to return a point (k-anonymity).
- Metrics are aggregated and do not expose user-level data.
- Additional segmentation keys (geo/age/gender/interests) can be added.
