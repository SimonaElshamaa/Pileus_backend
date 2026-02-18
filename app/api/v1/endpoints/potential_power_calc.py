#!/usr/bin/env python3
"""
calc_potential_power.py

Usage:
  python calc_potential_power.py \
    --data fake_data.csv \
    --powercurve powercurve.txt \
    --out fake_data_with_potential.csv \
    --wind-col wind_speed

Notes:
- Expects fake_data.csv to have a wind speed column (default: wind_speed).
- Reads ONLY the "Power Curve" section from the Task19 powercurve.txt.
- Computes potential power by linear interpolation between bins.
"""

from __future__ import annotations

import argparse
import csv
import re
from bisect import bisect_left
from typing import List, Tuple, Dict, Optional


SECTION_HEADER_RE = re.compile(r"^\s*(?P<dataset>.+?)\s+Power Curve\s*$")
NUMPAIR_RE = re.compile(r"^\s*(?P<x>-?\d+(?:\.\d+)?)\s+(?P<y>-?\d+(?:\.\d+)?)\s*$")


def read_power_curve_section(path: str) -> Tuple[List[float], List[float]]:
    """
    Parse the "Power Curve" section from a Task19 powercurve.txt file.

    Returns:
      xs: wind speed bins (ascending)
      ys: power values (kW)
    """
    in_power_curve = False
    xs: List[float] = []
    ys: List[float] = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line_stripped = line.rstrip("\n")

            # Detect the start of "Power Curve" section
            if SECTION_HEADER_RE.match(line_stripped):
                in_power_curve = True
                continue

            # If we hit another section header after Power Curve, stop reading
            if in_power_curve:
                # Any line like "ExampleDataset P10" means we are done with Power Curve section
                if re.match(r"^\s*.+?\s+(P10|P90|Std\.dev\.|Uncertainty \[%\]|Lower limit|Upper limit|Bin Size \[n\])\s*$",
                            line_stripped):
                    break

                # Parse numeric pairs inside section
                m = NUMPAIR_RE.match(line_stripped)
                if m:
                    xs.append(float(m.group("x")))
                    ys.append(float(m.group("y")))

    if not xs:
        raise ValueError("Could not find any numeric data in 'Power Curve' section. Check file format.")

    # Ensure sorted (should already be)
    pairs = sorted(zip(xs, ys), key=lambda t: t[0])
    xs_sorted = [p[0] for p in pairs]
    ys_sorted = [p[1] for p in pairs]
    return xs_sorted, ys_sorted


def interp_linear(x: float, xs: List[float], ys: List[float], clamp: bool = True) -> float:
    """
    Linear interpolation y(x) over tabulated points (xs, ys).
    If clamp=True, values outside range are clamped to endpoints.
    """
    if x <= xs[0]:
        return ys[0] if clamp else float("nan")
    if x >= xs[-1]:
        return ys[-1] if clamp else float("nan")

    # Find right index so xs[i-1] < = x < xs[i]
    i = bisect_left(xs, x)
    x1, y1 = xs[i - 1], ys[i - 1]
    x2, y2 = xs[i], ys[i]

    if x2 == x1:
        return y1

    f = (x - x1) / (x2 - x1)
    return y1 + f * (y2 - y1)


def parse_float(value: str) -> Optional[float]:
    if value is None:
        return None
    s = str(value).strip()
    if s == "" or s.lower() in {"null", "none", "nan"}:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="fake_data2.csv")
    ap.add_argument("--powercurve", required=True, help="./results/example/ExampleDataset_powercurve.txt")
    ap.add_argument("--out", required=True, help="Output.csv")
    ap.add_argument("--wind-col", default="Wind speed [m/s]", help="Wind speed")
    ap.add_argument("--potential-col", default="P_potential_kW", help="potential power")
    args = ap.parse_args()

    xs, ys = read_power_curve_section(args.powercurve)

    with open(args.data, "r", encoding="utf-8", errors="ignore", newline="") as f_in:
        reader = csv.DictReader(f_in)
        if reader.fieldnames is None:
            raise ValueError("Input CSV has no header row.")

        if args.wind_col not in reader.fieldnames:
            raise ValueError(
                f"Wind column '{args.wind_col}' not found. Available columns: {reader.fieldnames}"
            )

        with open(args.out, "w", encoding="utf-8", newline="") as f_out:
            fieldnames = [args.wind_col, args.potential_col]
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                v = parse_float(row.get(args.wind_col))

                if v is None:
                    potential = ""
                else:
                    potential = interp_linear(v, xs, ys, clamp=True)

                writer.writerow({
                    args.wind_col: v,
                    args.potential_col: potential
                })


    print(f"Done. Wrote output to: {args.out}")


if __name__ == "__main__":
    main()
