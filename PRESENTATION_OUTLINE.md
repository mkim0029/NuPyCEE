# The Europium Problem in Fornax

Duration: ~15 minutes (12–14 slides)

Audience: Graduate-level astrophysics students; accessible to broader astronomy students

Primary results to showcase:
- [Eu/Fe] vs [Mg/Fe] overlay (observations + two models)
- [X/Fe] vs [Fe/H] grid for X = [Mg, Sc, Ti, Cr, Mn, Ni, Y, Ba, Eu], for two models:
  1) Baseline with NSM r-process yields
  2) Baseline + prompt MRD (magneto-rotational) r-process channel

---

## Slide 1 — Title
- Title: The Europium Problem in Fornax
- Presenter, affiliation, date
- One-liner: Why Eu in Fornax challenges simple enrichment scenarios

Visuals:
- Small inset: Fornax dSph image/map; Eu periodic table highlight

References:
- None required on title slide

---

## Slide 2 — Motivation: Why care about Eu?
- Eu as a largely r-process tracer → a chemical “tag” of rare/high-yield events
- Dwarfs are ideal laboratories: low SFRs, bursty histories, strong outflows
- Fornax is intriguing: massive for a classical dSph, extended SFH, rich datasets
- Impact: Constraining r-process sites, event rates, and galaxy formation physics

Visuals:
- Schematic: timeline of CCSNe (prompt), SNe Ia (delayed), r-process channels (varying delays)

References:
- Sneden, Cowan & Gallino 2008 ARA&A (r-process review)
- Tolstoy, Hill & Tosi 2009 ARA&A (dSph chemo-dynamics review)

---

## Slide 3 — State of the Art (Observations)
- High-res abundances in Fornax: large samples, multiple elements
- Eu measurements exist across metallicity; trends differ from some classical dSphs
- Eu scatter at low [Fe/H] vs more coherent behavior at later times

Visuals:
- Bullet logos of key surveys; later slides carry the data figures

References:
- Letarte et al. 2010 (Fornax abundances)
- Lemasle et al. 2014 (Fornax abundances)
- Reichert et al. 2020 (Eu in Fornax; data used here)

---

## Slide 4 — State of the Art (Theory)
- Proposed r-process sites: NS-NS mergers (delayed), collapsars/MRD/jet SNe (prompt-ish), NS-BH
- Chemical evolution tension: Pure NSM often delays Eu too much in dwarfs
- Inhomogeneous enrichment and bursty SFHs can amplify scatter

Visuals:
- Timeline bar chart: relative delays/yields for CCSN, AGB, SNe Ia, NSM, MRD

References:
- Rosswog et al. 2014 (NSM yields)
- Asplund et al. 2009 (solar normalization)
- Côté et al. 2017+ (NuPyCEE/OMEGA framework)

---

## Slide 5 — Goals and Objectives
- Characterize Eu behavior in Fornax vs other classical dSphs
- Test whether a prompt r-process channel (MRD) helps reproduce Eu trends
- Evaluate trade-offs across elements with grid comparisons
- Use Eu as a chemical tag to infer event timing and SFH complexity

Visuals:
- Simple checklist infographic of the four objectives

References:
- None new

---

## Slide 6 — Data and Model Setup (Methods)
- Observations: STELLAB catalogs (Letarte 2010; Lemasle 2014) + Reichert 2020 Eu
- Model: NuPyCEE OMEGA one-zone, Fornax parameters (sfe, mass_loading, SNe Ia DTD)
- Two models:
  1) Baseline: NSM r-process only
  2) Baseline + prompt MRD injection in early window (e.g., 0–30 Myr)
- Assumptions: instantaneous mixing, fixed yields, chosen DTDs; identical SFH for fair comparison

Visuals:
- Table snippet of key parameters (sfe, mass_loading, nb_1a_per_m, yield tables)

References:
- Côté et al. 2017 ApJS (NuPyCEE/OMEGA)
- Rosswog et al. 2014 (NSM)
- MRD channel: magneto-rotational jet SNe literature (e.g., Winteler 2012; Nishimura 2015)

---

## Slide 7 — What Eu/Mg Reveals
- Mg traces prompt CCSNe; Eu traces r-process → relative timing diagnostic
- Early Eu rise implies prompt r-process; delayed rise implies NSM dominance
- Eu as a chemical tag: tracks rare, high-yield events and their DTD

Visuals:
- Conceptual [Eu/Fe] vs [Mg/Fe] schematic with “prompt” vs “delayed” annotations

References:
- Sneden, Cowan & Gallino 2008

---

## Slide 8 — Result: [Eu/Fe] vs [Mg/Fe] (Fornax)
- Plot: Observations + Baseline (NSM-only) + Baseline+MRD (prompt)
- Key read-outs:
  - NSM-only: later Eu rise; struggles to match early/mid Eu levels
  - +MRD: earlier Eu lift, better alignment with data at lower [Mg/Fe]
- Takeaway: A prompt component improves Eu timing

