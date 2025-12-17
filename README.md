# ASTR501 Final Project — Fornax Chemical Evolution Trend

This repository addition contains the analysis and figures for the ASTR501 final project (Fornax chemical evolution).  This README summarizes what is new to the NuPyCEE repo for this project, points to the main analysis notebook, and lists each figure produced with short assessor notes.

**New Items Added**
- **Notebook**: Fornax Chemical Evolution Trend.ipynb — main analysis notebook performing galactic chemical evolution experiments and generating figures. See [Fornax Chemical Evolution Trend.ipynb](Fornax%20Chemical%20Evolution%20Trend.ipynb)
- **Figures folder**: figures/ — contains PDF outputs produced by the notebook. See [figures](figures)
- **Observations**: observations/ — contains the processed observational catalog used (Reichert et al. 2020 CSV). See [observations](observations)
- **Extra yields**: yield_tables/additional_sources/ — contains MRD-SNe yield files (e.g., L0.75.dat). See [yield_tables/additional_sources](yield_tables/additional_sources)

**How to reproduce**
1. Ensure the `NuPyCEE` package and Python dependencies are available (numpy, pandas, matplotlib). The notebook expects the local package structure so run it from the repository root.
2. Open the notebook [Fornax Chemical Evolution Trend.ipynb](Fornax%20Chemical%20Evolution%20Trend.ipynb) and execute cells in order (or `Run All`). The notebook creates the figures saved into `figures/`.

**Figures produced by the notebook**

**Fornax Grid (figures/fornax_grid.pdf)**
- Notebook: [Fornax Chemical Evolution Trend.ipynb](Fornax%20Chemical%20Evolution%20Trend.ipynb)
- File: [figures/fornax_grid.pdf](figures/fornax_grid.pdf)
- Description: Multi-panel grid plotting elemental abundance trends (elements include Mg, Sc, Ti, Cr, Mn, Ni, Y, Ba, Eu) vs [Fe/H]. The notebook overlays four model predictions on observational data from Letarte et al. (2010), Lemasle et al. (2014) and Reichert et al. (2020).
- Models plotted (labels used in the legend):
  - `r-process: NSM` (baseline, `o_1`)
  - `r-process: NSM + MRD-SNe` (`o_2`)
  - `r-process: NSM + extra MRD-SNe` (`o_ext`)
  - `r-process: extra NSM + MRD-SNe` (`o_3`)
- Assessor note: Compare model trajectories to the three observational datasets. The figure is intended to show how prompt MRD-SNe and delayed NSM channels affect element-specific trends.

**Fornax 2x2 (figures/fornax_2x2.pdf)**
- Notebook: [Fornax Chemical Evolution Trend.ipynb](Fornax%20Chemical%20Evolution%20Trend.ipynb)
- File: [figures/fornax_2x2.pdf](figures/fornax_2x2.pdf)
- Description: 2×2 panel of key abundance ratios vs [Fe/H]:
  - Top-left: `[Mg/Fe]` vs `[Fe/H]`
  - Top-right: `[Ba/Mg]` vs `[Fe/H]` (computed as `[Ba/Fe] - [Mg/Fe]`)
  - Bottom-left: `[Ba/Eu]` vs `[Fe/H]` (computed as `[Ba/Fe] - [Eu/Fe]`)
  - Bottom-right: `[Eu/Mg]` vs `[Fe/H]` (computed as `[Eu/Fe] - [Mg/Fe]`)
- Models plotted: same set as in the grid (o_1, o_2, o_ext, o_3).
- Assessor note: These ratios are chosen to highlight the relative timing and channels of r-process enrichment (prompt vs delayed). Pay attention to interpolation behaviour used when model x-grids differ — the notebook interpolates one model onto another's x-grid for ratio computations.

**Notes on inputs and provenance**
- Observations: the processed Reichert et al. (2020) Fornax Eu catalog is `observations/reichert2020_for.csv`. The notebook will raise an error if the file is missing and provides the script to regenerate it.
- Yields: NSM yields from Rosswog et al. (2014) and MRD-SNe yields (e.g., `L0.75.dat`) are read from `yield_tables/` and `yield_tables/additional_sources/` respectively. These are used to manually inject r-process mass in model runs.
----------------
### Original README file for NuPyCEE

[![Build Status](https://travis-ci.org/NuGrid/NuPyCEE.svg?branch=master)](https://travis-ci.org/NuGrid/NuPyCEE) [![DOI](https://zenodo.org/badge/51356355.svg)](https://zenodo.org/badge/latestdoi/51356355)

NuPyCEE
=======

Public NuGrid Python Chemical Evolution Environment

This is a code repository containing the simple stellar population code SYGMA (Stellar Yields for Galactic Modeling Applications), the single-zone galaxy code OMEGA (One-zone Model for the Evolution of Galaxies), and the observational data plotting tool STELLAB (Stellar Abundances). 

**Requirement**: The codes are now in Python3 and use the "future" module.

**Online usage**: These tools can be used directly online via the public <a href="http://www.nugridstars.org/projects/wendi">WENDI interface</a>.

**Userguides**: See the <a href="https://github.com/NuGrid/NuPyCEE/tree/master/DOC"> Documentation </a> folder.

**Acknowledgments**: 

* SYGMA: Please refer to <a href="http://adsabs.harvard.edu/abs/2017arXiv171109172R">Ritter et al. (2017)</a>.

* OMEGA: Please refer to <a href="http://adsabs.harvard.edu/abs/2016arXiv160407824C">Côté et al. (2017)</a>.

* STELLAB: Please refer to the <a href="http://adsabs.harvard.edu/abs/2016ascl.soft10015R">NuPyCEE code library</a>.


### Installation Instructions

* Create the directory where you want to download the codes.
* Go in that directory with a terminal and clone the GitHub repository:
	* `git clone https://github.com/NuGrid/NuPyCEE.git`
* From the same directory which contains the cloned NuPyCEE directory, you can import the codes in Python mode by typing:
	* `from NuPyCEE import omega`
	* `from NuPyCEE import sygma`
	* `from NuPyCEE import stellab`
* If you want to import the NuPyCEE codes from anywhere else within your work space, you have to update your Python path using a terminal:
	* `export PYTHONPATH="your_path_to_before_NuPyCEE:$PYTHONPATH"`
	* **Example**: `export PYTHONPATH="benoitcote/gce_code:$PYTHONPATH"`
	* **Important**: Do not forget `:$PYTHONPATH` at the end, otherwise the python path will be overwritten.
	* **Note**: All `export` commands should be put into your bash file. With MAC, it is the .bash_profile file in your home directory. Otherwise, you will need to define the paths each time you open a terminal.

### Installation of the Decay Module for Using Radioactive Isotopes

* In the NuPyCEE folder, type the following
	* `f2py -c decay_module.f95 -m decay_module`
	* **Note**: Use the f2py version that will be compatible with your Python version.
