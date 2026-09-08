# Roman Strong Lensing Data Challenge

Analysis and methodology development for the **Roman Data Challenge for Dark Matter Substructure with Galaxy–Galaxy Strong Gravitational Lenses**.

The Nancy Grace Roman Space Telescope is expected to discover approximately $begin:math:text$10\^5$end:math:text$ galaxy–galaxy strong gravitational lenses. Roman's combination of wide-field coverage, depth, and high angular resolution will make it possible to use large samples of strong lenses to probe dark matter structure on sub-galactic scales.

The Roman Strong Lensing Data Challenge provides realistic simulated Roman observations of galaxy–galaxy strong lenses with different dark matter substructure populations. The challenge is designed to develop, test, and compare scalable methods for extracting dark-matter information from Roman strong-lensing observations.

## Scientific Goals

The challenge aims to:

- explore optimal approaches for strong-lensing substructure analysis;
- quantify how much information about dark matter can be extracted from Roman observations;
- determine which strong lenses are most informative for robust substructure measurements;
- develop methods that scale to Roman-sized datasets; and
- build a community focused on dark-matter studies with Roman strong lenses.

Strong gravitational lensing is sensitive to low-mass structure through perturbations to lensed arcs and images. Measurements of dark-matter subhalos and line-of-sight halos can therefore test the small-scale predictions of cold dark matter and alternative scenarios such as warm or self-interacting dark matter.

Potential inference targets include the presence and abundance of dark-matter halos, halo masses and locations, the substructure mass fraction, halo concentration, the half-mode mass, and population-level properties of the halo mass function.

## Data Challenge

The challenge is organized into progressively more demanding **rungs**.

| Rung | Goal | Status |
| --- | --- | --- |
| **Rung 0** | Infer the Einstein radius of the main deflector | Began October 2025 |
| **Rung 1** | Distinguish systems containing CDM substructure from smooth mass models | Began May 2026 |
| **Rung 2** | More advanced dark-matter substructure inference | Began Summer 2026 |

### Rung 0 — Einstein-radius regression

Rung 0 serves as an introduction to the challenge infrastructure and datasets. Participants train a regression model to infer the Einstein radius of simulated strong lenses.

The labeled dataset provides the quantities needed for training, while the unlabeled dataset withholds the Einstein radius and related parameters for evaluation.

### Rung 1 — Substructure classification

Rung 1 introduces direct sensitivity to dark-matter substructure. Participants train a binary classifier to determine whether a simulated lens contains a population of CDM subhalos.

The labeled dataset contains the substructure labels required for training. The corresponding unlabeled dataset withholds the substructure flag and related quantities and is used to evaluate submissions.

### Rung 2

Rung 2 extends the challenge toward more realistic inference of dark-matter substructure properties. See the official challenge documentation for the current specification and releases.

## Simulations

