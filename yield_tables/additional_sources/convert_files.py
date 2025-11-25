from __future__ import annotations

from pathlib import Path
import re
import sys

repo_root = Path('/home/minjih/NuPyCEE').resolve()
package_root = repo_root.parent
if str(package_root) not in sys.path:
    sys.path.insert(0, str(package_root))

def format_isotope(label: str) -> tuple[str, int]:
    """Convert labels like 'eu151' to ('Eu-151', 151)."""
    match = re.fullmatch(r"([a-zA-Z]+)([0-9]+)", label.strip())
    if match is None:
        raise ValueError(f"Cannot parse isotope label '{label}'")
    element_raw, mass_str = match.groups()
    element = element_raw.capitalize()
    if len(element_raw) > 1:
        element = element_raw[0].upper() + element_raw[1:].lower()
    mass_number = int(mass_str)
    return f"{element}-{mass_number}", mass_number


def ensure_mrd_yield_table(source: Path, destination: Path, metallicities: list[float]) -> Path:
    """Convert Nishimura et al. (2017) MRD yields to NuPyCEE Z-dependent format."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        print(f"MRD yield table already cached at {destination}")
        return destination

    entries = []
    with source.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 6:
                continue
            iso_label, mass = parts[0], float(parts[5])
            formatted, mass_number = format_isotope(iso_label)
            entries.append((mass_number, formatted, mass))

    entries.sort()

    header_lines = [
        "H Nishimura et al. (2017) L1.00 MRD yields converted for NuPyCEE",
        "H Metallicities columns carry identical yields (assumed MRD metallicity independence).",
        "&Isotopes  " + "  ".join(f"&Z={z:.4g}" for z in metallicities),
    ]

    rows = []
    for _, formatted, mass in entries:
        row = f"&{formatted:<8}" + "".join(f" &{mass:.6E}" for _ in metallicities)
        rows.append(row)

    destination.write_text("\n".join(header_lines + rows) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} isotopes to {destination}")
    return destination


mrd_source = repo_root / "yield_tables" / "additional_sources" / "MRD_r_process" / "L1.00.dat"
mrd_destination = repo_root / "yield_tables" / "additional_sources" / "MRD_r_process_NuPyCEE.txt"
metallicity_grid = [1.0e-4, 5.0e-4, 1.0e-3]
mrd_yield_path = ensure_mrd_yield_table(mrd_source, mrd_destination, metallicity_grid)
if __name__ == "__main__":
    print(f"MRD yield table available at: {mrd_yield_path}")