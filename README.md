# ehr-data-profiler

A Python Pandas toolkit to dynamically create a Jupyter Notebook for EHR data analysis that inlcudes a library of common functions using the Pandas library.

<hr />

## Dynamically creating the notebook

Begin by opening a command line and navigate to the location of the repository with the 'base' Anaconda environment activated. All data must be in the folder 'Data' in the same directory and must conform to the structure and naming patterns of Data_Dictionary.json file.

When ready run the python command:

`(base) PS E:\ehr-data-profiler> python data_profiler.py`

<hr />

## Function library

The notebook’s main library, ‘ehr_dp_lib.py’, is made up of a set of functions developed by our team that targets the main descriptive statistics that investigators typically need to begin understanding their data. The code blocks in the notebook are pre-generated to the match the different files and variables contained in your specific data set. The functions are as follows but rather than reviewing these in detail here you can proceed to try examples using your own data:

- describe_tables(): Returns a dataframe listing all the files in the ‘Data’ folder including row and column counts and descriptions
- missingness( dataframe name ): Returns a dataframe of the number of null values per column.
- occurrence_stats( dataframe name, unique id column ): [Generated on each table with a unique id that is not ‘IP_PATIENT_ID’] Returns a dataframe of counts for occurrences per table: Patients with Occurrence, Min, Max, Mean.
- catbar( dataframe name, column name, graph=(True or False)): [Generated on categorical data type only] Returns a dataframe of counts of all the groups of categories in the specific column in the dataframe. When graph argument set to True returns a bar graph.
- numstats( dataframe name, column name ): [Generated on number data type only] Returns a dataframe of descriptive statistics (ie. mean, max, min, median, quartiles) for the column data.
- dateline( dataframe name, column name ): [Generated on date data type only] Returns a line graph of the freuency of specific dates along an x-axis of time.
- flow_stats( flowsheet dataframe ): [Generated only if Flowsheet_Vitals.csv table in Data folder] Returns a dataframe of descriptive statistics for common vitals sign types (ie. Height, Weight, Temperature, Sp02, Pulse, BMI, Respirations).
- lab_stats( lab dataframe, top=(10 or greater) ): [Generated only if Labs.csv table in Data folder] Returns a dataframe of descriptive statistics for top lab procedures in dataset. The top argument can be adjusted to capture more lab procedures.
- text_search( dataframe name, column name, text to search, ignore case=(True by default can also be set to False), exclusion=(False by default), return_type=(‘df’ <default>, ‘ids’) ): Returns a dataframe based on a free text search of a specific column in an existing dataframe. Can also search by exclusion, and return an array of unique IP_PATIENT_ID s with set options.
- filter_by_ids( dataframe name,  ids array): [Used in conjuction with text_search and the return_type=’ids’ option ] Returns the dataframe in the first argument where the rows are filtered according to an array of IP_PATIENT_ID s produced by the text_search option.**


## TEXT_SEARCH BY EXAMPLE

Another useful function included is 'text_search'. It is useful way to search specific columns in dataframes for text and return only those rows that contain the text.

**text_search( dataframe name, column name, text to search (regular expression), ignore case=(True by default, can set False), exclusion=(False by default, can set True), return_type=(‘df’ by default returns DataFrame, can set to ‘ids’ to get unique patient id list) )**

The ‘text_search’ function is also used in conjunction with the ‘filter_by_ids’ function to return data regarding a cross-section of the original data cohort.

**filter_by_ids( dataframe name to filter, ids array )**
