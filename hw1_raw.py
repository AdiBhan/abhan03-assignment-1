# Part 1: (3, 1.5). We need to find the midpoint of the building. A point that has equal distance to any elevator since
# each elevator has equal probability to be chosen/open
# Finding the avg: x = (1 + 1 + 3 + 3 + 5 + 5)/6 = 3. y = 0+0+0+3+3+3 / 6 = 1.5. Thus the best position to be at is (3,1.5)


# Part 2:

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


def parse_data(file_path):
    '''parse_data() function parses data.txt and extracts timestamps and elevator_id'''
    data = []

    with open(file_path, 'r') as file:
        for line in file:

            timestamp, elevator_id = line.strip().split('\t')
            print(line.strip())
            data.append((timestamp, int(elevator_id)))

    # Create a DataFrame from the parsed data
    df = pd.DataFrame(data, columns=['Timestamp', 'Elevator ID'])

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    return df


def make_plot(df):
    #     '''
    #     You will need to read the training data CSV file and do some processing first.
    #     '''
    #     # TODO
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Timestamp'], df['Elevator ID'], c='blue', marker='o')
    plt.xlabel('Timestamp')
    plt.ylabel('Elevator ID')
    plt.title('Elevator Usage Over Time')
    plt.xticks(rotation=45)
    plt.savefig("./CS506/hw1/chart.png")


file_path = os.path.join(os.getcwd(), "CS506", "hw1", 'data.txt')
if os.path.exists(file_path):
    print("Found file ", file_path)
else:
    print("File not found. Please check the file path.")

df = parse_data(file_path)
print(df)
make_plot(df)

# Observations:

# 1. Elevators 1-6 have relatively consistent usage throughout the time range,
# with no elevator being used significantly more or less than others.

# 2.In the plot, there aren't any clear/recurring cycles over time for elevator usage.
#   The timestamps are fairly uniform, and the dots are spread out somewhat evenly for each elevator.


# Part 3:
def calc_avg_freq(df):
    '''calc_avg_freq() calculates average frequency and returns a dataframe representing a table with the elevator_id, total num of arrivals, and avg frequency'''
    # Calculate the total time span (in seconds)
    total_duration = (df['Timestamp'].max() -
                      df['Timestamp'].min()).total_seconds()

    # Calculate the total number of arrivals for each elevator
    elevator_counts = df['Elevator ID'].value_counts().sort_index()

    # Calculate average frequency for each elevator
    avg_frequencies = elevator_counts / total_duration

    # Create a DataFrame to display results
    avg_frequency_df = pd.DataFrame({
        'Elevator ID': elevator_counts.index,
        'Total Data Collection Time (seconds)': [int(total_duration)] * len(elevator_counts),
        'Total Arrivals': elevator_counts.values,
        'Average Frequency (arrivals per second)': avg_frequencies.values
    })

    return avg_frequency_df


# Calculate average frequencies
avg_frequency_df = calc_avg_freq(df)

# Display the DataFrame
print(avg_frequency_df)

# part 4


def calculate_probabilities(avg_frequency_df):
    # Sum of all average frequencies
    total_frequency = avg_frequency_df['Average Frequency (arrivals per second)'].sum(
    )

    # Calculate the probability for each elevator
    avg_frequency_df['Probability'] = avg_frequency_df[
        'Average Frequency (arrivals per second)'] / total_frequency

    # Ensure probabilities sum to 1 (normalized)
    return avg_frequency_df


# Calculate probabilities based on average frequencies
avg_frequency_df = calc_avg_freq(df)  # Ensure df has been parsed earlier
avg_frequency_df_with_probabilities = calculate_probabilities(avg_frequency_df)

# Part 5


def calculate_optimal_position(avg_frequency_df, elevator_coords):
    # Calculate the weighted average of the X and Y coordinates
    optimal_x = sum(elevator_coords[i][0] * avg_frequency_df['Probability'].values[i]
                    for i in range(len(elevator_coords)))
    optimal_y = sum(elevator_coords[i][1] * avg_frequency_df['Probability'].values[i]
                    for i in range(len(elevator_coords)))

    return optimal_x, optimal_y


# Coordinates for the elevators (these need to be based on your diagram)
elevator_coords = [(1, 0), (1, 0), (3, 3), (3, 3), (5, 3), (5, 3)]

# Calculate optimal position
optimal_x, optimal_y = calculate_optimal_position(
    avg_frequency_df_with_probabilities, elevator_coords)

# Print the result
print(f"The optimal position to wait is at coordinates: ({
      optimal_x:.2f}, {optimal_y:.2f})")


# Part 6:

# Function to calculate the Euclidean distance

def calculate_distance(coord1, coord2):
    return np.sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2)

# Function to calculate the average walk distance from a given point


def get_average_walk_distance(data, coordinate, elevator_coords):
    total_distance = 0
    count = 0

    # Loop through each data sample to calculate the distance
    for _, row in data.iterrows():
        elevator_id = row['Elevator ID']
        # Adjust for 0-based indexing
        elevator_coord = elevator_coords[elevator_id - 1]
        distance = calculate_distance(coordinate, elevator_coord)
        total_distance += distance
        count += 1

    # Calculate the average distance
    average_walk_distance = total_distance / count
    return average_walk_distance


# Example usage
elevator_coords = [(1, 0), (3, 0), (5, 0), (3, 3), (1, 3),
                   (5, 3)]  # Elevator coordinates

# Midpoint from question 1: (3, 1.5)
midpoint = (3, 1.5)

# Optimal point from question 5: (3.02, 2.03)
optimal_point = (3.02, 2.03)

# Assuming 'df' contains the parsed data
average_distance_midpoint = get_average_walk_distance(
    df, midpoint, elevator_coords)
average_distance_optimal = get_average_walk_distance(
    df, optimal_point, elevator_coords)

# Print the results
print(f"Average distance from the midpoint (3, 1.5): {
      average_distance_midpoint:.4f}")
print(f"Average distance from the optimal point (3.02, 2.03): {
      average_distance_optimal:.4f}")


# Part 7 (3)

def parse_data_csv(file_path):

    data = []
    with open(file_path, 'r') as file:
        for line in file:

            timestamp, elevator_id, _ = line.strip().split(',')

            data.append((timestamp, int(elevator_id)))
   # Create a DataFrame from the parsed data
    df = pd.DataFrame(data, columns=['Timestamp', 'Elevator ID'])

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    return df


file_path_csv = os.path.join(os.getcwd(), 'CS506','hw1', 'cdsdata.csv')
df1 = parse_data_csv(file_path_csv)
avg_dist_midpoint_p1 = get_average_walk_distance(
    df1, midpoint, elevator_coords)
avg_dist_midpoint_p2 = get_average_walk_distance(
    df1, optimal_point, elevator_coords)
print("Part 7 MidPoint based on part 1", avg_dist_midpoint_p1)
print("Part 7 MidPoint based on part 5", avg_dist_midpoint_p2)
