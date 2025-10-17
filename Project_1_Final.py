# Name: Charlotte Norment 
# UMID: 47500946
# Date: 10/15/25
# Course: SI 201, Section 006
# Assignment: Project 1
# Collaborators: None 
# Gen AI Use: I worked with Google Gemini to plan the overall structure of the code, determine how the functions would call each other, and debug the errors and failed tests.


# Step 1: Load Data
import csv

def load_penguins(csv_file_path):
    penguin_data = [] 
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file) 
    
        # first requirement: list of variables
        variables = reader.fieldnames
        print("Initial Data Analysis")
        print(f"List of variables (columns): {variables}")

        sample_entry = None 

        for row in reader: 
            # second requirement: sample entry 
            cleaned_row = {}
            for key, value in row.items():
                # strip whitespace
                clean_key = key.strip()

                # convert to float if value is not 'na'
                if clean_key in ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']:
                    cleaned_row[clean_key] = float(value) if value and value.strip().lower() != 'na' else None

                # other columns stay as strings 
                else:
                    cleaned_row[clean_key] = value.strip() if value else None 

            # only append if we have necessary data and skip if important data is missing
            if cleaned_row.get('species') is not None:
                penguin_data.append(cleaned_row) 
                if sample_entry is None:
                    sample_entry = cleaned_row.copy()

    # third requirement: number of rows after cleaning
    num_rows = len(penguin_data)
    print(f"Total number of penguin data rows: {num_rows}")

    #print sample row
    if sample_entry:
        print("\nSample Cleaned Entry:")
        for key, value in sample_entry.items():
            print(f" {key}: {value} (Type: {type(value).__name__})")

    return penguin_data                           



# Step 2: Calculation 1 

# helper function to calculate percentage of rows that meet criteria  
def get_percentage(group_key, data, min_flipper_length):

    # total count for each category 
    category_counts = {}

    # count of penguins that meet criteria
    criteria_counts = {}

    for record in data:
        category = record.get(group_key)
        flipper_length = record.get('flipper_length_mm')

        # skip missing data
        if category is None or flipper_length is None:
            continue 
            
        # tally for the total counts 
        category_counts[category] = category_counts.get(category, 0) + 1
        criteria_counts[category] = criteria_counts.get(category, 0) 

        # tally for the counts that meet the length criteria
        if flipper_length > min_flipper_length:
            criteria_counts[category] +=1 

    # final percentages
    group_percentages = {}
    for category, total in category_counts.items():
        if total > 0:
            count = criteria_counts.get(category, 0)
            percentage = count / total
            group_percentages[category] = percentage 
        else: 
            group_percentages[category] = 0

    return group_percentages 

# perform calculation 1 (percent of each species and sex with flipper length greater than 200mm)
def calculate_flipper_percentages(data):
    min_flipper = 200

    # percentages by species 
    species_percentages = get_percentage('species', data, min_flipper)

    # percentages by sex 
    sex_percentages = get_percentage('sex', data, min_flipper)

    # store results in a dict for report function 
    flipper_results = {
        'Species > 200mm': species_percentages,
        'Sex > 200mm': sex_percentages
    }

    return flipper_results 



# Step 3: Calculation 2

def calculate_island_averages(data, chosen_island):
    total_length = 0.0
    total_depth = 0.0
    count = 0 

    # loop through penguin records
    for record in data:
    
        # filter to see if the record is for the chosen island
        if record.get('island') == chosen_island:
        
            # get the data 
            bill_length = record.get('bill_length_mm')
            bill_depth = record.get('bill_depth_mm')

            # check for missing data 
            if bill_length is not None and bill_depth is not None:
                total_length += bill_length
                total_depth += bill_depth 
                count += 1 

    # calculate averages 
    if count > 0:
        avg_length = total_length / count
        avg_depth = total_depth / count 

        island_results = {
            'Island Name': chosen_island,
            'Average Bill Length (mm)': round(avg_length, 2),
            'Average Bill Depth (mm)': round(avg_depth, 2),
            'Sample Size (Count)': count 
        }
    
    # account for cases where island does not have valid data
    else:
        island_results = {
            'Island Name': chosen_island,
            'Error': 'No valid data for island',
            'Sample Size (Count)': 0 
        }

    return island_results 



