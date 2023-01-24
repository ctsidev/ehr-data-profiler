import pandas as pd
import matplotlib.pyplot as plt
import re

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
        return df

def numstats(df, col):
    return df[col].describe().reset_index().rename(columns={'index': 'STAT_TYPE'})

def missingness(df):
    df = df.isna().sum().reset_index()
    df.columns = ['COLUMN','NULLS']
    return df

def text_search(df, col, search, ignore_case=True):
    if ignore_case:
        return df[df[col].str.contains(search, flags=re.I) == True]
    else:
        return df[df[col].str.contains(search) == True]

def check_dups(df):
    if len(df[df.duplicated()]):
        return df[df.duplicated()]
    else:
        return 'No duplicates'

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