
import pandas as pd
from itertools import zip_longest
from collections import defaultdict
from .csv_class import CSV

#This code creates a table of the mismatches so it would be easy to use later in the code

def mismatches(csv_names):

    # Load all CSVs at once into CSV objects
    csv_objects = {name: CSV(name) for name in csv_names}

    # Find the CSV with the maximum number of rows in the 'index' column (for alignment)
    max_index_name = max(csv_names, key=lambda name: len(csv_objects[name].rows('index')))
    max_index_csv = csv_objects[max_index_name]
    
    mismatched_list = []  # List to store DataFrames of mismatched values between CSVs

    # Loop over all CSVs and compare each one with the CSV having the maximum 'index' rows
    for name in csv_names:
        
        # Skip comparison with the CSV that has the maximum index rows
        if name != max_index_name:
            base_csv = max_index_csv
            compared_csv = csv_objects[name]

            # Iterate through each column of the CSV
            for column in CSV(name).columns():
                base_rows = base_csv.rows(column)
                compared_rows = compared_csv.rows(column)

                # Skip columns with 'Unnamed' in their name or if any value in the column is None
                if all(x is not None for x in base_rows) and all(x is not None for x in compared_rows) and 'Unnamed' not in column and column != 'glossary':
                    
                    # Special handling for 'index' column
                    if column == 'index':
                        i = 0
                        while i < max(len(base_rows), len(compared_rows)):
                            val_base = base_rows[i] if i < len(base_rows) else None
                            val_compared = compared_rows[i] if i < len(compared_rows) else None

                            if val_base != val_compared:
                                if val_base not in compared_rows[i:]:
                                    compared_csv.insert_none_at(i)
                                    compared_rows.insert(i, None)
                                elif val_compared not in base_rows[i:]:
                                    base_csv.insert_none_at(i)
                                    base_rows.insert(i, None)
                            i += 1

                    # Create a dictionary to store mismatch records
                    mismatch_records = defaultdict(dict)

                    # Compare values between the two CSVs and store mismatches
                    for i, (base_object, compared_object) in enumerate(zip_longest(base_rows, compared_rows)):
                        try:
                            base_object = float(base_object)
                            compared_object = float(compared_object)
                        except (ValueError, TypeError):
                            pass

                        # Always log 'index' and 'word' columns, even if the values are equal
                        if column == 'index' or column == 'word':
                            mismatch_records[i][f"{column} {max_index_name}"] = base_object
                            mismatch_records[i][f"{column} {name}"] = compared_object

                            if base_object != compared_object:
                                
                                mismatch_records[i][f"{column} {max_index_name}"] = str(base_object) + '@M'
                                mismatch_records[i][f"{column} {name}"] = str(compared_object) + '@M'

                        elif base_object != compared_object:
                            # Log mismatches for non-'index' non-'word' columns
                            mismatch_records[i][f"{column} {max_index_name}"] = base_object
                            mismatch_records[i][f"{column} {name}"] = compared_object

                    # After comparisons, convert mismatch records into a DataFrame
                    mismatch_df = pd.DataFrame.from_dict(mismatch_records, orient="index")
                    mismatched_list.append(mismatch_df)


        # === Combine and Clean Up Results ===
    combined = (
        pd.concat(mismatched_list, axis=1)  # Concatenate the mismatched DataFrames
        .reset_index()  # Reset the index to ensure proper sorting
        .sort_values('index')  # Sort by 'index' column (or the first column in the DataFrame)
        .groupby('index', as_index=False)  # Group by 'index' and keep the first entry for each group
        .first()
        .drop(columns='index')  # Drop the 'index' column from the final result
    )


    return combined



