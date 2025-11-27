"""
Utilities to parse "stellab" formatted observation files (like the attachments)
and plot them onto a Matplotlib `ax`.

Usage:
    from stellab_utils import parse_stellab_file, plot_stellab_on_ax
    df = parse_stellab_file('stellab_data/fornax_data/Lemasle_et_al_2014_stellab.txt')
    fig, ax = plt.subplots()
    plot_stellab_on_ax(ax, df, x_elem='Fe', y_elem='Eu', label='Lemasle 2014')

The parser is robust to files that include a header row (column names) or
headerless numeric tables. Missing / sentinel values (commonly `30.0` in these
files) are filtered out automatically.
"""

from __future__ import annotations

import re
from typing import Optional, Tuple

import numpy as np
import pandas as pd


MISSING_VALUE_SENTINEL = 30.0


def _is_header_line(line: str) -> bool:
    """Return True if the line looks like a header (contains alphabetic tokens).
    """
    # Remove common bracket characters then check for letters
    t = line.strip()
    if t == "":
        return False
    # if there are alphabetic chars (excluding signs and digits), treat as header
    return bool(re.search(r"[A-Za-z]", t))


def _normalise_colname(name: str) -> str:
    """Normalise a column name: remove brackets, extra spaces, lower-case.
    """
    name = name.strip()
    name = re.sub(r"[\[\]]", "", name)
    name = name.replace("/", "_")
    name = re.sub(r"\s+", "_", name)
    return name.lower()


def parse_stellab_file(path: str) -> pd.DataFrame:
    """Parse a stellab-format text file and return a pandas DataFrame.

    The function handles both files with an explicit header line and files
    without a header (pure numeric). For headerless files, generic column
    names `col0`, `col1`, ... will be assigned.

    It will also normalise column names (remove brackets and spaces) so you
    can more easily match e.g. `[Fe/H]` -> `fe_h`.

    Parameters
    - path: file path to parse

    Returns
    - DataFrame: parsed numeric table; non-numeric or missing entries are
      converted to NaN. Columns are normalised to lower-case names.
    """
    # Read first non-empty line to see if it's a header
    with open(path, "r", encoding="utf-8") as fh:
        first_line = ""
        for raw in fh:
            line = raw.strip()
            if line == "":
                continue
            first_line = line
            break

    header_present = _is_header_line(first_line)

    if header_present:
        # Read the header tokens ourselves so we can preserve bracketed names
        # (e.g. "[Fe/H]") as DataFrame column names.
        with open(path, "r", encoding="utf-8") as fh:
            # first non-empty line already captured in first_line; re-tokenize it
            header_tokens = re.split(r"\s+", first_line.strip())

        # Ask pandas to read the file but don't let it alter header parsing
        df = pd.read_csv(path, delim_whitespace=True, comment="#", header=0, engine="python")
        # If pandas produced a different number of columns than header tokens
        # fall back to pandas' column names; otherwise set our header tokens
        if len(header_tokens) == len(df.columns):
            df.columns = [tok.strip() for tok in header_tokens]
        else:
            # Use pandas columns but still normalise them for downstream use
            df.columns = [_normalise_colname(c) for c in df.columns]
    else:
        # No header: load numeric table
        arr = np.loadtxt(path, comments="#")
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        cols = [f"col{i}" for i in range(arr.shape[1])]
        df = pd.DataFrame(arr, columns=cols)

    # Replace sentinel missing values with NaN
    df = df.replace(MISSING_VALUE_SENTINEL, np.nan)

    # Ensure numeric types where possible
    # Ensure column names are strings and make duplicates unique so that
    # indexing `df[col]` always returns a Series (not a DataFrame slice).
    df.columns = [str(c) for c in df.columns]
    if df.columns.duplicated().any():
        # append a numeric suffix to duplicate column names: name, name_1, name_2...
        new_cols = []
        counts = {}
        for c in df.columns:
            cnt = counts.get(c, 0)
            if cnt == 0:
                new_name = c
            else:
                new_name = f"{c}_{cnt}"
            counts[c] = cnt + 1
            new_cols.append(new_name)
        df.columns = new_cols

    for c in df.columns:
        # df[c] should now be a Series; coerce to numeric
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # If header was present we may have many columns like '[X/H]'.
    # Create a standardized '[Fe/H]' column if possible and then add
    # derived '[X/Fe]' columns so callers can access abundances by
    # the common y-axis format e.g. '[Eu/Fe]'.
    try:
        fe_col = None
        for col in df.columns:
            kl = col.lower()
            if 'err' in kl:
                continue
            # Prefer explicit '[Fe/H]' style matches
            if re.search(r"\[?\s*fe\s*(?:ii|i)?\s*/\s*h\s*\]?", col, flags=re.I):
                fe_col = col
                break
            # Fallback: any column containing 'fe' and 'h'
            if 'fe' in kl and 'h' in kl:
                fe_col = col
                break
        # Final fallback: any column named like 'fe' or starting with 'fe'
        if fe_col is None:
            for col in df.columns:
                kl = col.lower()
                if kl == 'fe' or kl.startswith('fe'):
                    fe_col = col
                    break

        # If we found an Fe column ensure '[Fe/H]' exists as a canonical name
        if fe_col is not None and ('[Fe/H]' not in df.columns):
            df['[Fe/H]'] = df[fe_col]

        # For each abundance column that appears to be an [X/H] column,
        # add a derived '[X/Fe]' column equal to [X/H] - [Fe/H]
        if '[Fe/H]' in df.columns:
            for col in list(df.columns):
                # skip error columns and the Fe column itself
                if 'err' in col.lower():
                    continue
                if col == '[Fe/H]':
                    continue
                # try to extract element symbol from bracketed token like '[Eu/H]'
                m = re.match(r"\[\s*([^\]/]+)\s*/\s*H\s*\]", col)
                if m:
                    elem = m.group(1).strip()
                else:
                    # otherwise, derive a short element token from the column name
                    # take the leading alpha-numeric run
                    m2 = re.match(r"([A-Za-z0-9]+)", col)
                    if m2:
                        elem = m2.group(1).strip()
                    else:
                        continue

                # Skip Fe itself
                if elem.lower() == 'fe':
                    continue

                newname = f'[{elem}/Fe]'
                if newname not in df.columns and col in df.columns:
                    # compute derived abundance where possible
                    try:
                        df[newname] = df[col] - df['[Fe/H]']
                    except Exception:
                        # if arithmetic fails, leave it absent
                        pass
    except Exception:
        # Be conservative: parsing should not crash because of derived columns
        pass

    return df


