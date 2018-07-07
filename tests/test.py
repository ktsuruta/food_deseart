import pandas as pd
import unittest

import sys, os
sys.path.insert(0, os.getcwd())
import libs.preprocess as preprocess

class TestImportData(unittest.TestCase):
    '''
    This class check data load
    '''

    def setUp(self):
       self.national_census_df = preprocess.national_census_df
        self.mesh_df = preprocess.mesh_df

    def test_load_national_survey(self):
        # At first, we import the records of national survey.
        self.assertEquals(type(self.national_survey_df), pd.DataFrame)
        # Then, we found that the first and second row are the header information.
        # We need to set the first row as header information and skip the second row.

    def test_check_if_a_mesh_is_food_hazard(self):
        self.assertEqual(preprocess.check_if_it_is_a_food_desert('684201122', self.mesh_df), False)
        self.assertEqual(preprocess.check_if_it_is_a_food_desert('684201212', self.mesh_df), True)        

    def test_senario(self):
        # Import all the national survey files to a dataframe. The files are stored in a specific directory.
        # https://www.e-stat.go.jp/gis/statmap-search?page=1&type=1&toukeiCode=00200521
        national_census = preprocess.import_national_census_files() 

        # Import the commercial statistics file to a dataframe.
        # To compare the number of records of the above dataframes.
        commercial_census = preprocess.import_commercial_census_file()

        # To add the column of prefecture to "national_census_df". 
        # We use the data of Mesh Code List by city, town, and area.
        # http://www.stat.go.jp/data/mesh/m_itiran.html

        # To add the columns of estimated number of population who are not able to drive.
        # We use the data of the study below.

        # To add the column of FOOD_DESERT_FLAG to national_survey_df.
        # We check if a mesh area has any grocery store or not by seeing the same area and 9 neibough areas.


        # To convert the mesh codes of food desert areas to zipcode using Google API


        # To check if any co-op serve home delivery service in food deserts searching by zipcode in Takuhai Portal.
        pass

if __name__ == '__main__':
    unittest.main()


