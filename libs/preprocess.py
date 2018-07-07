import pandas as pd
import glob, os

import conf as CONF 

# To import table data of National Servey, skipping the second row because it overlaps the first row.
# https://www.e-stat.go.jp/gis/statmap-search?page=1&type=1&toukeiCode=00200521
current_dir = os.getcwd()
print(current_dir)
national_census_df = pd.read_csv('{0}tblT000847H3622.txt'.format(CONF.DIR_NATIONAL_CENSUS), skiprows=[1])
national_census_df.set_index('KEY_CODE', inplace=True)
print(national_census_df)
print(national_census_df.index.values)

#national_census_df['T000847001','T000847040','T000847041']

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
    
    mesh_df = pd.concat([mesh_df, department_store_df, supermarket_df, supermarket_grocery_df, convenience_store_df], axis=1)
    mesh_df.columns = ['KEY_CODE', 'department', 'supermarket', 'supermarket_grocery', 'convenience']
    mesh_df.set_index('KEY_CODE', inplace=True)
    return mesh_df

def check_if_it_is_a_food_desert(KEY_CODE, df):
    '''
    This method to check if the mesh of KEY_CODE has any store in the mesh and the neibough meshes.
    '''
    if df.loc[KEY_CODE, 'department'] == '-' and df.loc[KEY_CODE, 'supermarket'] == '-' and df.loc[KEY_CODE, 'supermarket_grocery'] == '-' and df.loc[KEY_CODE, 'convenience'] == '-':
        return True
    else:
        return False

def import_national_census_files():
    files = glob.glob(os.path.join(CONF.DIR_NATIONAL_CENSUS, '*.txt'))
    df_list = []
    for file in files:
        tmp_df = pd.read_csv(file,  encoding="SHIFT-JIS", skiprows=[1] )
        df_list.append(tmp_df)
    df = pd.concat(df_list)
    df.set_index('KEY_CODE', inplace=True)
    return df

def import_files_to_df(dir, encoding='utf8', skiprows=[], index=None):
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
        print(file)
        tmp_df = pd.read_csv(file,  encoding=encoding, skiprows=skiprows)
        df_list.append(tmp_df)
    df = pd.concat(df_list)
    if index:
        df.set_index(index, inplace=True)
    return df

print(import_national_census_files())
print(import_commercial_census_file())
mesh_df = import_commercial_census_file()
print(check_if_it_is_a_food_desert('684115032', mesh_df))
print(check_if_it_is_a_food_desert('684117501', mesh_df))


tmp = pd.read_csv('data/pref_meshcode/27.csv', encoding='SHIFT-JIS', skiprows=None)
tmp = pd.read_csv('data/pref_meshcode/28.csv', encoding='SHIFT-JIS', skiprows=None)

print(import_files_to_df(CONF.DIR_NATIONAL_CENSUS, encoding="SHIFT-JIS", skiprows=[1], index='KEY_CODE'))
print(import_files_to_df(CONF.DIR_PREF_MESHCODE, encoding='SHIFT-JIS', skiprows=[1]))