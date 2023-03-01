import os
import nbformat as nbf
import json
import string
from nbformat.v4.nbbase import (
    new_code_cell, new_markdown_cell, new_notebook,
    new_output, new_raw_cell
)

data_dictionary = json.load(open('data_dictionary.json'))
data_files = os.listdir('./Data')

cells = []

first_cells = """# EHR Data Profiler

Documentation of the functions available in the library as well as an in-depth tutorial on the use of `text_search` can be found on the project's GitHub page:
<a href="https://github.com/ctsidev/ehr-data-profiler#function-library">https://github.com/ctsidev/ehr-data-profiler#function-library</a>

### Run the next cell to make all the imports, which include Pandas and the EHR data anaylsis functions:
"""

cells.append(new_markdown_cell(source=first_cells))
cells.append(new_code_cell(source="import pandas as pd\nimport matplotlib.pyplot as plt\nfrom lib.ehr_dp_lib import *\npd.set_option('display.max_colwidth', None)\npd.set_option('display.max_rows', 500)"))

cells.append(new_markdown_cell(source='### Run the following block to describe the tables in your Data folder:'))
cells.append(new_code_cell(source='describe_tables()'))

for table in data_dictionary:
    csv_file = string.capwords(table['element'].replace('_', ' ')).replace(' ', '_') + '.csv'
    if csv_file in data_files:
        cells.append(new_markdown_cell(source=f"### {table['element']}"))
        table_df = f"{table['element'].lower()}_df"
        cells.append(new_code_cell(source=f"{table_df} = pd.read_csv('Data/{csv_file}')\n{table_df}"))
        cells.append(new_code_cell(source=f"missingness({table_df})"))
        
        if table['unique_id'] != 'IP_PATIENT_ID':
            cells.append(new_code_cell(source=f"occurrence_stats({table_df}, '{table['unique_id']}')"))
        elif table_df == 'patient_demographics_df':
            cells.append(new_code_cell(source="table_1(patient_demographics_df)"))

        if table['date_field']:
            cells.append(new_code_cell(source=f"dateline({table_df}, '{table['date_field']}')"))

        f = open('Data/' + csv_file, encoding='utf-8')
        fields = [field.replace('"','').strip() for field in f.readline().split(',')]
        for nb_field in [f for f in table['fields'] if f['nb_func']]:
            if nb_field['field_name'] in fields:
                if nb_field['nb_func'] == 'catbar':
                    cells.append(new_code_cell(source=f"{nb_field['nb_func']}({table_df}, \'{nb_field['field_name']}\', graph=False) ## Set graph=True for Bar graph"))
                else:
                    cells.append(new_code_cell(source=f"{nb_field['nb_func']}({table_df}, \'{nb_field['field_name']}\')"))

        if table_df == 'flowsheet_vitals_df':
            cells.append(new_code_cell(source=f"flow_stats({table_df})"))
        elif table_df == 'labs_df':
            cells.append(new_code_cell(source=f"lab_stats({table_df}, top=10)"))

nb = new_notebook(cells=cells, metadata={ 'language' : 'python' })
nbf.write(nb, open('Data_Profiler.ipynb', 'w', encoding='utf-8'), 4)

