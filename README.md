# ehr-data-profiler

A Python Pandas toolkit to dynamically create a Jupyter Notebook for EHR data analysis that inlcudes a library of common functions using the Pandas library.

### Dynamically creating the notebook

Begin by opening a command line and navigate to the location of the repository with the 'base' Anaconda environment activated. All data must be in the folder 'Data' in the same directory and must conform to the structure and naming patterns of Data_Dictionary.json file.

When ready run the python command:

`(base) PS E:\ehr-data-profiler> python data_profiler.py`

## TEXT_SEARCH BY EXAMPLE

Another useful function included is 'text_search'. It is useful way to search specific columns in dataframes for text and return only those rows that contain the text.

**text_search( dataframe name, column name, text to search (regular expression), ignore case=(True by default, can set False), exclusion=(False by default, can set True), return_type=(‘df’ by default returns DataFrame, can set to ‘ids’ to get unique patient id list) )**

The ‘text_search’ function is also used in conjunction with the ‘filter_by_ids’ function to return data regarding a cross-section of the original data cohort.

**filter_by_ids( dataframe name to filter, ids array )**
