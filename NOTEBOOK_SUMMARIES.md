# Fornax Notebook Summaries

## `Fornax_omega+.ipynb`
- Compare prompt vs stochastic MRD (magneto-rotational / r-process) channels using a 2-zone OMEGA+ framework and calibrate against Reichert et al. (2020) [Eu/Fe] observations.
- Convert Nishimura et al. MRD yields to a JINAPyCEE-compatible table and build metallicity-dependent DTDs for prompt and stochastic scenarios.
- Implement an episodic SFH (sfh_array), run baseline and MRD model scans, and plot best-fit spectroscopic tracks and RMS diagnostics.

## `Fornax_omega+_yields.ipynb`
- Prepare and inspect r-process / MRD yield inputs, converting external yield files into the JINAPyCEE yield-table format.
- Build and cache metallicity grid variants of MRD yield tables for use in OMEGA/OMEGA+ runs.
- Provide example usage of the yield table in a simple GCE run or diagnostic to validate the conversion.

## `Fornax_MRD_analysis.ipynb`
- Perform the core MRD analysis and calibration: fit MRD event rates and DTD shapes to Fornax [Eu/Fe] observations.
- Compare model variants (e.g., different DTDs, rates, or yield sets), compute goodness-of-fit metrics (RMS), and identify best-fit parameters.
- Produce summary plots and diagnostics (RMS vs rate, best-fit tracks, and possibly multi-element comparisons) to interpret model performance.

## `Fornax_burstySF.ipynb`
- Implement a bursty / episodic star-formation history for Fornax (from file) and convert it to `sfh_array` for model input.
- Re-run baseline and MRD prompt/stochastic scenarios under bursty SFH to test sensitivity of r-process enrichment to SFH bursts.
- Generate comparison plots vs observations and diagnostics to assess whether bursty SFHs change best-fit MRD rates or enrichment patterns.

