import numpy as np
import pandas as pd
import re
import sys

def validate_file_format(df):
    if df.empty:
        return False, "File is empty"
    
    if 'PID' not in df.columns:
        return False, "PID column is missing"

    allocation_cols = [col for col in df.columns if col.startswith('Allocation_')]
    max_cols = [col for col in df.columns if col.startswith('Max_')]
    
    if not allocation_cols or not max_cols:
        return False, "Allocation or Max columns are missing"
    
    allocation_resources = [col.split('_')[1] for col in allocation_cols]
    max_resources = [col.split('_')[1] for col in max_cols]
    
    if set(allocation_resources) != set(max_resources):
        return False, "Resource types don't match between Allocation and Max columns"
    
    expected_resources = [chr(65 + i) for i in range(len(allocation_resources))]
    if sorted(allocation_resources) != sorted(expected_resources):
        return False, "Resource types don't follow the expected alphabetical sequence"
    
    return True, "Valid File Format"

def read_input(file_path):
    try:
        df = pd.read_csv(file_path, delimiter='\t')
        
        # Validate file format
        is_valid, message = validate_file_format(df)
        print(message)
        if not is_valid:
            sys.exit(1)
        
        df = df.replace('-', 0)  
        
        allocation_cols = [col for col in df.columns if col.startswith('Allocation_')]
        max_cols = [col for col in df.columns if col.startswith('Max_')]
        
        allocation_cols.sort(key=lambda x: x.split('_')[1])
        max_cols.sort(key=lambda x: x.split('_')[1])
        
        resource_types = [col.split('_')[1] for col in allocation_cols]
        num_resources = len(resource_types)
        
        allocation = df[allocation_cols].to_numpy().astype(int)
        max_allocation = df[max_cols].to_numpy().astype(int)
        
        total_resources = np.array([10, 5, 7] + [8] * (num_resources - 3))
        if num_resources < 3:
            total_resources = total_resources[:num_resources]
            
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
        
        return allocation, max_allocation, available, resource_types
    
    except Exception as e:
        print(f"Error reading input file: {e}")
        print("Invalid File Format")
        sys.exit(1)

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
                "how": "Marking P{i} as visited and adding its allocated resources to available pool",
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
    file_path = sys.argv[1] if len(sys.argv) > 1 else 'sample-input-file.csv'
    
    setup_steps = []
    
    allocation, max_allocation, available, resource_types = read_input(file_path)
    
    num_processes = allocation.shape[0]
    num_resources = len(resource_types)
    
    print(f"\nDetected {num_processes} processes and {num_resources} resources ({', '.join(resource_types)})")
    
    remaining_need = calculate_need(allocation, max_allocation)
    
    print("\nRemaining Need Matrix:")
    need_df = pd.DataFrame(remaining_need, columns=[f"Need_{r}" for r in resource_types])
    need_df.insert(0, 'PID', [f"P{i}" for i in range(num_processes)])
    print(need_df)
    
    all_safe_sequences = []
    all_path_steps = {}
    
    visited = np.zeros(num_processes, dtype=bool)
    BankersAlgorithm(available, remaining_need, visited, [], all_safe_sequences, all_path_steps, [])
    
    print("\n=== INITIAL SETUP ===")
    for step in setup_steps:
        print_step_details(step)
    
    print("=== FIRST 3 SAFE SEQUENCES WITH DETAILED STEPS ===")
    for i, seq in enumerate(all_safe_sequences[:3], 1):
        print(f"\nSEQUENCE {i}: {seq}")
        print("-" * 50)
        
        for step in all_path_steps[seq]:
            print_step_details(step)
    
    print(f"\nTotal number of safe sequences found: {len(all_safe_sequences)}")