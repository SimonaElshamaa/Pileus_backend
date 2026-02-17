#!/usr/bin/env python3
"""
fetch_scada_to_csv.py to use at task 19 folder

- Calls a SCADA API endpoint (GET)
- Parses JSON response
- Extracts fields + defaults/transforms
- Writes a CSV named "scada data.csv"
- Overwrites the old file if it already exists

Required: pip install requests
"""

from __future__ import annotations

import csv
import sys
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


OUTPUT_CSV_NAME = "scada_data.csv"

OUTPUT_FIELDS = [
    "Timestamp",
    "Wind speed [m/s]",
    "Wind direction [deg]",
    "Ambient temperature [C]",
    "Output power [kW]",
    "Status",
    "State",
    "Ice detected",
    "IPS",
]


def ms_epoch_to_iso(ms: Any) -> str:
    """Convert Unix epoch milliseconds -> 'D.M.YYYY H:MM' (UTC)."""
    if ms is None:
        return ""
    try:
        ms_int = int(float(ms))
        dt = datetime.fromtimestamp(ms_int / 1000.0, tz=timezone.utc)

        # Example output: 1.1.2003 0:00
        # %-d and %-m remove leading zeros on mac/linux.
        return dt.strftime("%-d.%-m.%Y %-H:%M")
    except (ValueError, TypeError, OverflowError):
        return ""
    

def to_float_default(value: Any, default: float) -> float:
    if value is None:
        return float(default)
    try:
        return float(value)
    except (ValueError, TypeError):
        return float(default)


def status_ok_no(value: Any) -> str:
    """0 -> OK, anything else -> NO"""
    try:
        return "OK" if int(value) == 0 else "NO"
    except (ValueError, TypeError):
        return "NO"


def extract_records(payload: Any) -> List[Dict[str, Any]]:
    """
    Supports:
      - API wrapper dict with 'data_vector' (preferred) or 'last_data'
      - a plain list of objects
    """
    if isinstance(payload, dict):
        dv = payload.get("data_vector")
        if isinstance(dv, list) and dv:
            return [r for r in dv if isinstance(r, dict)]
        ld = payload.get("last_data")
        if isinstance(ld, dict) and ld:
            return [ld]
        return []

    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]

    return []


def transform_row(obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "Timestamp": ms_epoch_to_iso(obj.get("timepoint")),
        "Wind speed [m/s]": to_float_default(obj.get("wind_speed"), 0.0),
        "Wind direction [deg]": to_float_default(obj.get("wind_direction"), 0.0),  # null -> 0.0
        "Ambient temperature [C]": 5.0,  # default
        "Output power [kW]": to_float_default(obj.get("P_actual_kW"), 0.0),
        "Status": status_ok_no(obj.get("main_status")),
        "State": status_ok_no(obj.get("sub_status")),
        "Ice detected": "NO",  # default
        "IPS": "OFF",          # default
    }


def fetch_json(url: str, token: Optional[str] = None, timeout: int = 30) -> Any:
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    print('headersssss',headers)
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def write_csv(rows: List[Dict[str, Any]], path: str) -> None:
    # mode="w" overwrites if file exists
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    
        print("Usage: python fetch_scada_to_csv.py <Scada data log> [BEARER_TOKEN]", file=sys.stderr)
        print('Example: python fetch_scada_to_csv.py "https://example.com/task19?wec_uuid=..."', file=sys.stderr)

        url = "https://api-144067630816.europe-west1.run.app/api/scada/dragaliden-01/data-log/?start_time=2023-09-08T00:00&end_time=2025-09-08T12:00"
        token = "" #to be added access to end point 

        payload = fetch_json(url, token=token)
        records = extract_records(payload)
        rows = [transform_row(obj) for obj in records]

        write_csv(rows, OUTPUT_CSV_NAME)
        print(f"Wrote {len(rows)} rows to '{OUTPUT_CSV_NAME}' (overwritten if existed).")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
