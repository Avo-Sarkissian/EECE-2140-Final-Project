#mports csv file and matlab plot so that the data can be graphed
import csv
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np


print("\nWelcome to Healthbot. Healthbot is a computer program to help users be more aware of where they \nstand healthwise in comparison to others in their age group and gender.\n\nHealthbot will also use the information you submit to help predict what your\nresting heart rate and average steps will be as you age. \n")

# Base class for health analysis and sets variables
# I chose to set the HealthAnalyzer as a parent class so that the two other class can call the variables from here. Then the Age GenderAnalyzer can send the inputted variables from the user to this parent class where it can later be called be the HealthProjection Analyzer
class HealthAnalyzer:
    def __init__(self, gender, age, resting_heart_rate, average_steps):
        self.gender = gender
        self.age = age
        self.resting_heart_rate = resting_heart_rate
        self.average_steps = average_steps


    # Makes sure all subclasses define how they analyze data to ensure consistency throughout the program
    def analyze_health(self):
        raise NotImplementedError("Subclasses must implement analyze_health method")


# this subclass is for age and gender to differentiate the catagories when comparing data
class AgeGenderAnalyzer(HealthAnalyzer):
    def __init__(self, gender, age, resting_heart_rate, average_steps):
        super().__init__(gender, age, resting_heart_rate, average_steps)


    # This method determines the age catagories
    def get_age_category(self):
        if 18 <= self.age < 30:
            return "18-29"
        elif 30 <= self.age < 40:
            return "30-39"
        elif 40 <= self.age < 50:
            return "40-49"
        elif 50 <= self.age < 60:
            return "50-59"
        elif 60 <= self.age < 70:
            return "60-69"
        else:
            return "70+"


    # This function analyzes the information inputted and writes the data to CSV file
    def analyze_health(self):
        age_category = self.get_age_category()


        
        with open('health_data.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([self.gender, age_category, self.resting_heart_rate, self.average_steps])

        return age_category

class HealthProjectionAnalyzer(HealthAnalyzer):
    def __init__(self, gender):
        super().__init__(gender)

    def project_health(self):
        # Placeholder for a simplified projection logic.
        # Note: This is a basic example. In a real-world scenario, you'd need a more sophisticated approach.

        # Assuming the age categories and their midpoint values
        age_categories = ["18-29", "30-39", "40-49", "50-59", "60-69", "70+"]
        age_midpoints = [23.5, 34.5, 44.5, 54.5, 64.5, 75]

        # Placeholder arrays for projected steps and heart rates
        steps_projections = []
        heart_rate_projections = []

        # Loop through each age category to perform a basic projection
        for age_category in age_categories:
            steps_data, heart_rate_data = read_filtered_data(self.gender, age_category)

            if steps_data and heart_rate_data:
                # Using linear regression for projection
                steps_model = LinearRegression().fit(np.array(age_midpoints).reshape(-1, 1), steps_data)
                heart_rate_model = LinearRegression().fit(np.array(age_midpoints).reshape(-1, 1), heart_rate_data)

                # Predict future values
                steps_proj = steps_model.predict(np.array([age_midpoints[age_categories.index(age_category)]]).reshape(-1, 1))
                heart_rate_proj = heart_rate_model.predict(np.array([age_midpoints[age_categories.index(age_category)]]).reshape(-1, 1))

                steps_projections.append(steps_proj[0])
                heart_rate_projections.append(heart_rate_proj[0])

        # Example of how to plot the projections (can be customized or expanded)
        plt.figure(figsize=(12, 6))

        # Plotting Steps Projections
        plt.subplot(1, 2, 1)
        plt.plot(age_midpoints, steps_projections, 'o-', label='Projected Steps')
        plt.title('Projected Steps Over Age Groups')
        plt.xlabel('Age')
        plt.ylabel('Average Steps')

        # Plotting Heart Rate Projections
        plt.subplot(1, 2, 2)
        plt.plot(age_midpoints, heart_rate_projections, 'o-', label='Projected Heart Rate')
        plt.title('Projected Heart Rate Over Age Groups')
        plt.xlabel('Age')
        plt.ylabel('Resting Heart Rate')

        plt.tight_layout()
        plt.show()

    def analyze_health(self):
        self.project_health()
    plt.show()
    


# Function to generate box plots for steps and heart rate
def generate_box_plots(step_data, heart_rate_data, user_step_value, user_heart_rate_value, title):
    plt.figure(figsize=(12, 6))


    # Create box plot for steps
    plt.subplot(1, 2, 1)
    plt.boxplot(step_data)
    plt.plot(1, user_step_value, 'ro')
    plt.title(f'{title} - Steps')
    plt.ylabel('Average Steps')


    # Create box plot for resting heart rate
    plt.subplot(1, 2, 2)
    plt.boxplot(heart_rate_data)
    plt.plot(1, user_heart_rate_value, 'ro')
    plt.title(f'{title} - Resting Heart Rate')
    plt.ylabel('Resting Heart Rate')

    plt.tight_layout()
    plt.show()


# Function to read and filter data from CSV file
def read_filtered_data(gender, age_category):
    step_data = []
    heart_rate_data = []
    try:
        # Reads data from CSV and filter based on gender and age category
        with open('health_data.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if row[0] == gender and row[1] == age_category:
                    try:
                        step_data.append(int(row[3]))
                        heart_rate_data.append(int(row[2]))
                    except ValueError:
                        pass
    except FileNotFoundError:
        print("No data file found. Creating a new one.")
    return step_data, heart_rate_data


# Function which prompts the user for input data and make sure its within the valid constraints of each variable.
def get_valid_input(prompt, data_type=int, min_value=None, max_value=None):
    while True:
        try:
            user_input = data_type(input(prompt))
            if (min_value is not None and user_input < min_value) or (max_value is not None and user_input > max_value):
                raise ValueError
            return user_input
        except ValueError:
            print(f"Invalid input. Please enter a valid {data_type.__name__}", end="")
            if min_value is not None and max_value is not None:
                print(f" between {min_value} and {max_value}.")
            else:
                print(".")


# Main script to collect user data and generate plots
gender = input("Enter your gender (M/F): ").upper()

if gender not in ["M", "F"]:
    print("Error: Invalid gender. Please enter 'M' or 'F'.")

else:
    age = get_valid_input("Enter your age: ", min_value=0, max_value=120)
    resting_heart_rate = get_valid_input("Enter your resting heart rate: ", min_value=40, max_value=140)
    average_steps = get_valid_input("Enter your average steps: ", min_value=0)

    user = AgeGenderAnalyzer(gender, age, resting_heart_rate, average_steps)
    user_category = user.analyze_health()
    filtered_steps, filtered_heart_rates = read_filtered_data(gender, user_category)


    # Generates and displays box plots if the correct data is available
    if filtered_steps and filtered_heart_rates:
        generate_box_plots(filtered_steps, filtered_heart_rates, user_step_value=user.average_steps, user_heart_rate_value=user.resting_heart_rate, title=f'Health Analysis - {user_category} ({gender}, {age} years)')
    else:
        print("No matching data found in the file for comparison.")

projection_analyzer = HealthProjectionAnalyzer(gender)
projection_analyzer.analyze_health()  # This will create and show the XY plots

