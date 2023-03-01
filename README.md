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

- **describe_tables()**: Returns a dataframe listing all the files in the ‘Data’ folder including row and column counts and descriptions
- **missingness( dataframe name )**: Returns a dataframe of the number of null values per column.
- **occurrence_stats( dataframe name, unique id column )**: [Generated on each table with a unique id that is not ‘IP_PATIENT_ID’] Returns a dataframe of counts for occurrences per table: Patients with Occurrence, Min, Max, Mean.
- **catbar( dataframe name, column name, graph=(True or False))**: [Generated on categorical data type only] Returns a dataframe of counts of all the groups of categories in the specific column in the dataframe. When graph argument set to True returns a bar graph.
- **numstats( dataframe name, column name )**: [Generated on number data type only] Returns a dataframe of descriptive statistics (ie. mean, max, min, median, quartiles) for the column data.
- **dateline( dataframe name, column name )**: [Generated on date data type only] Returns a line graph of the freuency of specific dates along an x-axis of time.
- **flow_stats( flowsheet dataframe )**: [Generated only if Flowsheet_Vitals.csv table in Data folder] Returns a dataframe of descriptive statistics for common vitals sign types (ie. Height, Weight, Temperature, Sp02, Pulse, BMI, Respirations).
- **lab_stats( lab dataframe, top=(10 or greater) )**: [Generated only if Labs.csv table in Data folder] Returns a dataframe of descriptive statistics for top lab procedures in dataset. The top argument can be adjusted to capture more lab procedures.
- **text_search( dataframe name, column name, text to search, ignore case=(True by default can also be set to False), exclusion=(False by default), return_type=(‘df’ <default>, ‘ids’) )**: Returns a dataframe based on a free text search of a specific column in an existing dataframe. Can also search by exclusion, and return an array of unique IP_PATIENT_ID s with set options.
- **filter_by_ids( dataframe name,  ids array)**: [Used in conjuction with text_search and the return_type=’ids’ option ] Returns the dataframe in the first argument where the rows are filtered according to an array of IP_PATIENT_ID s produced by the text_search option.**

<hr />

## TEXT_SEARCH tutorial

Another useful function included is `text_search`. It is useful way to search specific columns in dataframes for text and return only those rows that contain the text. The `text_search` function is also used in conjunction with the `filter_by_ids` function to return data regarding a cross-section of the original data cohort.
  
Here are some practical examples:

### 1. Getting the 'Female' patients from the Patient Demographics dataframe
  
![Screenshot 2023-03-01 102502](https://user-images.githubusercontent.com/44505663/222229616-7abaa6b8-7394-4e6c-8df0-7824c1dd1702.png)
  
We can use `text_search` to filter those patients with 'female' in the column 'SEX'. Note, the search is not case sensitive, if you require it to be case sensitive you can set the optional argument `ignore_case=False`

`text_search(patient_demographics_df, 'SEX', 'female')`

or with case sensitivity:

`text_search(patient_demographics_df, 'SEX', 'Female', ignore_case=False)`
  
![Screenshot 2023-03-01 102337](https://user-images.githubusercontent.com/44505663/222228992-5d10fa03-2889-49c4-8c42-edb187a65f3a.png)
  
### 2. Getting the 'Female' patients that are also 'Spanish' speakers

In some cases we need to combine searchs to filter a even more specific group, such as 'Female Spanish speakers'. To do this you will need to use the search twice on 2 lines, saving the first search in a variable that is then used in the next search:

```
female_pats = text_search(patient_demographics_df, 'SEX', 'female')
female_spanish_pats = text_search(female_pats, 'LANGUAGE', 'spanish')
female_spanish_pats
```

![Screenshot 2023-03-01 103701](https://user-images.githubusercontent.com/44505663/222233830-6379fa20-11e8-4486-9411-a702e8a270b9.png)


### 3. Using this new 'Female spanish patient' cohort to filter other tables

We can use the `return_type` option in `text_search` to get the unique ids of the cohort by setting the `return_type='ids'`

```
female_pats = text_search(patient_demographics_df, 'SEX', 'female')
female_spanish_pat_ids = text_search(female_pats, 'LANGUAGE', 'spanish', return_type='ids')
female_spanish_pat_ids
```
  
![Screenshot 2023-03-01 104409](https://user-images.githubusercontent.com/44505663/222235218-b6fe4274-29e3-4742-8fea-e4ca5c7b7f6f.png)

We can now take this variable `female_spanish_pat_ids` to then plug into the fnction `filter_by_ids` to get the Procedures for that cohort:
  
```
filter_by_ids(procedures_df, female_spanish_pat_ids)
```

You will now have a DataFrame of Procedures just for the cohort of 'Female Spanish speakers':
  
![Screenshot 2023-03-01 105004](https://user-images.githubusercontent.com/44505663/222236594-b37ab5ed-9538-4613-8212-cf62624d30da.png)

### 4. Using new dataset from our filtered cohort to get a summary of the counts of Procedures
  
You can now use the result of the `filter_by_ids(procedures_df, female_spanish_pat_ids)` to get a breakdown of the Procedures using another function in the library `catbar`. Feed the result of the filter into a new variable:
  
```
female_spanish_procs = filter_by_ids(procedures_df, female_spanish_pat_ids)
catbar(female_spanish_procs, 'PROCEDURE_DESCRIPTION') 
```

![Screenshot 2023-03-01 105953](https://user-images.githubusercontent.com/44505663/222238273-2c05396f-5418-4a89-b08c-696df6715d3a.png)
 
### 5. Exclusions using `text_search`
  
The exclusion option in text search can be made as well. Assume we want to find anyone in our Patient Demographics table that **does not** have 'Unknown' as their language. Using the `text_search` with `exclusion=True` we can create a new variable to then plug into `catbar`

```
language_known_pats = text_search(patient_demographics_df, 'LANGUAGE', 'unknown', exclusion=True)
catbar(language_known_pats, 'LANGUAGE')
```

The before and after:
  
![Screenshot 2023-03-01 110913](https://user-images.githubusercontent.com/44505663/222240198-9dc2c6dd-be7b-48a5-b0fb-809d4ad4f75f.png)

