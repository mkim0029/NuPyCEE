# OMEGA+ DTD (Delay-Time Distribution) Parameter Reference

## Summary

Based on analysis of the NuPyCEE repository, the correct parameter name for passing a Delay-Time Distribution (DTD) array to OMEGA+ model initialization is:

### **`nsmerger_dtd_array`**

This parameter is used to pass custom Delay-Time Distribution curves for neutron star merger (NSM) / magneto-rotational dynamo (MRD) r-process enrichment.

---

## Parameter Details

### Parameter Name
- **`nsmerger_dtd_array`** (primary parameter)

### Format & Structure

The `nsmerger_dtd_array` expects a **nested list structure**:

```
nsmerger_dtd_array = [[ [time_array, rate_array, Z_value], [time_array, rate_array, Z_value], ... ]]
```

**Outer structure:**
- Top level: List of sources (typically one source: `[[ ... ]]`)
- Second level: List of metallicity-dependent DTD curves

**Per-metallicity entry structure:**
```
[time_array, rate_array, metallicity_value]
```

where:
- `time_array`: List of time points (Gyr or years, depending on your convention)
- `rate_array`: Corresponding DTD values at each time point (dimensionless or in events/yr)
- `metallicity_value`: Metallicity Z for this curve

### Example from Fornax_omega+.ipynb

**Prompt DTD builder:**
```python
def build_prompt_dtd(
    metallicities: list[float],
    prompt_window: tuple[float, float] = (3.0e6, 3.0e8),
    t_end: float = 12.0e9,
) -> list[list[list[float]]]:
    """
    Build a simple "prompt" Delay-Time Distribution (DTD) curve for MRD enrichment.
    """
    t_start, t_stop = prompt_window
    
    # Piecewise curve: 0 → prompt_window → 0
    base_curve = [
        [0.0, 0.0],
        [t_start, 0.0],
        [t_start * 1.001, 1.0],
        [t_stop, 1.0],
        [t_stop * 1.001, 0.0],
        [t_end, 0.0],
    ]

    # Return format: outer list per source, inner list per metallicity
    return [[ [point[:] for point in base_curve] for _ in metallicities ]]
```

**Stochastic DTD builder:**
```python
def build_stochastic_dtd(
    metallicities: list[float],
    event_times: list[float],
    width: float = 2.0e7,
    t_end: float = 13.0e9,
) -> list[list[list[float]]]:
    """Build a spiky DTD to emulate stochastic MRD events at discrete times."""
    
    curve = [[0.0, 0.0]]
    for t_event in sorted(event_times):
        start = max(curve[-1][0], max(0.0, t_event - width))
        if start > curve[-1][0]:
            curve.append([start, 0.0])
        curve.append([t_event - 0.5 * width, 1.0])
        curve.append([t_event + 0.5 * width, 1.0])
        curve.append([t_event + width, 0.0])
    
    if curve[-1][0] < t_end:
        curve.append([t_end, 0.0])
    
    return [[ [point[:] for point in curve] for _ in metallicities ]]
```

---

## Related MRD Parameters

When using `nsmerger_dtd_array`, ensure these related parameters are correctly set:

### 1. **`ns_merger_on`** (boolean)
   - **Required:** `True` to enable neutron star merger contributions
   - **Default:** `False`
   - **Purpose:** Activates NSM/MRD enrichment in the model

### 2. **`nb_nsm_per_m`** (float)
   - **Required:** Event rate (events per solar mass formed)
   - **Default:** `1.0e-5`
   - **Purpose:** Sets the overall NSM event rate; scales the DTD curve
   - **Units:** Events per solar mass of stars formed
   - **Example:** `1.0e-5` to `1.0e-3` for typical models

### 3. **`nsm_yields_table`** (string)
   - **Required:** Path to NSM/MRD yield table
   - **Default:** None (uses built-in table if available)
   - **Purpose:** Specifies which nucleosynthesis yields to use for NSM products
   - **Format:** File path relative to repository root or absolute path
   - **Example:** `"yield_tables/MRD_r_process_JINAPyCEE.txt"`

### 4. **`nsmerger_table`** (string)
   - **Alternative parameter:** Older name, similar to `nsm_yields_table`
   - **Note:** Verify which parameter name is used in your version

---

## Complete Usage Example

From `Fornax_omega+.ipynb`:

```python
from functools import partial
import omega_plus

# Build DTD curves for your metallicity grid
metallicity_grid = [1.0e-4, 5.0e-4, 1.0e-3, 2.0e-3]

# Create a prompt DTD builder
prompt_builder = partial(build_prompt_dtd, prompt_window=(3.0e6, 3.0e8))

# Build the DTD for this metallicity grid
dtd = prompt_builder(metallicity_grid)

# Create OMEGA+ model with DTD
model = omega_plus.omega_plus(
    ns_merger_on=True,                              # Enable NSM
    nb_nsm_per_m=1.0e-5,                           # Event rate
    nsmerger_dtd_array=dtd,                        # DTD curve
    nsm_yields_table="path/to/yields/table.txt",  # Yield table
    imf_yields_range=[1.0, 40.0],
    table="yield_tables/agb_and_massive_stars_C15_LC18_R_mix.txt",
    iolevel=0,
    special_timesteps=100,
)
```

---

## Time Units

**Important:** Verify the time units used in your DTD:
- The examples in `build_prompt_dtd` use **years** (Gyr specified as `12.0e9` yr)
- Ensure your time array is consistent with the model's internal time convention
- Typically: `3.0e6` = 3 Myr, `3.0e8` = 300 Myr, `12.0e9` = 12 Gyr

---

## Source Files

- **Parameter definition:** `/home/minjih/NuPyCEE/chem_evol.py` (lines 478, 570-571)
- **Usage examples:** `/home/minjih/NuPyCEE/Fornax_omega+.ipynb` (DTD builders and evaluation functions)
- **OMEGA+ module:** `/home/minjih/NuPyCEE/omega.py`

---

## Common Issues & Debugging

### Issue: DTD parameter not recognized
- **Check:** Parameter name is exactly `nsmerger_dtd_array` (not `dtd_array` or `nsm_dtd_array`)
- **Check:** Passed via keyword argument: `nsmerger_dtd_array=dtd`

### Issue: DTD has no effect
- **Check:** `ns_merger_on=True` is set
- **Check:** `nb_nsm_per_m` > 0 (event rate is not zero)
- **Check:** `nsm_yields_table` points to valid file

### Issue: Metallicity mismatch
- **Check:** DTD curves provided for all metallicities used in the model
- **Check:** Metallicity values in DTD match model's metallicity grid

---

## References

The parameter `nsmerger_dtd_array` is inherited from the `chem_evol` base class and used by both `SYGMA` and `OMEGA` models through the inheritance hierarchy.

Definition hierarchy:
1. `chem_evol.__init__()` accepts `nsmerger_dtd_array` parameter
2. `omega.__init__()` inherits via `chem_evol.__init__()`
3. `omega_plus.omega_plus.__init__()` passes through via `**kwargs`
