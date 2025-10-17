# Name: Charlotte Norment 
# Date: 10/15/25
# Assignment: SI 201 Project 1
# Collaborators: None 


# Step 1: Load Data
import csv

def load_penguins(csv_file_path):
    penguin_data = [] 
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file) 
    
        # first requirement: list of variables
        variables = reader.fieldnames
        print(f"List of variables (columns): {variables}")

        for row in reader: 
            # second requirement: sample entry 
            if not penguin_data:
                sample_entry = row.copy()

            cleaned_row = {}
            for key, value in row.items():
                # strip whitespace
                clean_key = key.strip()

                # convert to float if value is not 'na'
                if clean_key in ['bill_length_mm, 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']:
                    cleaned_row[clean_key] = float(value) if value and value.strip().lower() != 'na'

                # other columns stay as strings 
                else:
                    cleaned_row[clean_key] = value.strip() if value else None 

            # only append if we have necessary data and skip if important data is missing
            if cleaned_row.get('species') is not None:
                penguin_data.append(cleaned_row) 

    # third requirement: number of rows after cleaning
    num_rows = len(penguin_data)
    print(f"Total number of penguin data rows: {num_rows}")

    #print sample row
    if penguin_data:
        print("\nSample Cleaned Entry:")
        for key, value in penguin_data[0].items():
            print(f" {key}: {value}")

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
        
        with open(output_file_path, 'w') as f:
            f.write("\n Penguin Data Analysis Report \n")

        # write report for calculation 1
        f.write("Calculation 1: Flipper Lengths > 200mm  \n")

        for category, results in flipper_results.items():
            f.write(f"Analysis by {category}:\n")

            if results:
                for group, percentage in results.items():
                # make sure string is clean
                cleaned_percent = f"{percentage * 100:.1f}%"
                f.write(f" {group.1just(10)}: {cleaned_percent}\n")

            else:
                f.write("No data found for this category\n")
            f.write("\n")

        # write report for calculation 2
        f.write("Calculation 2: Averages for {island_results['Island Name']} Island  \n")
        if 'Error' in island_results:
            f.write(f"Error: {island_results['Error']}")




#call to main
def main():
    # define file path 
    data_file = 'penguins.csv'

    # define chosen island for calculation 2
    chosen_island = 'Dream'

    # call load_penguins to load the data
    penguin_data = load_penguins(data_file)

if __name__ == "__main__":
    csv_data = load_penguins("penguins.csv")
    for row in csv_data:
        print(row)