def _find_column_for_element(df: pd.DataFrame, element: str) -> Optional[str]:
    """Find the best matching column name for an element like 'Fe' or 'Eu'.

    The function accepts element symbols and attempts to match columns named
    like 'fe_h', '[fe/h]', 'eu_h', 'eu/h', 'eu', etc.
    """
    el = element.strip()

    # Prefer explicit bracketed '[X/Fe]' columns if present (case-insensitive)
    bracket_target = f'[{el}/Fe]'
    for col in df.columns:
        if col.lower() == bracket_target.lower():
            return col

    # Next prefer '[X/H]' style columns
    bracket_h = f'[{el}/H]'
    for col in df.columns:
        if col.lower() == bracket_h.lower():
            return col

    # Otherwise try loose matching on the normalized name (fallback)
    el_l = el.lower()
    candidates = []
    for col in df.columns:
        key = col.lower()
        if re.search(rf"\b{re.escape(el_l)}\b", key):
            candidates.append(col)

    if not candidates:
        # Fallback: try columns that start with the element
        for col in df.columns:
            if col.lower().startswith(el_l):
                candidates.append(col)

    if not candidates:
        return None

    # Prefer columns that look like abundance (contain '/h' or '[' or 'h')
    for col in candidates:
        if '/' in col or 'h' in col:
            return col

    return candidates[0]


def extract_abundances(df: pd.DataFrame, x_elem: str = "Fe", y_elem: str = "Eu") -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray], Optional[np.ndarray]]:
    """Extract x, y and optional errors for two elements from DataFrame.

    Parameters:
    - df: DataFrame from `parse_stellab_file`.
    - x_elem: element for x-axis (e.g. 'Fe' for [Fe/H]).
    - y_elem: element for y-axis (e.g. 'Eu' for [Eu/Fe] or [Eu/H] depending
              on what the file contains).

    Returns
    - x: array of x values (float)
    - y: array of y values (float)
    - x_err: array or None
    - y_err: array or None

    Notes:
    - The function tries to find columns with names like 'fe_h', 'eu_h', etc.
    - If error columns are present they'll often appear as a following column
      named like '<column>_err' or just 'err' adjacent in the header; the
      function will attempt reasonable matches.
    """
    # find columns for x and y
    x_col = _find_column_for_element(df, x_elem)
    y_col = _find_column_for_element(df, y_elem)

    if x_col is None:
        raise KeyError(f"Could not find a column for element '{x_elem}' in DataFrame columns: {list(df.columns)}")
    if y_col is None:
        raise KeyError(f"Could not find a column for element '{y_elem}' in DataFrame columns: {list(df.columns)}")

    x = df[x_col].to_numpy(dtype=float)
    y = df[y_col].to_numpy(dtype=float)

    # Attempt to find error columns
    def _find_err_col(base_col: str) -> Optional[str]:
        # common patterns: base_col + '_err', 'err' adjacent, 'basecol_err'
        candidates = [f"{base_col}_err", f"{base_col}err", f"{base_col}__err"]
        for c in candidates:
            if c in df.columns:
                return c
        # Try generic 'err' columns near base_col's position
        try:
            idx = list(df.columns).index(base_col)
        except ValueError:
            return None
        # Look at next column
        if idx + 1 < len(df.columns):
            nxt = df.columns[idx + 1]
            if "err" in nxt or re.match(r"^err$", nxt):
                return nxt
        # No obvious err found
        return None

    x_err_col = _find_err_col(x_col)
    y_err_col = _find_err_col(y_col)

    x_err = df[x_err_col].to_numpy(dtype=float) if x_err_col is not None else None
    y_err = df[y_err_col].to_numpy(dtype=float) if y_err_col is not None else None

    # Filter NaNs (including those from sentinel values)
    mask = ~np.isnan(x) & ~np.isnan(y)
    x = x[mask]
    y = y[mask]
    if x_err is not None:
        x_err = x_err[mask]
    if y_err is not None:
        y_err = y_err[mask]

    return x, y, x_err, y_err


