# Atlanta MSA Landfill Gas-to-Energy Analysis
This project processes landfill gas-to-energy (LFGTE) project data from the EPA Landfill Methane Outreach Program (LMOP) Database and identifies projects located within the Atlanta Metropolitan Statistical Area (MSA). The script filters and cleans raw Excel data, handles missing values, tracks cumulative landfill gas-to-energy projects over time, and calculates current greenhouse gas emission reductions from active projects.

## Features
- Loads EPA LMOP landfill gas-to-energy project data from an Excel workbook
- Handles common file-reading errors
- Checks for required columns before analysis
- Cleans and standardizes county names
- Filters data to only include Atlanta MSA counties
- Cleans and standardizes project status values
- Filters projects to include:
  - Operational
  - Construction
  - Planned
  - Shutdown
- Accounts for project shutdown dates when calculating historical project counts
- Computes cumulative landfill gas-to-energy project counts for selected years: 2005, 2015, 2025, 2026
- Computes cumulative landfill counts with active gas-to-energy projects over time
- Identifies currently active landfill gas-to-energy projects
- Calculates total current-year greenhouse gas emission reductions (direct + avoided emissions)
- Returns total current-year emission reductions for active projects

## Technologies Used
- Python 3
- Pandas

## Input Data
The script expects an Excel workbook containing the EPA LMOP Database sheet with at least the following columns:
- Landfill Name
- County
- Current Project Status
- Project Start Date
- Project Shutdown Date
- Project Type Category
- Actual MW Generation
- Current Year Emission Reductions (MMTCO2e/yr) - Direct
- Current Year Emission Reductions (MMTCO2e/yr) - Avoided
- The data should be stored in a worksheet named: LMOP Database

## Outputs
The script generates:
- Cumulative landfill counts with gas-to-energy projects by year
- Cumulative landfill gas-to-energy project counts by year
- A table of currently active projects
- Total current-year greenhouse gas emission reductions from active projects (MMTCO₂e/year)

## Usage
- Download the latest EPA Landfill Methane Outreach Program (LMOP) Database from [https://www.epa.gov/lmop/project-and-landfill-data-state](url).
- Save the Excel file in the same folder as the Python script.
- Ensure the worksheet containing the project data is named: LMOP Database
- If needed, replace the filename at the end of the script: print(landfills_gas_to_energy("lmopdataga.xlsx"))
- Run the script: python landfill_gas_to_energy.py