# Step 4: Report Results
def write_report(flipper_results, island_results, output_file_path):
    try:
        with open(output_file_path, 'w') as f:
            f.write("\n Penguin Data Analysis Report \n\n")

            # write report for calculation 1
            f.write("Calculation 1: Flipper Lengths > 200mm  \n\n")

            for category, results in flipper_results.items():
                f.write(f"Analysis by {category}:\n")

                if results:
                    for group, percentage in results.items():
                        # make sure string is clean
                        cleaned_percent = f"{percentage * 100:.1f}%"
                        f.write(f" {group.ljust(10)}: {cleaned_percent}\n")

                else:
                    f.write("No data found for this category\n")
                f.write("\n")

            # write report for calculation 2
            f.write(f"\nCalculation 2: Averages for {island_results['Island Name']} Island  \n")
            if 'Error' in island_results:
                f.write(f"Error: {island_results['Error']}\n")
                f.write(f"Sample Size: {island_results['Sample Size (Count)']}\n")
            else:
                f.write(f"Island analyzed: {island_results['Island Name']}\n")
                f.write(f"Sample Size (Count): {island_results['Sample Size (Count)']}\n")
                f.write(f"Average Bill Length: {island_results['Average Bill Length (mm)']} mm\n")
                f.write(f"Average Bill Depth: {island_results['Average Bill Depth (mm)']} mm\n")

            f.write("\n")

            print(f"Success: report successfully written to '{output_file_path}'")

    except IOError as e:
        print(f"Error: Could not write file '{output_file_path}'")

