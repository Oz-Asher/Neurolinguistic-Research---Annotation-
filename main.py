#main.py: Entry point for the project

import os

from src.mismatches import mismatches
from src.excel_editing import excel_editing
from src.statistics import statistics, count_sentences
from src.search_unit import search


# Get the directory of main.py
directory = os.path.dirname(os.path.abspath(__file__))


csv_names = ['Oz', 'Shaked']


# combined = mismatches(csv_names) 

# excel_editing(combined, directory)

# statistics(combined)

# search('Final')

count_sentences('Oz') # Prints the number of sentences for a scpecific CSV file.









