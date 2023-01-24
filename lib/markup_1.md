## The following cells in this notebook are auto-generated from the data in the 'Data' folder
## For each table a Pandas dataframe is created to connect to each table

### Below is a list of the EHR Data Profiler functions, arguments, and descriptions:

- **check_dups( *dataframe name* )**:  Checks duplicate rows in dataframe, if none found outputs 'No duplicates' otherwise it returns a dataframe of the duplicate rows.


- **missingness( *dataframe name* )**: Returns a dataframe of the number of null values per column.


- **catbar( *dataframe name, column name, graph=(True or False)*)**: \[Generated on *categorical* data type only\] Returns a dataframe of counts of all the groups of categories in the specific column in the dataframe. When `graph` argument set to `True` returns a bar graph.


- **numstats( *dataframe name, column name* )**: \[Generated on *number* data type only\] Returns a dataframe of descriptive statistics (ie. mean, max, min, median, quartiles) for the column data.


- **dateline( *dataframe name, column name* )**: \[Generated on *date* data type only\] Returns a line graph of the freuency of specific dates along an x-axis of time.


- **flow_stats( *flowsheet dataframe* )**: \[Generated only if Flowsheet_Vitals.csv table in Data folder\] Returns a dataframe of descriptive statistics for common vitals sign types (ie. Height, Weight, Temperature, Sp02, Pulse, BMI, Respirations).


- **lab_stats( *lab dataframe, top=(10 or greater)* )**: \[Generated only if Labs.csv table in Data folder\] Returns a dataframe of descriptive statistics for top lab procedures in dataset. The `top` argument can be adjusted to capture more lab procedures.