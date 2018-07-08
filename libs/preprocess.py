import codecs,glob, os
import pandas as pd
import libs.conf as CONF

def import_commercial_census_file():

    # To import table data of Commercial Statistics
    # the data format follows http://www.meti.go.jp/statistics/tyo/syougyo/mesh/download.html#500m
    header = [str(x) for x in range(1,97)]
    file_path = CONF.DIR_COMMERCIAL_CEUNSUS + 'H26_03_500mNationwide.csv'
    commercial_census_df = pd.read_csv(file_path, header=None, \
                           dtype={0:str, 1:str, 2:str, 3:str, 4:str, 5:str, 6:str,  7:str, 8:str})
    commercial_census_df.columns = header
    
    # To add columns.
    # To combine the columns of mesh values.
    mesh_df = commercial_census_df['5'].astype(str) + commercial_census_df['6'].astype(str) \
              + commercial_census_df['7'].astype(str) + commercial_census_df['8'].astype(str)
    department_store_df = commercial_census_df['64']
    supermarket_df = commercial_census_df['67']
    supermarket_grocery_df = commercial_census_df['70']
    convenience_store_df = commercial_census_df['73']
    
    mesh_df = pd.concat([mesh_df, department_store_df, supermarket_df, supermarket_grocery_df, \
              convenience_store_df], axis=1)
    mesh_df.columns = ['KEY_CODE', 'department', 'supermarket', 'supermarket_grocery', 'convenience']
    mesh_df.set_index('KEY_CODE', inplace=True)
    return mesh_df

def check_if_it_is_a_food_desert(KEY_CODE, df):
    '''
    This method to check if the mesh of KEY_CODE has any store in the mesh and the neibough meshes.
    '''
    if df.loc[KEY_CODE, 'department'] == '-' and df.loc[KEY_CODE, 'supermarket'] == '-' and \
       df.loc[KEY_CODE, 'supermarket_grocery'] == '-' and df.loc[KEY_CODE, 'convenience'] == '-':
        return True
    else:
        return False

def import_files_to_df(dir, encoding='utf8', skiprows=[], index=None, dtype={}):
    '''
    params: 
        dir(str): Directory of the files to import.
        encoding(str): The encode of the files such as SHIFT-JIS, utf8
        skiprows(list): The rows to skip when importing.
        index(str) : The name to set as index
    return: pandas dataframe
    '''

    files = glob.glob(os.path.join(dir, '*'))
    df_list = []
    for file in files:
        try:
            tmp_df = pd.read_csv(file,  encoding=encoding, skiprows=skiprows, dtype=dtype)
            df_list.append(tmp_df)
        except:
            with codecs.open(file, "r", "SHIFT-JIS", "ignore") as file:
                tmp_df = pd.read_table(file, delimiter=",")
                df_list.append(tmp_df)
    df = pd.concat(df_list, sort=True)
    if index:
        df.set_index(index, inplace=True)
    return df

def import_the_metrics_of_cities_and_prefs():
    df = pd.read_csv('{0}FEA_hyoujun-20180707233259.csv'.format(CONF.DIR_METRICS_OF_CITIES_AND_PREFS), \
         skiprows=[1], encoding="SHIFT-JIS", dtype={'標準地域コード':str})
    df.rename(inplace=True, columns={"標準地域コード":"都道府県市区町村コード"})
    return df

def merge_mesh_code_and_the_metrics_of_pref(pref_meshcode, metrics_of_cities_and_prefs):
    return prpref_meshcode.merge(metrics_of_cities_and_prefs , on='都道府県市区町村コード')