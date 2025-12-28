
import pandas as pd
from .csv_class import CSV


def count_sentences(name):

    
    boundaries = CSV(name).rows('boundary')

    count = 0
    for n in boundaries:
        try:
            if float(n) == 1 and str(n).strip() in ['1', '1.0']:
                count += 1
        except ValueError:
            continue 

    print(f'Number of Complete Sentences (count of 1 in "boundary"): {count}')


def clean_combined_indices(combined):
    """
    Removes rows from the DataFrame where the first 'index' column 
    contains any non-numeric characters.
    
    Parameters:
        combined (pd.DataFrame): The original DataFrame.
        
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Find the first column whose name includes 'index'
    index_column = next((col for col in combined.columns if 'index' in col.lower()), None)
    
    if index_column is None:
        raise ValueError("No column with 'index' found in DataFrame.")
    
    # Keep away rows where the index_column is NaN or entirely digits
    mask = ~(~combined[index_column].astype(str).str.replace('.', '', 1).str.isdigit() | combined[index_column].isna())

    combined_edited = combined[mask].reset_index(drop=True)
    return combined_edited


def calculate_disagreement(combined):

    # Get unique themes and names from the column headers
    themes = list({col.split(' ')[0] for col in combined.columns})
    names = list({col.split(' ')[1] for col in combined.columns})

    # Dictionary to store percentage of disagreements for each theme
    percentage_of_disagreements = {}

    for theme in themes:
        
        # Extract the two relevant columns for comparison 
        # ATTENTION: Get rid of clean_combined_indices if you want to include words added.
        col1 = [x for x in clean_combined_indices(CSV(names[0]).full_file())[theme] if not pd.isna(x)]
        col2 = [x for x in clean_combined_indices(CSV(names[1]).full_file())[theme] if not pd.isna(x)]
        
        cases_sum = max(len(col1), len(col2)) # Total number of cases. 
      

        num = 0
        for first_person, second_person in zip(col1, col2):
            
            if first_person != second_person:
                num = num + 1
                
                # Calculate percentage of disagreement over total rows
                percentage_of_disagreements[theme] = [round((num / cases_sum) * 100, 3) , f'{num} out of {cases_sum}']
            
        if theme not in list(percentage_of_disagreements.keys()):
            percentage_of_disagreements[theme] = [0, f'0 out of {cases_sum}']
    
    return percentage_of_disagreements



def statistics(combined):
        
    disagreement_stats = calculate_disagreement(combined)

    for theme, stat in disagreement_stats.items():
        
        print(f"\nDisagreement for {theme}: {stat[0]}% ({stat[1]}).")

