import pandas as pd

def dropping_column(df:pd.DataFrame, col:str)-> pd.DataFrame:
    '''
    dropping the selected column
    df = DataFrame
    col = column to drop
    '''
    df = df.drop(col,axis = 1) 
    return df

def replace_column_lower(df:pd.DataFrame, replace:str, replaced_by:str)-> pd.DataFrame:
    '''
    replaceing in every column the variable "replace" with the var "replaced_by" and lower the letters.
    
    '''
    col_rename = []

    for col in df.columns:
        col_rename.append(col.lower().replace(replace,replaced_by))
    
    df.columns = col_rename      
    return df
    
def column_rename(df:pd.DataFrame, column_name:str, replaced_by:str)-> pd.DataFrame:    
    '''
    replacing the column name 
    '''
    df = df.rename(columns={column_name:replaced_by})
    return df

def drop_nan_value_rows(df:pd.DataFrame) -> pd.DataFrame:
    '''
    Dropping Rows if there are fully empty.
    ''' 
    df = df.dropna(how='all')
    return df

def drop_global_duplicated(df:pd.DataFrame, col:str)-> pd.DataFrame:
    '''
    searching for dupliccateds in any columns and keep only the first occurrence of each duplicated row 
    '''
    df = df.drop_duplicates(subset=col)
    return df

def replace(df:pd.DataFrame, col:str, replace:str, replaced_by:str)-> pd.DataFrame:
    '''
    replace a string for another string
    ''' 
    if df[col].dtype == 'O':
        df[col] = df[col].str.replace(replace,replaced_by)
        return df

def drop_null(df:pd.DataFrame, col:str)-> pd.DataFrame:    
    '''
    dropping theses rows with the value = 0
    '''
    df2 = df.copy()
    df2 = df2.drop(df2[df2[col]== 0].index,axis=0)
    return df2
    
def fillna(df:pd.DataFrame, col:str, fill:str)->pd.DataFrame:
    '''
    Fill all the NaNs of one column with the median of that column
    '''
    if fill == 'median':
        clv_mean = df[col].median()
        df[col] = df[col].fillna(clv_mean)
        return df
    if fill == 'mode':
        clv_mode = df[col].mode()[0]
        df[col] = df[col].fillna(clv_mode)
        return df
    else:
        df[col] = df[col].fillna(fill)
        return df

def chance_datatype(df:pd.DataFrame, col:str, d_type:type) -> pd.DataFrame:
    '''
    chancing the datatype of a column 
    '''
    if df[col].dtype is not d_type:
        df[col] = df[col].astype(d_type)
        return df
    
def chance_object_to_datetime(df:pd.DataFrame, col:str) -> pd.DataFrame:
    '''
    chancing the type of a object column to datetime and the invalid vallues will be set as NaT.
    '''
    if df[col].dtype == 'O':
        df[col] = pd.to_datetime(df[col], errors='coerce')
        return df
    else:
        pass

def split(df: pd.DataFrame, symbol:str, col:str)-> pd.DataFrame:
    '''
    split a string by specific symbol and indexing which split should return
    ''' 

    df2 = df.copy()
    if df[col].dtype == 'O':
        if col not in df2.columns:
            return df2
        else:
            df2[col] = df2[col].apply(lambda x: x.split(symbol)[1] )
            
            return df2

def clean_gender_column(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function will take a Pandas DataFrame as an input and it will replace the values in
    the "gender" column ins such a way that any gender which is not Male or Female with be 
    replaced by "U" otherwise the genders will be either "F" or "M"

    Inputs:
    df: Pandas DataFrame

    Outputs:
    A pandas DataFrame with the values in the "gender" column cleaned.
    '''

    df2 = df.copy()

    if "gender" not in df2.columns:
        return df2
    else:
        #df2['gender'] = df2['gender'].apply(lambda x: x[0].upper() if x[0].upper() in ['M', 'F'] else "U")
        df2['gender'] = list(map(lambda x: x[0].upper() if x[0].upper() in ['M', 'F'] else "U", df2['gender']))
        return df2

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    '''
    set all columns to lowercase letters and replace spaces with underscore.
    Rename the column 'st'
    '''
    df = replace_column_lower(df," ","_")
    df = column_rename(df,'st','state')
    return df

def data_clean(df: pd.DataFrame) -> pd.DataFrame:
    '''
    start all cleaning functions
    '''
    df = drop_nan_value_rows(df)   
    df = drop_global_duplicated(df,'customer')
    df = replace(df,'education','Bachelors','Bachelor')
    df = replace(df,'state','AZ','Arizona')
    df = replace(df,'state','Cali','California')
    df = replace(df,'state','WA','Washington')
    df = replace(df,'vehicle_class','Sports Car','Luxury')
    df = replace(df,'vehicle_class','Luxury SUV','Luxury')
    df = replace(df,'vehicle_class','Luxury Car','Luxury')
    df = replace(df,'customer_lifetime_value','%','')
    df = chance_datatype(df,'customer_lifetime_value',float)
    df = fillna(df,'customer_lifetime_value','median')
    df = fillna(df,'gender','U')
    df = clean_gender_column(df)
    df = split(df,'/','number_of_open_complaints')
    df = chance_datatype(df,'number_of_open_complaints',int)
    df = chance_datatype(df,'income',int)
    df = chance_datatype(df,'customer_lifetime_value',int)
    df = chance_datatype(df,'monthly_premium_auto',int)
    df = chance_datatype(df,'total_claim_amount',int)
    return df
