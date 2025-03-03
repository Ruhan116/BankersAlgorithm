import numpy as np
import pandas as pd

def read_input(file_path):
    df = pd.read_csv(file_path, delimiter='\t')
    df = df.replace('-', 0)  
    
    allocation = df[['Allocation_A', 'Allocation_B', 'Allocation_C']].to_numpy().astype(int)
    max_allocation = df[['Max_A', 'Max_B', 'Max_C']].to_numpy().astype(int)
    
    total_resources = np.array([10, 5, 7])  
    allocated_total = np.sum(allocation, axis=0)
    available = total_resources - allocated_total
    
    step_info = {
        "step": "Calculating available resources",
        "what": "Determining the current available resources",
        "why": "To know how many resources are free to allocate",
        "how": f"Subtracting total allocated resources ({allocated_total}) from total resources ({total_resources})",
        "result": f"Available resources are {available}"
    }
    
    setup_steps.append(step_info)
    
    return allocation, max_allocation, available

def calculate_need(allocation, max_allocation):
    need = max_allocation - allocation
    
    step_info = {
        "step": "Calculating remaining need matrix",
        "what": "Computing how many more resources each process needs",
        "why": "To determine if processes can complete with available resources",
        "how": "Subtracting current allocation from maximum need for each process",
        "result": f"Need matrix calculated"
    }
    
    setup_steps.append(step_info)
    
    return need

def BankersAlgorithm(instances_available, remaining_need, visited, sequence, all_sequences, all_steps, current_path_steps):
    path_step = {
        "step": f"Exploring safe sequence {' -> '.join(sequence)}",
        "what": f"Finding processes that can safely execute with available resources: {instances_available}",
        "why": "To identify safe execution sequences that avoid deadlock",
        "how": "Checking if any unvisited process can have its needs satisfied with available resources"
    }
    current_path_steps.append(path_step)
    
    found = False  
    for i in range(num_processes):
        if not visited[i] and np.all(remaining_need[i] <= instances_available):
            process_step = {
                "step": f"Process P{i} can execute safely",
                "what": f"Simulating execution of process P{i}",
                "why": f"P{i}'s needs ({remaining_need[i]}) are <= available resources ({instances_available})",
                "how": f"Marking P{i} as visited and adding its allocated resources to available pool",
                "result": f"After P{i} completes, resources available will be {instances_available + allocation[i]}"
            }
            current_path_steps.append(process_step)
            
            visited[i] = True  
            new_available = instances_available + allocation[i]
            
            new_path_steps = current_path_steps.copy()
            
            BankersAlgorithm(new_available, remaining_need, visited, sequence + [f"P{i}"], 
                            all_sequences, all_steps, new_path_steps)  
            
            visited[i] = False 
            found = True
            
            current_path_steps.pop()
    
    if not found and len(sequence) == num_processes:  
        complete_step = {
            "step": "Complete safe sequence found",
            "what": "Identified a full sequence where all processes can complete",
            "why": "All processes have been safely scheduled",
            "how": f"Successfully assigned all {num_processes} processes in sequence {' -> '.join(sequence)}",
            "result": "Adding sequence to safe sequences list"
        }
        current_path_steps.append(complete_step)
        
        path_sequence = ' -> '.join(sequence)
        all_sequences.append(path_sequence)
        all_steps[path_sequence] = current_path_steps.copy()
    elif not found:
        dead_end_step = {
            "step": "Dead end reached in current path",
            "what": "No more processes can safely execute from current state",
            "why": "Remaining processes' needs exceed available resources",
            "how": "Backtracking to explore other possible sequences",
            "result": f"Abandoning current partial sequence {' -> '.join(sequence)}"
        }
        current_path_steps.append(dead_end_step)

def print_step_details(step_dict):
    print(f"  Step: {step_dict['step']}")
    print(f"  What: {step_dict['what']}")
    print(f"  Why: {step_dict['why']}")
    print(f"  How: {step_dict['how']}")
    if 'result' in step_dict:
        print(f"  Result: {step_dict['result']}")
    print()

if __name__ == "__main__":
    file_path = 'input0.csv'
    
    setup_steps = []
    
    allocation, max_allocation, available = read_input(file_path)
    
    num_processes = allocation.shape[0]
    remaining_need = calculate_need(allocation, max_allocation)
    
    all_safe_sequences = []
    all_path_steps = {}
    
    visited = np.zeros(num_processes, dtype=bool)
    BankersAlgorithm(available, remaining_need, visited, [], all_safe_sequences, all_path_steps, [])
    
    print("=== INITIAL SETUP ===")
    for step in setup_steps:
        print_step_details(step)
    
    print("=== FIRST 3 SAFE SEQUENCES WITH DETAILED STEPS ===")
    for i, seq in enumerate(all_safe_sequences[:3], 1):
        print(f"\nSEQUENCE {i}: {seq}")
        print("-" * 50)
        
        for step in all_path_steps[seq]:
            print_step_details(step)
    
    print(f"\nTotal number of safe sequences found: {len(all_safe_sequences)}")