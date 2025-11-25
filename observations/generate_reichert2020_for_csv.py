#!/usr/bin/env python3
"""Build a Fornax Eu abundance catalogue from Reichert et al. (2020).

This script parses the `tableo3.dat` file (distributed here as
`observations/reichert2020.dat`) described in the CDS ReadMe and extracts the
Fornax ("For") entries together with their iron and europium measurements.  The
output CSV mirrors the column naming convention from the ReadMe and adds
computed [Eu/H] and [Eu/Fe] ratios for convenience.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Iterator

EU_SOLAR_LOGEPS = 0.52  # Asplund et al. (2009), adopted for consistency with CDS catalogue

SOLAR_LOGEPS = {
    "Mg": 7.60,
    "Sc": 3.15,
    "Ti": 4.95,
    "Cr": 5.64,
    "Mn": 5.43,
    "Ni": 6.22,
    "Zn": 4.56,
    "Sr": 2.87,
    "Y": 2.21,
    "Ba": 2.18,
    "Eu": EU_SOLAR_LOGEPS,
}

ELEMENT_SLICES = {
    "Mg": {
        "logeps": (50, 53),
        "e_tot": (55, 58),
    },
    "Sc": {
        "logeps": (90, 94),
        "e_tot": (96, 99),
    },
    "Ti": {
        "logeps": (131, 134),
        "e_tot": (136, 139),
    },
    "Cr": {
        "logeps": (171, 174),
        "e_tot": (176, 179),
    },
    "Mn": {
        "logeps": (211, 214),
        "e_tot": (216, 219),
    },
    "Ni": {
        "logeps": (251, 254),
        "e_tot": (256, 259),
    },
    "Zn": {
        "logeps": (291, 294),
        "e_tot": (296, 299),
    },
    "Sr": {
        "logeps": (331, 335),
        "e_tot": (337, 340),
    },
    "Y": {
        "logeps": (372, 376),
        "e_tot": (378, 381),
    },
    "Ba": {
        "logeps": (413, 417),
        "e_tot": (419, 422),
    },
    "Eu": {
        "logeps": (454, 458),
        "e_tot": (460, 463),
    },
}


def parse_float(segment: str) -> float:
    """Return a float for the provided fixed-width segment or NaN when blank."""
    text = segment.strip()
    if not text:
        return math.nan
    try:
        return float(text)
    except ValueError:
        return math.nan


def slice_field(line: str, start: int, end: int) -> str:
    """Return the fixed-width segment (1-indexed) for the requested bytes."""
    return line[start - 1 : end]


def parse_record(line: str) -> dict[str, float | str] | None:
    """Convert a fixed-width Reichert et al. (2020) row into a dict.

    The byte ranges follow the `tableo3.dat` layout documented in observations/ReadMe.txt.
    Only Fornax stars (Galaxy == "For") with finite europium abundances are returned.
    """

    galaxy = line[31:37].strip()
    if galaxy != "For":
        return None

    star_id = line[0:30].strip()

    feh = parse_float(slice_field(line, 39, 43))
    feh_err = parse_float(slice_field(line, 45, 48))

    eu_logeps_raw = parse_float(slice_field(line, 454, 458))
    if math.isnan(eu_logeps_raw):
        return None

    record: dict[str, float | str] = {
        "ID": star_id,
        "Galaxy": galaxy,
        "[Fe/H]": feh,
        "e_[Fe/H]": feh_err,
    }

    for element in ELEMENT_SLICES:
        meta = ELEMENT_SLICES[element]
        logeps_value = parse_float(slice_field(line, *meta["logeps"]))
        e_tot_value = parse_float(slice_field(line, *meta["e_tot"]))

        record[f"logeps({element})"] = logeps_value
        record[f"e_tot({element})"] = e_tot_value
        record[f"sigma_{element}"] = e_tot_value

        if not math.isnan(logeps_value):
            record[f"[{element}/H]"] = logeps_value - SOLAR_LOGEPS[element]
        else:
            record[f"[{element}/H]"] = math.nan

        if (
            not math.isnan(record[f"[{element}/H]"])
            and not math.isnan(record["[Fe/H]"])
        ):
            record[f"[{element}/Fe]"] = record[f"[{element}/H]"] - record["[Fe/H]"]
        else:
            record[f"[{element}/Fe]"] = math.nan

    e_temp_eu = parse_float(slice_field(line, 465, 468))
    e_logg_eu = parse_float(slice_field(line, 470, 473))
    e_feh_eu = parse_float(slice_field(line, 475, 478))
    e_v_eu = parse_float(slice_field(line, 480, 483))
    e_stat_eu = parse_float(slice_field(line, 485, 488))
    e_noise_eu = parse_float(slice_field(line, 490, 493))

    record.update(
        {
            "e_temp(Eu)": e_temp_eu,
            "e_logg(Eu)": e_logg_eu,
            "e_[Fe/H](Eu)": e_feh_eu,
            "e_v(Eu)": e_v_eu,
            "e_stat(Eu)": e_stat_eu,
            "e_noise(Eu)": e_noise_eu,
            "[Eu/H]": record[f"[Eu/H]"],
            "[Eu/Fe]": record[f"[Eu/Fe]"],
            "sigma_Fe": feh_err,
            "sigma_Eu": record[f"sigma_Eu"],
        }
    )

    return record


def iter_records(path: Path) -> Iterator[dict[str, float | str]]:
    with path.open("r", encoding="ascii", errors="replace") as handle:
        for line in handle:
            record = parse_record(line)
            if record is not None:
                yield record


def build_catalogue(input_path: Path, output_path: Path) -> int:
    records = list(iter_records(input_path))
    records.sort(key=lambda row: (row.get("[Fe/H]", math.nan), row["ID"]))

    def build_fieldnames() -> list[str]:
        names = ["ID", "Galaxy", "[Fe/H]", "e_[Fe/H]"]
        for element in ELEMENT_SLICES:
            names.append(f"logeps({element})")
            names.append(f"e_tot({element})")
            if element == "Eu":
                names.extend(
                    [
                        "e_temp(Eu)",
                        "e_logg(Eu)",
                        "e_[Fe/H](Eu)",
                        "e_v(Eu)",
                        "e_stat(Eu)",
                        "e_noise(Eu)",
                    ]
                )
            names.append(f"sigma_{element}")
            names.append(f"[{element}/H]")
            names.append(f"[{element}/Fe]")
        names.append("sigma_Fe")
        return names

    fieldnames = build_fieldnames()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="ascii", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    return len(records)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parent / "reichert2020.dat",
        help="Path to the Reichert et al. (2020) tableo3.dat file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "reichert2020_for.csv",
        help="Destination path for the Fornax CSV catalogue.",
    )
    args = parser.parse_args()

    count = build_catalogue(args.input, args.output)
    print(f"Wrote {count} Fornax rows to {args.output}")


if __name__ == "__main__":
    main()
