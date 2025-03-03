import numpy as np

# num_processes = int(input("Enter Number of Processes: "))
# num_resources = int(input("Enter Number of Resources: "))

# total_resource_instance = np.zeros((1,num_resources))

# for i in range(num_resources):
#     total_resource_instance[0,i] = int(input(f"Enter the maximum number of instances of resource {i}: "))

# instances_allocated = np.zeros((num_processes, num_resources))

# for i in range (num_processes):
#     for j in range(num_resources):
#         instances_allocated[i, j] = int(input(f"Enter the number of instances of resource {j} allocated for process {i}"))


num_processes = 5 
num_resoureces = 3
total_resource_instance = np.array([10, 5, 7])
instances_allocated = np.array([[0, 1, 0],
                               [2, 0, 0],
                               [3, 0, 2],
                               [2, 1, 1],
                               [0, 0, 2]])

max_allocation_required = np.array([[7, 5, 3],
                                    [3, 2, 2],
                                    [9, 0, 2],
                                    [4, 2, 2],
                                    [5, 3, 3]]) 

instances_available = total_resource_instance - np.sum(instances_allocated, axis=0)

remaining_need = max_allocation_required - instances_allocated

print(remaining_need)
