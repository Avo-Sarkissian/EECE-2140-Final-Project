import unittest
import os
import Final_testing

# Imports the classes and functions from your script to the test file
from Final_testing import AgeGenderAnalyzer, HealthProjectionAnalyzer, generate_box_plots, read_filtered_data, get_valid_input

class TestHealthAnalyzer(unittest.TestCase):
    def setUp(self):
        # Creates a temporary test file
        self.test_file = 'test_health_data.csv'
        with open(self.test_file, 'w', newline='') as csvfile:
            pass


    def test_age_category(self):
        # Tests the get_age_category method to make sure that the code properly categories this 25 year old in the 18-29 age category
        user = AgeGenderAnalyzer('M', 25, 70, 8000)
        self.assertEqual(user.get_age_category(), '18-29')


    def test_analyze_health_and_read_filtered_data(self):
        # Tests the analyze_health method and read_filtered_data function to make sure that the system is correctly processing the data, writing to the csv file, and then reading and filtering the necessary csv data.
    
        user = AgeGenderAnalyzer('F', 45, 60, 10000)
        user_category = user.analyze_health()


        # checks to see if the data is written to the the csv file
        with open('health_data.csv', 'r') as csvfile:
            data = csvfile.readlines()
            self.assertIn(f'F,{user_category},60,10000\n', data)

        # Checks to make sure that read_filtered_data retrieves the correct data from the csv file
        steps, heart_rate = read_filtered_data('F', user_category)
        self.assertEqual(steps, [10000])
        self.assertEqual(heart_rate, [60])

    def test_generate_box_plots(self):
        # Tests the generate_box_plots function to unsure that the program is generating accurate box plots based on the data in the test.
        # A user can also visually verify this
        step_data = [[8000, 9000, 10000], [7000, 8000, 9000]]
        heart_rate_data = [[70, 75, 80], [65, 70, 75]]
        generate_box_plots(step_data, heart_rate_data, user_step_value=9500, user_heart_rate_value=75, title='Test')

        

    def test_get_valid_input(self):
        # Tests the get_valid_input function to make sure that invalid inputs dont break the program and valid inputs remain.
        # Mocks the situation in which the user inputs 25 has their age
        with unittest.mock.patch('builtins.input', side_effect=['25']):
            age = get_valid_input("Enter your age: ", min_value=0, max_value=120)
            self.assertEqual(age, 25)
        # Mocks the situation where a user inputs abc, then 30. This will test that the code rejects abc and then accepts the second input of 30.
        with unittest.mock.patch('builtins.input', side_effect=['abc', '30']):
            age = get_valid_input("Enter your age: ", min_value=0, max_value=120)
            self.assertEqual(age, 30)

if __name__ == Final_testing:
    unittest.main()