Visuals:
- Use notebook output: `plot_spectro_with_observations(o_1, x='[Mg/Fe]', y='[Eu/Fe]')` and with `o_ext`
- Distinct line styles/colors for the two models; shared legend

References:
- Reichert et al. 2020 (data)

---

## Slide 9 — Result: [X/Fe] vs [Fe/H] Grid (Baseline)
- Nine-panel grid for X = Mg, Sc, Ti, Cr, Mn, Ni, Y, Ba, Eu (Baseline)
- What works: Mg plateau and knee behavior consistent with extended SFH
- Tensions: Fe-peak (Ti/Cr/Mn/Ni) and n-capture (Y/Ba/Eu) mismatches illustrate model limits

Visuals:
- Use `plot_grid(o_1, title='Baseline model')`

References:
- Asplund et al. 2009 (solar)
- Letarte 2010; Lemasle 2014; Reichert 2020 (observations)

---

## Slide 10 — Result: [X/Fe] vs [Fe/H] Grid (+MRD)
- Same grid with MRD prompt channel
- Improvements: Eu trends rise earlier; better qualitative agreement in Eu panel
- Cross-check other elements remain broadly consistent (no unintended degradations)

Visuals:
- Use `plot_grid(o_ext, title='Baseline + prompt MRD')`

References:
- Rosswog 2014 (NSM)
- MRD references (e.g., Winteler 2012; Nishimura 2015)

---

## Slide 11 — Fornax vs Other Classical dSphs
- Fornax: more massive, extended SFH, prolonged SNe Ia influence → lower [Mg/Fe] at given [Fe/H]
- Eu: relative timing differs from Sculptor/Carina trends; Fornax suggests need for (at least some) prompt r-process
- Chemical fingerprint: Eu helps disentangle r-process channels and SFH

Visuals:
- Comparative schematic: Eu behavior in Fornax vs “typical” classical dSph trend shapes

References:
- Tolstoy, Hill & Tosi 2009 (review)

---

## Slide 12 — Interpretation: What the Models Say
- Eu requires a mixture of channels and/or shorter DTD tail than pure NSM
- Fornax’s extended SFH and strong outflows modulate abundance tracks and timescales
- Prompt MRD improves Eu timing without breaking alpha trends → plausible contribution

Visuals:
- Single panel highlighting Eu panel changes across models with callouts

References:
- Côté et al. 2017; Rosswog 2014; MRD literature

---

## Slide 13 — Assumptions and Limitations
- One-zone, instantaneous mixing (no spatial/stochastic effects)
- Fixed yields and DTD prescriptions; MRD normalization/window simplified
- Potential inflow/outflow and SFH degeneracies

Visuals:
- “Caution” callouts near key assumptions

References:
- NuPyCEE/OMEGA docs and related papers

---

## Slide 14 — Outlook
- Calibrate MRD normalization and timing window vs Eu constraints (grid/RMS fits)
- Explore mixed-channel r-process models (NSM + MRD + collapsars)
- Try inhomogeneous/stochastic models to reproduce early-time scatter
- Jointly tune inflow/outflow and SFH against multi-element grid

Visuals:
- Roadmap diagram

References:
- Relevant modeling literature as above

---

## Slide 15 — Conclusions
- Eu in Fornax rises earlier than NSM-only predicts → prompt r-process improves agreement
- Eu acts as an incisive chemical tag for rare events and DTDs
- Fornax’s complex SFH and outflows shape multi-element trends; multi-channel r-process is favored

Visuals:
- Reprise the [Eu/Fe] vs [Mg/Fe] figure with a succinct takeaway box

References:
- As cited across slides

---

## Slide 16 (Optional) — Backup
- Model parameters, yield tables, and DTD settings
- Additional plots or alternative MRD windows

---

## Figure Assembly Notes (for your convenience)
- [Eu/Fe] vs [Mg/Fe]: use `plot_spectro_with_observations(model, x='[Mg/Fe]', y='[Eu/Fe]')` for both `o_1` and `o_ext`; distinguish line styles/colors; single legend outside RHS.
- Nine-panel grids: `plot_grid(o_1, ...)` and `plot_grid(o_ext, ...)`; consistent axes and titles; include a single figure-level legend.
- When describing model differences, annotate early-time Eu uplift in MRD case and note any trade-offs across other elements.

## References (short list)
- Asplund, Grevesse, Sauval & Scott 2009, ARA&A (solar abundances)
- Côté et al. 2017, ApJS (NuPyCEE/OMEGA framework)
- Letarte et al. 2010, A&A (Fornax abundances)
- Lemasle et al. 2014, A&A (Fornax abundances)
- Reichert et al. 2020 (Fornax Eu catalog used here)
- Rosswog et al. 2014 (NSM nucleosynthesis yields)
- Sneden, Cowan & Gallino 2008, ARA&A (r-process review)
- Tolstoy, Hill & Tosi 2009, ARA&A (dSph chemical evolution review)
- Winteler et al. 2012; Nishimura et al. 2015 (magneto-rotational/jet SNe as prompt r-process)
