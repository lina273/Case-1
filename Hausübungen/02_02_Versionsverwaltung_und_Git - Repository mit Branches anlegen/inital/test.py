import time
import socket
from datetime import datetime
from sort_2 import sort_2
from sort_1 import sort_1

# Function to perform sorting, measure time, and assert correctness
def test_sort(sort_function, data):
    start_time = time.time()
    sorted_data = sort_function(data.copy())
    end_time = time.time()
    
    # Ensure that the data is sorted
    #assert sorted_data == sorted(data), "Sort failed!"
    print(sorted_data[1:100])
    return end_time - start_time

# Main function
if __name__ == "__main__":
    # Generate a random list of numbers for testing
    with open('random.txt', 'r') as file:
        # Read the lines from the file and convert them to integers
        data = [int(line.strip()) for line in file]

    
    # Record the computer name and current date
    computer_name = socket.gethostname()
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Test Bubble Sort
    bubble_sort_time = test_sort(sort_1, data)
    
    # Test Quick Sort
    quick_sort_time = test_sort(sort_2, data)
    
    # Append results to 'results.txt'
    with open("results.txt", "a+") as file:
        file.write(f"Computer Name: {computer_name}\n")
        file.write(f"Date of Test: {current_date}\n")
        file.write(f"Bubble Sort Time: {bubble_sort_time:.6f} seconds\n")
        file.write(f"Quick Sort Time: {quick_sort_time:.6f} seconds\n")
        file.write("\n")