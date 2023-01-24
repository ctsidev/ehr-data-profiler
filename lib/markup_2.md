## Using TEXT_SEARCH

### Another useful function included is 'text_search'. It is useful way to search specific columns in dataframes for text and return only those rows that contain the text.

- **text_search( *dataframe name, column name, text to search, ignore case=(True by default can also be set to False)* )**


### Example:
If you wanted to search Patient Demographics data for patients whose 'ETHNICITY' contains the text 'latino' using text_search:
`text_search(patient_demographics_df, 'ETHNICITY', 'latino')`

Result:
![latino_search.PNG](lib/latino_search.PNG)


## Combining TEXT_SEARCH with other functions:
### You can also combine functions to get the a specific analytical calculation. 

### Example:
If you wanted to get a set of counts of the categories in `SEX` of the patients (ie. Male, Female) in the previous dataset of 'latino'. First, you would need to assign the result of the `text_search` to a new value, in this case `latino_pats`:

`latino_pats = text_search(patient_demographics_df, 'ETHNICITY', 'latino')
catbar(latino_pats, 'SEX', graph='True')`

Result:
![latino_gender_search.PNG](lib/latino_gender_search.PNG)
