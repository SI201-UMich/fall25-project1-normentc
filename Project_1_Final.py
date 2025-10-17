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


def main():
    # define file path 
    data_file = 'penguins.csv'

    # define chosen island for calculation 2
    chosen_island = 'Dream'

    # call load_penguins to load the data
    penguin_data = load_penguins(data_file)

# Step 2: Calculation 1  
    #def calculate_flipper_percentages():

# Step 3: Calculation 2
    #def calculate_island_averages():

# Step 4: Report Results
    #def write_report():

#call to main
if __name__ == "__main__":
    csv_data = load_penguins("penguins.csv")
    for row in csv_data:
        print(row)