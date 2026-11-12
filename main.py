"""Print basic statistics for numeric CSV columns."""

import csv
import statistics
import sys
from pathlib import Path


def summarize(file_path):
    rows = []
    with Path(file_path).open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(row)
    if not rows:
        return None
    header = list(rows[0].keys())
    stats = {}
    for column in header:
        values = []
        for row in rows:
            try:
                values.append(float(row[column]))
            except (TypeError, ValueError):
                continue
        if values:
            stats[column] = {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "mean": statistics.fmean(values),
            }
    return stats


def main():
    if len(sys.argv) < 2:
        print("usage: csvstats.py <file.csv>")
        return 1
    stats = summarize(sys.argv[1])
    if not stats:
        print("no data rows")
        return 1
    for column, values in stats.items():
        print(f"{column}: n={values['count']} "
              f"min={values['min']:.3f} max={values['max']:.3f} "
              f"mean={values['mean']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

