# Landfill Gas-to-Energy Projects (Atlanta MSA)

A command-line tool for analyzing landfill gas-to-energy (LFGTE) projects within the Atlanta MSA, using the EPA's [Landfill Methane Outreach Program (LMOP) database](https://www.epa.gov/lmop/landfill-technical-data).

## What it does

The script takes the LMOP database Excel export and:

1. **Filters to a hardcoded list of Atlanta MSA counties.**
2. **Filters to projects with a current status of** Operational, Construction, Planned, or Shutdown (excludes other/unknown statuses).
3. **Prints summary statistics** to the console:
   - Cumulative count of landfills with gas-to-energy projects, by benchmark year
   - Cumulative count of individual projects, by benchmark year (a landfill can have more than one project)
   - Total current-year greenhouse gas emission reductions (direct + avoided) across currently **active** projects
4. **Saves the active-projects dataset** as a CSV for further use.

## Requirements

- Python 3.8+
- Packages: `pandas`, `openpyxl` (needed by pandas to read `.xlsx` files)

Install with:

```bash
pip install pandas openpyxl
```

## Getting the input data

Download the LMOP database Excel file from the [EPA LMOP Project and Landfill Data by State page](https://www.epa.gov/lmop/project-and-landfill-data-state). The script expects a sheet named `LMOP Database` within that file, and expects the following columns to be present: `Landfill Name`, `County`, `Current Project Status`, `Project Start Date`, `Project Shutdown Date`, `Project Type Category`, `Actual MW Generation`, `Current Year Emission Reductions (MMTCO2e/yr) - Direct`, `Current Year Emission Reductions (MMTCO2e/yr) - Avoided`. A standard LMOP export should already contain all of these.

## Basic usage

```bash
python landfills-gas-to-energy.py path/to/lmopdataga.xlsx
```

## Command-line options

| Argument | Required? | Default | Description |
|---|---|---|---|
| `xlsx_path` | Yes | — | Path to the LMOP database Excel file (e.g. `lmopdataga.xlsx`). |

## Examples

**Run with defaults:**
```bash
python landfills-gas-to-energy.py lmopdataga.xlsx
```

## Outputs

- **Console output**:
  - A table of cumulative landfill counts (unique landfills with an active project) at each benchmark year (2005, 2015, 2025, 2026)
  - A table of cumulative project counts (individual projects, which can outnumber landfills) at each benchmark year
  - Total current-year emission reductions (MMTCO₂e/yr) summed across active projects
- **A filtered CSV** — one row per **active** project (Operational, Construction, or Planned, and with no shutdown date) in the Atlanta MSA, including a computed `Total Current Year Emission Reduction` column.

## Notes on the data

- **County list is hardcoded**, same as `solar-PV-landfills.py` — see that script's README for more on this, and how it compares to `ev-chargers.py`'s live boundary approach.
- **"Cumulative" accounts for shutdowns.** A project only counts toward a given benchmark year if it started on or before that year *and* either has no shutdown date or shut down after that year — so a project that started in 2010 and shut down in 2020 won't count toward the 2025 or 2026 totals.
- **Missing shutdown dates are treated as still active.** If `Project Shutdown Date` is blank, the script assumes the project is still running as of today.
- **The "active projects" CSV excludes Shutdown-status projects even though they're counted in the cumulative history tables** — the console tables include all four statuses (to show the full historical picture), but the saved CSV and the emission-reduction total only include projects that are currently Operational, Construction, or Planned with no shutdown date.
