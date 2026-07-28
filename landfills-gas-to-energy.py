import pandas as pd
import argparse

atlanta_msa_counties = [
    "Barrow", "Clayton", "Douglas", "Haralson", "Meriwether", 
    "Pike", "Bartow", "Cobb", "Fayette", "Heard", "Morgan", 
    "Rockdale", "Butts", "Coweta", "Forsyth", "Henry", "Newton", 
    "Spalding", "Carroll", "Dawson", "Fulton", "Jasper", "Paulding", 
    "Walton", "Cherokee", "DeKalb", "Gwinnett", "Lamar", "Pickens"]

def landfills_gas_to_energy(file_path):
    # Reads CSV file
    try:
        landfills_gas_to_energy_df = pd.read_excel(file_path, sheet_name='LMOP Database')
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a parsing error while reading the file.")
        return None
    
    # Check for required columns
    must_have_columns = ['Landfill Name', 'County', 'Current Project Status', "Project Start Date", "Project Shutdown Date", "Project Type Category", "Actual MW Generation",
                       "Current Year Emission Reductions (MMTCO2e/yr) - Direct", "Current Year Emission Reductions (MMTCO2e/yr) - Avoided"] 

    missing_cols = [col for col in must_have_columns if col not in landfills_gas_to_energy_df.columns]
    if missing_cols:
        print(f"Missing columns: {missing_cols}")
        return None

     # Clean 'County' column and filter for Atlanta MSA counties
    landfills_gas_to_energy_df['County'] = landfills_gas_to_energy_df['County'].fillna('').str.strip() # can't do title case because of "DeKalb"
    # Case-insensitive filter
    atlanta_msa_counties_lower = {c.lower() for c in atlanta_msa_counties}
    landfills_gas_to_energy_df = landfills_gas_to_energy_df[landfills_gas_to_energy_df['County'].str.lower().isin(atlanta_msa_counties_lower)]

    # Clean 'Current Project Status' column and filter for Operational, Construction, Planned, and Shutdown projects
    landfills_gas_to_energy_df['Current Project Status'] = landfills_gas_to_energy_df['Current Project Status'].fillna('').str.strip().str.lower()
    landfills_gas_to_energy_df = landfills_gas_to_energy_df[landfills_gas_to_energy_df['Current Project Status'].isin(['operational', 'construction', 'planned', 'shutdown'])]    
    
    '''Cumulative count of landfill gas-to-energy projects over time'''
    # If project shutdown date exists then account for that in the cumulative count by not counting projects that have shut down by the target year. 
    # If shutdown date is missing, assume project is still operational and count it.
    landfills_gas_to_energy_df['Project Start Date'] = pd.to_datetime(landfills_gas_to_energy_df['Project Start Date'],errors='coerce')
    landfills_gas_to_energy_df['Project Shutdown Date'] = pd.to_datetime(landfills_gas_to_energy_df['Project Shutdown Date'],errors='coerce')

    # Years to evaluate
    target_years = [2005, 2015, 2025, 2026]

    # Build cumulative counts
    cumulative_project_counts = []
    cumulative_landfill_counts = []

    for year in target_years:
        active_projects = landfills_gas_to_energy_df[
        (landfills_gas_to_energy_df['Project Start Date'].dt.year <= year)
        &
        (landfills_gas_to_energy_df['Project Shutdown Date'].isna()
            |
            (landfills_gas_to_energy_df['Project Shutdown Date'].dt.year > year))]
        
        landfill_count = active_projects['Landfill Name'].nunique()

        cumulative_project_counts.append({'Year': year, 'Cumulative Projects': len(active_projects)})
        cumulative_landfill_counts.append({'Year': year, 'Cumulative Landfills': landfill_count})

    # Convert to DataFrame
    project_gas_to_energy_years = pd.DataFrame(cumulative_project_counts)
    landfill_gas_to_energy_years = pd.DataFrame(cumulative_landfill_counts)

    # Print table
    print("\nCumulative Landfills Planning/Operating Gas-to-Energy Projects Over Time")
    print(landfill_gas_to_energy_years.to_string(index=False))
    print("\nCumulative Landfill Gas-to-Energy Projects Over Time")
    print(project_gas_to_energy_years.to_string(index=False))

    active_landfills_gas_to_energy_df = landfills_gas_to_energy_df[landfills_gas_to_energy_df['Current Project Status'].isin(['operational', 'construction', 'planned']) & landfills_gas_to_energy_df['Project Shutdown Date'].isna()].copy()
    # Create new dataframe for active projects only and need to exclude projects with a shutdown date even if they are marked as operational, construction, or planned
    # have to make a copy of the filtered dataframe to avoid SettingWithCopyWarning when creating the new column for total emission reduction

    active_landfills_gas_to_energy_df['Total Current Year Emission Reduction'] = (active_landfills_gas_to_energy_df['Current Year Emission Reductions (MMTCO2e/yr) - Direct'].fillna(0) 
                                                                     + active_landfills_gas_to_energy_df['Current Year Emission Reductions (MMTCO2e/yr) - Avoided'].fillna(0))
    
    print(f"\nTotal Current Year Emission Reduction from Active Landfill Gas-to-Energy Projects in Atlanta MSA: {active_landfills_gas_to_energy_df['Total Current Year Emission Reduction'].sum():.3f} MMTCO₂e/yr") 

    output_path = "atlanta_msa_landfill_gas_to_energy_projects.csv"
    active_landfills_gas_to_energy_df.to_csv(output_path, index=False)
    print(f"Saved active projects to {output_path}")
    return active_landfills_gas_to_energy_df

def parse_args():
    parser = argparse.ArgumentParser(
        description="Filter the EPA LMOP landfill gas-to-energy database to Atlanta MSA landfills and summarize project growth/emission reductions.")
    parser.add_argument(
        "xlsx_path",
        help="Path to the LMOP database Excel file (e.g. 'lmopdataga.xlsx')")
    return parser.parse_args()

def main():
    args = parse_args()
    landfills_gas_to_energy(args.xlsx_path)

if __name__ == "__main__":
    main()