# Step 5: test cases
def test_functions():
    test_data = [
        # 0: Long Flipper, Male, Island A (Contributes to all counts)
        {'species': 'Adelie', 'sex': 'Male', 'flipper_length_mm': 210.0, 
         'bill_length_mm': 40.0, 'bill_depth_mm': 18.0, 'island': 'Island A'},
        # 1: Short Flipper, Female, Island A (Contributes to total, not criteria)
        {'species': 'Adelie', 'sex': 'Female', 'flipper_length_mm': 180.0, 
         'bill_length_mm': 42.0, 'bill_depth_mm': 17.0, 'island': 'Island A'},
        # 2: Long Flipper, Female, Island B (Contributes to all counts)
        {'species': 'Chinstrap', 'sex': 'Female', 'flipper_length_mm': 201.0, 
         'bill_length_mm': 50.0, 'bill_depth_mm': 16.0, 'island': 'Island B'},
        # 3: Short Flipper, Male, Island B (Contributes to total, not criteria)
        {'species': 'Chinstrap', 'sex': 'Male', 'flipper_length_mm': 195.0, 
         'bill_length_mm': 48.0, 'bill_depth_mm': 19.0, 'island': 'Island B'},
        # 4: Missing Flipper (Edge Case: Should be skipped for flipper calc)
        {'species': 'Adelie', 'sex': 'Male', 'flipper_length_mm': None, 
         'bill_length_mm': 35.0, 'bill_depth_mm': 14.0, 'island': 'Island C'},
        # 5: Missing Bill (Edge Case: Should be skipped for island calc)
        {'species': 'Adelie', 'sex': 'Male', 'flipper_length_mm': 215.0, 
         'bill_length_mm': None, 'bill_depth_mm': None, 'island': 'Island A'},
        # 6: Island A, Flipper=200 (Edge Case: Should NOT be included since > 200)
        {'species': 'Adelie', 'sex': 'Female', 'flipper_length_mm': 200.0, 
         'bill_length_mm': 45.0, 'bill_depth_mm': 15.0, 'island': 'Island A'},
    ]


    # tests for get_percentage
    print(f"Testing get_percentage")

    # test 1 (general): group by species, threshold 200mm
    test_1_results = get_percentage('species', test_data, 200)
    test_1_expected = {'Adelie': 0.5, 'Chinstrap': 0.5}
    check_test_1 = abs(test_1_results['Adelie'] - test_1_expected['Adelie']) < 0.001 and test_1_results['Chinstrap'] == test_1_expected['Chinstrap']
    print(f"Test 1 (General, Species): Pass={check_test_1}")

    # test 2 (general): group by sex, threshold 195mm
    test_2_results = get_percentage('sex', test_data, 195)
    test_2_expected = {'Male': 2/3, 'Female': 2/3}
    check_test_2 = abs(test_2_results['Male'] - test_2_expected['Male']) < 0.001 and abs(test_2_results['Female'] - test_2_expected['Female']) < 0.001
    print(f"Test 2 (General, Sex): Pass={check_test_2}")

    # test 3 (edge): flipper_length = None 
    test_3_results = get_percentage('species', test_data, 200)
    test_3_expected = {'Adelie': 0.5, 'Chinstrap': 0.5}
    check_test_3 = abs(test_3_results['Adelie'] - test_3_expected['Adelie']) < 0.001
    print(f"Test 3 (Edge, Missing Flipper): Pass={check_test_3}")

    # test 4 (edge): category not in the data 
    test_4_results = get_percentage('Unknown_Column', test_data, 190)
    test_4_expected = {}
    check_test_4 = test_4_results == test_4_expected
    print(f"Test 4 (Edge, Non-existent Category): Pass={check_test_4}")



    # tests for calculate_flipper_percentages 
    print(f"Testing calculate_flipper_percentages")

    # test 5 (general): species and sex results 
    test_5_results = calculate_flipper_percentages(test_data)
    test_5_expected_species = {'Adelie': 0.5, 'Chinstrap': 0.5}
    test_5_expected_sex = {'Male': 2/3, 'Female': 1/3}
    check_test_5 = (test_5_results['Species > 200mm']['Adelie'] - test_5_expected_species['Adelie'] and 
                    test_5_results['Species > 200mm']['Chinstrap'] == test_5_expected_species['Chinstrap'] and
                    abs(test_5_results['Sex > 200mm']['Male'] - test_5_expected_sex['Male']) < 0.001 and 
                    abs(test_5_results['Sex > 200mm']['Female'] - test_5_expected_sex['Female']) < 0.001)
    print(f"Test 5 (General, Species and Sex Results): Pass={check_test_5}")

    # test 6 (general): correct keys 
    test_6_results = calculate_flipper_percentages(test_data)
    test_6_expected = ['Species > 200mm', 'Sex > 200mm']
    check_test_6 = all(key in test_6_results for key in test_6_expected) and len(test_6_results) == 2
    print(f"Test 6 (General, Dictionary Keys): Pass={check_test_6}") 

    # test 7 (edge): empty list
    test_7_results = calculate_flipper_percentages([])
    test_7_expected = {'Species > 200mm': {}, 'Sex > 200mm': {}}
    check_test_7 = test_7_results == test_7_expected
    print(f"Test 7 (Edge, Empty List): Pass={check_test_7}")

    # test 8 (edge): expected percentage = 0
    test_data_8 = [
        {'species': 'Gento', 'sex': 'Female', 'flipper_length_mm': 150.0},
        {'species': 'Gento', 'sex': 'Female', 'flipper_length_mm': 155.0}
    ]
    test_8_results = calculate_flipper_percentages(test_data_8)
    test_8_expected = {'Species > 200mm': {'Gento': 0.0}, 'Sex > 200mm': {'Female': 0.0}}
    check_test_8 = test_8_results == test_8_expected
    print(f"Test 8 (Edge, 0 percent): Pass={check_test_8}")



    # tests for calculate_island_averages
    print(f"Testing calculate_island_averages")

    # test 9 (general): Island A
    test_9_results = calculate_island_averages(test_data, 'Island A')
    test_9_expected = {'Island Name': 'Island A', 'Average Bill Length (mm)': 42.33, 'Average Bill Depth (mm)': 16.67, 'Sample Size (Count)': 3}
    check_test_9 = (test_9_results['Sample Size (Count)'] == 3 and
                    test_9_results['Average Bill Length (mm)'] == test_9_expected['Average Bill Length (mm)'] and
                    test_9_results['Average Bill Depth (mm)'] == test_9_expected['Average Bill Depth (mm)'])
    print(f"Test 9 (General, Island A): Pass={check_test_9}")

    # test 10 (general): Island B
    test_10_results = calculate_island_averages(test_data, 'Island B')
    test_10_expected = {'Island Name': 'Island B', 'Average Bill Length (mm)': 49.00, 'Average Bill Depth (mm)': 17.50, 'Sample Size (Count)': 2}
    check_test_10 = (test_10_results['Sample Size (Count)'] == 2 and
                    test_10_results['Average Bill Length (mm)'] == test_10_expected['Average Bill Length (mm)'] and
                    test_10_results['Average Bill Depth (mm)'] == test_10_expected['Average Bill Depth (mm)'])
    print(f"Test 10 (General, Island B): Pass={check_test_10}")

    # test 11 (edge): Island Not Found
    test_11_results = calculate_island_averages(test_data, 'Island Z')
    check_test_11 = 'Error' in test_11_results and test_11_results['Sample Size (Count)'] == 0
    print(f"Test 11 (Edge, Island Not Found): Pass={check_test_11}")

    # test 12 (edge): Island Missing Bill Data
    test_data_12 = [
        {'island': 'Island D', 'bill_length_mm': None, 'bill_depth_mm': None},
        {'island': 'Island D', 'bill_length_mm': None, 'bill_depth_mm': None}
    ]
    test_12_results = calculate_island_averages(test_data_12, 'Island D')
    check_test_12 = 'Error' in test_12_results and test_12_results['Sample Size (Count)'] == 0 
    print(f"Test 12 (Edge, Island Missing Bill Data): Pass={check_test_12}")


# Step 5: main function
def main():
    # define file path 
    data_file = 'penguins.csv'

    # define chosen island for calculation 2
    chosen_island = 'Dream'

    # call load_penguins to load the data
    penguin_data = load_penguins(data_file)

    # calculation 1
    flipper_results = calculate_flipper_percentages(penguin_data)

    # calculation 2 
    island_results = calculate_island_averages(penguin_data, chosen_island)

    # report results 
    write_report(flipper_results, island_results, 'analysis_report.txt')

    # tests
    test_functions()

    print(f"\nDone")

if __name__ == "__main__":
    main()