def plot_stellab_on_ax(ax, df: pd.DataFrame, x_elem: str = "Fe", y_elem: str = "Eu",
                       label: Optional[str] = None, fmt: str = "o", color: Optional[str] = None,
                       show_errors: bool = True, ms: float = 5.0, **kwargs):
    """Plot observations from a stellab DataFrame onto a Matplotlib axis.

    Parameters
    - ax: Matplotlib axis to draw on.
    - df: DataFrame returned by `parse_stellab_file`.
    - x_elem: element for x-axis (default 'Fe' == [Fe/H]).
    - y_elem: element for y-axis (default 'Eu' == [Eu/H] or [Eu/Fe]).
    - label: legend label.
    - fmt: marker style passed to `errorbar`/`plot`.
    - color: marker color.
    - show_errors: if True, draw errorbars when error columns exist.
    - ms: marker size.
    - kwargs: additional kwargs forwarded to `ax.errorbar` or `ax.plot`.

    Returns
    - handle: the Matplotlib artist returned (errorbar/Line2D)
    """
    import matplotlib.pyplot as plt

    x, y, x_err, y_err = extract_abundances(df, x_elem=x_elem, y_elem=y_elem)

    if show_errors and (x_err is not None or y_err is not None):
        xe = x_err if x_err is not None else None
        ye = y_err if y_err is not None else None
        handle = ax.errorbar(x, y, xerr=xe, yerr=ye, fmt=fmt, label=label, color=color, markersize=ms, linestyle='none', **kwargs)
    else:
        handle = ax.plot(x, y, fmt, label=label, color=color, markersize=ms, **kwargs)

    return handle


def ensure_abundance_columns(df: pd.DataFrame, elements: list, x_axis: str = 'Fe') -> pd.DataFrame:
    """Ensure bracket-style abundance columns '[X/Fe]' exist in `df`.

    For each element symbol in `elements`, this function will ensure a column
    named `[{elem}/Fe]` exists. If the column is missing it will be created
    and filled with NaNs so plotting code that expects the column will not
    fail. If a derived '[X/Fe]' exists already it is left unchanged.

    Parameters
    - df: DataFrame to operate on (modified in place and returned).
    - elements: list of element symbols (e.g. ['Mg','Eu']).
    - x_axis: element name for the x-axis baseline (unused currently but kept
              for future extension to e.g. '[X/Mg]'.)

    Returns
    - df: the same DataFrame (modified in place).
    """
    for elem in elements:
        colname = f'[{elem}/Fe]'
        if colname not in df.columns:
            df[colname] = np.nan
    return df


# If module executed as script, provide a tiny demo using the known paths in repo
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import os

    demo_paths = [
        os.path.join("stellab_data", "fornax_data", "Letarte_et_al_2010_stellab.txt"),
        os.path.join("stellab_data", "fornax_data", "Lemasle_et_al_2014_stellab.txt"),
    ]

    fig, ax = plt.subplots(figsize=(6, 4))
    for p in demo_paths:
        if not os.path.exists(p):
            print("Demo file not found:", p)
            continue
        df = parse_stellab_file(p)
        plot_stellab_on_ax(ax, df, x_elem='Fe', y_elem='Eu', label=os.path.basename(p))
    ax.set_xlabel('[Fe/H]')
    ax.set_ylabel('[Eu/H] or [Eu/Fe]')
    ax.legend()
    plt.show()