Challenge datasets are generated with [`mejiro`](https://github.com/AstroMusers/mejiro), a pipeline for producing realistic diffraction-limited images of galaxy–galaxy strong gravitational lenses.

`mejiro` combines several components of the strong-lensing and image-simulation ecosystem, including:

- [`SLSim`](https://github.com/LSST-strong-lensing/slsim) for populations of strong-lensing systems;
- [`lenstronomy`](https://github.com/lenstronomy/lenstronomy) for gravitational-lensing calculations;
- [`pyHalo`](https://github.com/dangilman/pyHalo) for dark-matter subhalos and line-of-sight structure;
- `STPSF` for the Roman point-spread function; and
- `romanisim` for Roman detector/image simulation.

The resulting datasets incorporate astrophysical lens populations, dark-matter structure, Roman optics, and detector effects.

Participants normally **do not need to generate the challenge datasets themselves**. Researchers interested in custom simulations can use `mejiro`; see the official challenge documentation for setup and configuration instructions.

## Data

Challenge datasets are publicly archived on **Zenodo**.

### Rung 0

The Rung 0 releases contain simulated Roman strong-lens images and associated metadata for Einstein-radius regression.

Current releases include updated simulations using `romanisim`. In these releases, image values correspond to Roman L2-like units of DN/s. The latest Rung 0 unlabeled release restores the image dimensions to $begin:math:text$91\\times91$end:math:text$ pixels, corresponding to approximately $begin:math:text$10\.01\'\'$end:math:text$ on a side, to match the training dataset.

### Rung 1

The Rung 1 dataset contains simulated systems with and without CDM substructure for binary classification.

The current unlabeled Rung 1 release corrects an exposure-time inconsistency in the earlier simulations. Participants should consult the Zenodo records and official documentation for the latest dataset versions before beginning an analysis.

The datasets can be large—several GB per release—so they should generally **not be committed to this repository**.

A convenient local layout is

```text
data/
├── rung_0/
│   ├── labeled/
│   └── unlabeled/
└── rung_1/
    ├── labeled/
    └── unlabeled/
```

Add local data products, trained models, and other large generated files to `.gitignore`.

## This Repository

This repository is intended for analysis of the Roman Strong Lensing Data Challenge datasets and development of methods for extracting strong-lensing and dark-matter information from Roman observations.

A useful organization is

```text
Roman_Strong_Lensing_Data_Challenge/
├── notebooks/       # Tutorials, exploration, and outward-facing analyses
├── src/             # Reusable analysis and modeling functions
├── scripts/         # Training, inference, and evaluation scripts
├── configs/         # Analysis and model configurations
├── results/         # Lightweight derived results
├── figures/         # Publication-quality figures
└── README.md
```

Where possible, reusable functionality should live in `src/` rather than being duplicated across notebooks. Notebooks should primarily demonstrate workflows, inspect datasets, visualize results, and document scientific analyses.

## Getting Started

Clone this repository:

```bash
git clone https://github.com/AstroMusers/Roman_Strong_Lensing_Data_Challenge.git
cd Roman_Strong_Lensing_Data_Challenge
```

Create an isolated Python environment appropriate for the analysis being performed, then download the relevant labeled and unlabeled challenge datasets from Zenodo.

The notebooks distributed with the Zenodo datasets provide examples for inspecting the HDF5 files and are a useful starting point for understanding the data structure.

For work requiring new simulated lenses rather than the released datasets, install `mejiro` following its documentation. Generating custom challenge-like simulations requires additional Roman technical-information and PSF setup; see the official challenge documentation before attempting a local installation.

## Resources

- **Official challenge documentation:** https://roman-data-challenge.readthedocs.io/
- **`mejiro` simulation pipeline:** https://github.com/AstroMusers/mejiro
- **`mejiro` documentation:** https://mejiro.readthedocs.io/
- **AstroMusers Roman Strong Lensing WFS Program:** https://sites.wustl.edu/astromusers/roman-strong-lensing-wfs-program/
- **NASA WFS program description:** https://science.nasa.gov/mission/roman-space-telescope/preparing-for-a-leap-precursor-strong-lensing-science-with-roman-towards-precision-cosmology/
- **Rung 0 datasets:** search Zenodo for *Rung 0 Dataset for Roman Strong Lens Data Challenge*
- **Rung 1 datasets:** search Zenodo for *Rung 1 Dataset for Roman Strong Lens Data Challenge*

For questions about the challenge, contact: `tansu@wustl.edu.`

Discussion also takes place in the **#strong-lensing** channel of the Roman Space Telescope Slack.

Announcements related to the Roman strong-lensing program are distributed through:

`romanstronglensing@lists.physics.wustl.edu`

To join the mailing list, email:

`romanstronglensing-join@lists.physics.wustl.edu`

## Team

The Roman strong-lensing simulation and data-challenge effort is led by researchers at **Washington University in St. Louis** and **Stony Brook University**, with collaborators across the strong lensing, dark matter, and Roman communities.

Core contributors to the public challenge datasets include:

- Bryce Wedig — Washington University in St. Louis
- Alan Huang — Stony Brook University
- Simon Birrer — Stony Brook University (co-I)
- Tansu Daylan — Washington University in St. Louis (PI)

The broader Roman Strong Lensing WFS team includes Aysu Ece Sarıcaoğlu, Jodie Xiao, Rahul Karthik, and collaborators Francis-Yan Cyr-Racine, Cora Dvorkin, Douglas P. Finkbeiner, Priyamvada Natarajan, Anna M. Nierenberg, Annika Peter, Justin D. R. Pierel, and Risa H. Wechsler.

## Citation

If you use the challenge simulations, please cite the relevant Zenodo dataset release and the papers describing the Roman strong-lensing forecasts and `mejiro`.

In particular, please cite:

- **Wedig et al. (2025), _The Roman View of Strong Gravitational Lenses_**
- the appropriate **Roman Strong Lens Data Challenge Zenodo dataset**
- `mejiro`, when simulations or software from that package are used

Consult the `mejiro` repository and individual Zenodo records for current citation metadata and DOIs.

## Acknowledgments

This work is supported by the National Aeronautics and Space Administration under grant **80NSSC24K0095**, *Preparing for a leap: Precursor Strong Lensing Science with Roman Towards Precision Cosmology*, issued by the Astrophysics Division of NASA's Science Mission Directorate, and by the **McDonnell Center for the Space Sciences at Washington University in St. Louis**.

The challenge builds on software and infrastructure developed by the broader Roman, strong-lensing, and open-source astronomy communities.
