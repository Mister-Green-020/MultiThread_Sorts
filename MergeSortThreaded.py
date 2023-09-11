import threading
import time
import random

# Number of elements in the array to be sorted
MAX_NUM_ELEMENTS = 100000

# Number of threads to use
# Minimum number of 4 threads
MAX_THREADS = 100

# Intialize the array to be sorted
array = [0] * MAX_NUM_ELEMENTS
part = 0



def merge(low, mid, high):
    """Merge the two sorted arrays.

    Args:
        low (int): index for when the left array starts
        mid (int): index for when the left array ends and the right array starts
        high (int): index for when the right array ends
    """
    # Create temp arrays
    left = array[low:mid+1]
    left_size = len(left)
    right = array[mid+1:high+1]
    right_size = len(right)
    
    # Initialize the pointers
    left_pointer = right_pointer = 0
    temp_pointer = low
    
    while left_pointer < left_size and right_pointer < right_size:
        # Add the largest element from the temp array to the main array
        if left[left_pointer] <= right[right_pointer]:
            array[temp_pointer] = left[left_pointer]
            left_pointer += 1
        else:
            array[temp_pointer] = right[right_pointer]
            right_pointer += 1
        temp_pointer += 1
    
    while left_pointer < left_size:
        # Add the remaining elements from the left array
        array[temp_pointer] = left[left_pointer]
        left_pointer += 1
        temp_pointer += 1
        
    while right_pointer < right_size:
        # Add the remaining elements from the right array
        array[temp_pointer] = right[right_pointer]
        right_pointer += 1
        temp_pointer += 1
    
def merge_sort(low, high):
    """Recursively splits the array and runs merge_sort

    Args:
        low (int): The index for the first element in the array
        high (int): The index for the last element in the array
    """
    if low < high:
        # Determine mid point
        mid = low + (high - low) // 2
        
        # Split array into two arrays
        merge_sort(low, mid)
        merge_sort(mid + 1, high)
        
        # Merge two halves
        merge(low, mid, high)
    
def merge_sort_threaded():
    """Spawns multiple threads to preform merge sort
    """
    global part
    
    # Spawn the threads
    for i in range(MAX_THREADS):
        thread = threading.Thread(target=merge_sort, args=(part*(MAX_NUM_ELEMENTS//4), (part+1)*(MAX_NUM_ELEMENTS//4)-1))
        part += 1
        thread.start()
        
    # Join the threads
    for i in range(MAX_THREADS):
        thread.join()
    
    # Merge the final parts
    merge(0, (MAX_NUM_ELEMENTS // 2 - 1) // 2, MAX_NUM_ELEMENTS // 2 - 1)
    merge(MAX_NUM_ELEMENTS // 2, MAX_NUM_ELEMENTS // 2 + (MAX_NUM_ELEMENTS - 1 - MAX_NUM_ELEMENTS // 2) // 2, MAX_NUM_ELEMENTS - 1)
    merge(0, (MAX_NUM_ELEMENTS - 1) // 2, MAX_NUM_ELEMENTS - 1)


if __name__ == '__main__':
    # generating random values in array
    for i in range(MAX_NUM_ELEMENTS):
        array[i] = random.randint(0, 100)
 
    # t1 and t2 for calculating time for merge sort
    t1 = time.perf_counter()
 
    merge_sort_threaded()
 
    t2 = time.perf_counter()
 
    # print("Sorted array:", array)
    print(f"Time taken: {t2 - t1:.6f} seconds")
    
    for i in range(MAX_NUM_ELEMENTS):
        array[i] = random.randint(0, 100)
 
    # t1 and t2 for calculating time for merge sort
    t1 = time.perf_counter()
 
    merge_sort(0, MAX_NUM_ELEMENTS)
 
    t2 = time.perf_counter()
    # print("Sorted array:", array)
    print(f"Time taken: {t2 - t1:.6f} seconds")
        