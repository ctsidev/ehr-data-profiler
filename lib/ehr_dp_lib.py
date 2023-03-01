import pandas as pd
import matplotlib.pyplot as plt
import re
import os
import json

data_dictionary = json.load(open('lib/data_dictionary.json'))

def describe_tables():
    data = []
    for f in os.listdir('Data'):
        table = {}
        table['TABLE'] = f
        df = pd.read_csv(f'Data/{f}')
        table['ROW_COUNT'] = len(df)
        table['COLUMN_COUNT'] = len(df.columns)
        desc = ''
        for row in data_dictionary:
            if row['element'] == f.split('.')[0].upper():
                desc = row['description']
        table['DESCRIPTION'] = desc
        data.append(table)
    
    return pd.DataFrame(data)

def occurrence_stats(occur_df, unique_id):
    pats_w_occur = len(occur_df.groupby(['IP_PATIENT_ID']))
#     pats_wo_occur = len(pat_df) - len(occur_df.groupby(['IP_PATIENT_ID']))
    occur_min = occur_df.groupby('IP_PATIENT_ID').count()[unique_id].min()
    occur_max = occur_df.groupby('IP_PATIENT_ID').count()[unique_id].max()
    occur_mean = occur_df.groupby('IP_PATIENT_ID').count()[unique_id].mean()
    data = [{
        'Patients w/ Occurrence': pats_w_occur,
        'Occurrence Min': occur_min,
        'Occurrence Max': occur_max,
        'Occurrence Mean': occur_mean
    }]
    return pd.DataFrame(data)

def table_1(pat_df, t1_groups=['AGE','RACE','ETHNICITY','LANGUAGE','EDUCATION','INCOME']):
    output = ''

    for grp in t1_groups:
        if grp not in pat_df.columns:
            continue

        grp_df = pat_df
        if grp == 'AGE':
            grp_df['a_grp'] = ''
            grp_df.loc[grp_df['AGE'] < 18, 'a_grp'] = '<18'
            grp_df.loc[(grp_df['AGE'] >= 18) & (grp_df['AGE'] < 25), 'a_grp'] = '18-24'
            grp_df.loc[(grp_df['AGE'] >= 25) & (grp_df['AGE'] < 35), 'a_grp'] = '25-34'
            grp_df.loc[(grp_df['AGE'] >= 35) & (grp_df['AGE'] < 45), 'a_grp'] = '35-44'
            grp_df.loc[(grp_df['AGE'] >= 45) & (grp_df['AGE'] < 55), 'a_grp'] = '45-54'
            grp_df.loc[(grp_df['AGE'] >= 55) & (grp_df['AGE'] < 65), 'a_grp'] = '55-64'
            grp_df.loc[(grp_df['AGE'] >= 65), 'a_grp'] = '65+'
            grp_df.loc[(grp_df['AGE'].isna()), 'a_grp'] = 'Unknown'
            
            grp_df = ((grp_df['a_grp'].value_counts() / grp_df['a_grp'].value_counts().sum()) * 100).reset_index()
        else:
            grp_df = ((grp_df[grp].value_counts() / grp_df[grp].value_counts().sum()) * 100).reset_index()
            
        output += f'\n{grp}\n-----------------\n'
        for i, row in grp_df.iterrows():
            output += f'{row[0]} => {round(row[1], 1)}\n'
                
    print(output)

def dateline(df, date_col):
    date_series = pd.to_datetime(df[date_col])
    date_counts = date_series.value_counts()
    date_counts.plot(figsize=(20, 6))
    plt.title(f"{date_col} over time Line Graph")
    plt.xlabel('Time')
    plt.ylabel(f'Occurences of {date_col}')
    plt.ylim(0 if date_counts.min() == 0 else date_counts.min() - (date_counts.max() * .05), 
        date_counts.max() + (date_counts.max() * .05))

def catbar(df, col, graph=False):
    if graph:
        cat_series = df.groupby(col).count().iloc[:, 0]
        cat_series.plot(kind='bar', figsize=(20, 6))
        plt.title(f"{col} Categories Bar Chart")
        plt.xlabel(f'{col} Category')
        plt.ylabel(f'Occurences of Category')
        plt.ylim(0 if cat_series.min() else cat_series.min() - (cat_series.max() * .05),
            cat_series.max() + (cat_series.max() * .05))
    else:
        df = df[col].value_counts().reset_index()
        df.columns = [col, 'COUNT']
        df['PERCENT'] = (df['COUNT'] / df['COUNT'].sum()) * 100
        return df

def numstats(df, col):
    return df[col].describe().reset_index().rename(columns={'index': 'STAT_TYPE'})

def missingness(df):
    total = len(df)
    df = df.isna().sum().reset_index()
    df.columns = ['COLUMN','NULLS']
    df['PERCENT'] = (df['NULLS'] / total) * 100
    return df

def text_search(df, col, search, ignore_case=True, exclusion=False, return_type='df'):
    if ignore_case:
        if exclusion:
            df = df[~df[col].str.contains(search, flags=re.I)]
        else:
            df = df[df[col].str.contains(search, flags=re.I)]
    else:
        if exclusion:
            df = df[~df[col].str.contains(search)]
        else:
            df = df[df[col].str.contains(search)]
    
    if return_type == 'df':
        return df
    elif return_type == 'ids':
        return df['IP_PATIENT_ID'].unique()

def filter_by_ids(df, ids):
    return df[df['IP_PATIENT_ID'].isin(ids)]

def flow_stats(df):
    df_list = []
    for vs_type in df['VITAL_SIGN_TYPE'].unique():
        try:
            type_ser = df[df['VITAL_SIGN_TYPE'] == vs_type]['VITAL_SIGN_VALUE'].astype('float').describe()
            ser_dict = {'VITAL_SIGN_TYPE': vs_type}
            for k, v in type_ser.items():
                ser_dict[k.upper()] = round(v, 2)
            
            df_list.append(ser_dict)
        except:
            pass

    return pd.DataFrame(df_list)

def lab_stats(df, top):
    df = df[df['RESULT'].notnull()]
    df = df[df['RESULT'].str.isnumeric()]
    top = df['COMPONENT_NAME'].value_counts().head(top).index
    
    df_list = []
    for l_type in top:
        type_ser = df[df['COMPONENT_NAME'] == l_type]['RESULT'].astype('float').describe()
        ser_dict = {'COMPONENT_NAME': l_type}
        for k, v in type_ser.items():
            ser_dict[k.upper()] = round(v, 2)
            
        df_list.append(ser_dict)
    return pd.DataFrame(df_list)