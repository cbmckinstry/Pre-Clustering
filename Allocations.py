def allocate_groups(vehicle_capacities, backup_groups, six_person_groups, vers, sort_order="none", minimize_remainder=False, fill_before_next=False, switch_to_seven=False):
    # Validate inputs
    original_indices = list(range(len(vehicle_capacities)))

    # Apply sorting based on `sort_order`
    if sort_order == "asc":
        sorted_data = sorted(zip(vehicle_capacities, original_indices))
        vehicle_capacities, original_indices = zip(*sorted_data)
    elif sort_order == "desc":
        sorted_data = sorted(zip(vehicle_capacities, original_indices), reverse=True)
        vehicle_capacities, original_indices = zip(*sorted_data)

    vehicle_capacities = list(vehicle_capacities)
    vehicle_assignments = [[0, 0] for _ in vehicle_capacities]
    totals = [0, 0]

    # Adjust group sizes based on `switch_to_seven`
    backup_size = 7 if switch_to_seven else 5
    if vers == 1:
        primary_size, primary_groups, secondary_groups = 6, six_person_groups, backup_groups
    else:
        primary_size, primary_groups, secondary_groups, backup_size = backup_size, backup_groups, six_person_groups,6

    # Function to find the best vehicle based on remainder
    def find_best_vehicle(group_size):
        best_vehicle = None
        smallest_remainder = float('inf')

        for i, capacity in enumerate(vehicle_capacities):
            if capacity >= group_size:
                remainder = capacity % group_size
                if remainder < smallest_remainder:
                    smallest_remainder = remainder
                    best_vehicle = i

        return best_vehicle

    # Distribute primary and backup groups
    while primary_groups > 0 or secondary_groups > 0:
        progress_in_iteration = False

        if minimize_remainder:
            if fill_before_next:
                # Minimize remainder and fill vehicles
                best_vehicle_primary = find_best_vehicle(primary_size) if primary_groups > 0 else None
                best_vehicle_secondary = find_best_vehicle(backup_size) if secondary_groups > 0 else None
                if best_vehicle_primary is not None and (best_vehicle_secondary is None or vehicle_capacities[best_vehicle_primary] % primary_size <= vehicle_capacities[best_vehicle_secondary] % backup_size):
                    best_vehicle = best_vehicle_primary
                    group_size = primary_size
                elif best_vehicle_secondary is not None:
                    best_vehicle = best_vehicle_secondary
                    group_size = backup_size
                else:
                    break

                while vehicle_capacities[best_vehicle] >= group_size and (primary_groups > 0 if group_size == primary_size else secondary_groups > 0):
                    vehicle_assignments[best_vehicle][group_size == 6] += 1
                    totals[group_size == 6] += 1
                    vehicle_capacities[best_vehicle] -= group_size
                    if group_size == primary_size:
                        primary_groups -= 1
                    else:
                        secondary_groups -= 1
                    progress_in_iteration = True
            else:

                # Place one group based on remainder minimization
                best_vehicle_primary = find_best_vehicle(primary_size) if primary_groups > 0 else None
                best_vehicle_secondary = find_best_vehicle(backup_size) if secondary_groups > 0 else None
                if best_vehicle_primary is not None and (best_vehicle_secondary is None or vehicle_capacities[best_vehicle_primary] % primary_size <= vehicle_capacities[best_vehicle_secondary] % backup_size):
                    best_vehicle = best_vehicle_primary
                    group_size = primary_size
                elif best_vehicle_secondary is not None:
                    best_vehicle = best_vehicle_secondary
                    group_size = backup_size
                else:
                    break

                if vehicle_capacities[best_vehicle] >= group_size:
                    vehicle_assignments[best_vehicle][group_size == 6] += 1
                    totals[group_size == 6] += 1
                    vehicle_capacities[best_vehicle] -= group_size
                    if group_size == primary_size:
                        primary_groups -= 1
                    else:
                        secondary_groups -= 1
                    progress_in_iteration = True
        else:
            if fill_before_next:
                for current_vehicle in range(len(vehicle_capacities)):
                    while vehicle_capacities[current_vehicle] >= primary_size and primary_groups > 0:
                        vehicle_assignments[current_vehicle][primary_size == 6] += 1
                        totals[primary_size == 6] += 1
                        vehicle_capacities[current_vehicle] -= primary_size
                        primary_groups -= 1
                        progress_in_iteration = True

                    while vehicle_capacities[current_vehicle] >= backup_size and secondary_groups > 0:
                        vehicle_assignments[current_vehicle][backup_size == 6] += 1
                        totals[backup_size == 6] += 1
                        vehicle_capacities[current_vehicle] -= backup_size
                        secondary_groups -= 1
                        progress_in_iteration = True
            else:
                for current_vehicle in range(len(vehicle_capacities)):
                    if vehicle_capacities[current_vehicle] >= primary_size and primary_groups > 0:
                        group_size = primary_size
                    elif vehicle_capacities[current_vehicle] >= backup_size and secondary_groups > 0:
                        group_size = backup_size
                    else:
                        continue

                    if vehicle_capacities[current_vehicle] >= group_size:
                        vehicle_assignments[current_vehicle][group_size == 6] += 1
                        totals[group_size == 6] += 1
                        vehicle_capacities[current_vehicle] -= group_size
                        if group_size == primary_size:
                            primary_groups -= 1
                        else:
                            secondary_groups -= 1
                        progress_in_iteration = True

        if not progress_in_iteration:
            break

    space_remaining = list(vehicle_capacities)
    restored_order = sorted(zip(original_indices, vehicle_assignments, space_remaining), key=lambda x: x[0])
    vehicle_assignments = [x[1] for x in restored_order]
    space_remaining = [x[2] for x in restored_order]

    return [totals, vehicle_assignments, space_remaining]


def allocate_groups_simultaneous(vehicle_capacities, backup_groups, six_person_groups, sort_order="none", minimize_remainder=False, fill_before_next=False, switch_to_seven=False):
    original_indices = list(range(len(vehicle_capacities)))

    if sort_order == "asc":
        sorted_data = sorted(zip(vehicle_capacities, original_indices))
        vehicle_capacities, original_indices = zip(*sorted_data)
    elif sort_order == "desc":
        sorted_data = sorted(zip(vehicle_capacities, original_indices), reverse=True)
        vehicle_capacities, original_indices = zip(*sorted_data)

    vehicle_capacities = list(vehicle_capacities)
    vehicle_assignments = [[0, 0] for _ in vehicle_capacities]
    totals = [0, 0]

    backup_size = 7 if switch_to_seven else 5

    def find_best_vehicle(group_size):
        best_vehicle = None
        smallest_remainder = float('inf')

        for i, capacity in enumerate(vehicle_capacities):
            if capacity >= group_size:
                remainder = capacity % group_size
                if remainder < smallest_remainder:
                    smallest_remainder = remainder
                    best_vehicle = i

        return best_vehicle

    while backup_groups > 0 or six_person_groups > 0:
        progress_in_iteration = False

        if minimize_remainder:
            if fill_before_next:
                best_vehicle_6 = find_best_vehicle(6) if six_person_groups > 0 else None
                best_vehicle_backup = find_best_vehicle(backup_size) if backup_groups > 0 else None

                if best_vehicle_6 is not None and (best_vehicle_backup is None or vehicle_capacities[best_vehicle_6] % 6 <= vehicle_capacities[best_vehicle_backup] % backup_size):
                    best_vehicle = best_vehicle_6
                    group_size = 6
                elif best_vehicle_backup is not None:
                    best_vehicle = best_vehicle_backup
                    group_size = backup_size
                else:
                    break

                while vehicle_capacities[best_vehicle] >= group_size and (six_person_groups > 0 if group_size == 6 else backup_groups > 0):
                    vehicle_assignments[best_vehicle][group_size == 6] += 1
                    totals[group_size == 6] += 1
                    vehicle_capacities[best_vehicle] -= group_size
                    if group_size == 6:
                        six_person_groups -= 1
                    else:
                        backup_groups -= 1
                    progress_in_iteration = True
            else:
                best_vehicle_6 = find_best_vehicle(6) if six_person_groups > 0 else None
                best_vehicle_backup = find_best_vehicle(backup_size) if backup_groups > 0 else None

                if best_vehicle_6 is not None and (best_vehicle_backup is None or vehicle_capacities[best_vehicle_6] % 6 <= vehicle_capacities[best_vehicle_backup] % backup_size):
                    best_vehicle = best_vehicle_6
                    group_size = 6
                elif best_vehicle_backup is not None:
                    best_vehicle = best_vehicle_backup
                    group_size = backup_size
                else:
                    break

                if vehicle_capacities[best_vehicle] >= group_size:
                    vehicle_assignments[best_vehicle][group_size == 6] += 1
                    totals[group_size == 6] += 1
                    vehicle_capacities[best_vehicle] -= group_size
                    if group_size == 6:
                        six_person_groups -= 1
                    else:
                        backup_groups -= 1
                    progress_in_iteration = True
        else:
            if fill_before_next:
                for current_vehicle in range(len(vehicle_capacities)):
                    while vehicle_capacities[current_vehicle] >= 6 and six_person_groups > 0:
                        vehicle_assignments[current_vehicle][1] += 1
                        totals[1] += 1
                        vehicle_capacities[current_vehicle] -= 6
                        six_person_groups -= 1
                        progress_in_iteration = True

                    while vehicle_capacities[current_vehicle] >= backup_size and backup_groups > 0:
                        vehicle_assignments[current_vehicle][0] += 1
                        totals[0] += 1
                        vehicle_capacities[current_vehicle] -= backup_size
                        backup_groups -= 1
                        progress_in_iteration = True
            else:
                for current_vehicle in range(len(vehicle_capacities)):
                    if vehicle_capacities[current_vehicle] >= 6 and six_person_groups > 0:
                        group_size = 6
                    elif vehicle_capacities[current_vehicle] >= backup_size and backup_groups > 0:
                        group_size = backup_size
                    else:
                        continue

                    if vehicle_capacities[current_vehicle] >= group_size:
                        vehicle_assignments[current_vehicle][group_size == 6] += 1
                        totals[group_size == 6] += 1
                        vehicle_capacities[current_vehicle] -= group_size
                        if group_size == 6:
                            six_person_groups -= 1
                        else:
                            backup_groups -= 1
                        progress_in_iteration = True

        if not progress_in_iteration:
            break

    space_remaining = list(vehicle_capacities)
    restored_order = sorted(zip(original_indices, vehicle_assignments, space_remaining), key=lambda x: x[0])
    vehicle_assignments = [x[1] for x in restored_order]
    space_remaining = [x[2] for x in restored_order]

    return [totals, vehicle_assignments, space_remaining]

def closestalg(required_groups, allocations,backupsize=5):
    offby = []
    total_shortfalls = []

    for allocation in allocations:
        shortfall = [
            max(0, required_groups[0] - allocation[0][0]),  # Shortfall of backup groups
            max(0, required_groups[1] - allocation[0][1])   # Shortfall of 6-person groups
        ]
        offby.append(shortfall)
        total_shortfalls.append(sum(shortfall))

    # Find the minimum shortfall
    min_shortfall = min(total_shortfalls)
    best_indices = [i for i, total in enumerate(total_shortfalls) if total == min_shortfall]

    # If there's a tie, choose the allocation with the fewest vehicles with nonzero remaining capacity
    if len(best_indices) > 1:
        best_indices.sort(key=lambda i: (
            len([cap for cap in allocations[i][2] if cap > 0]),  # Number of vehicles with remaining capacity
            -allocations[i][0][backupsize==5]  # Number of larger groups
        ))

    # Return the best allocation
    best_index = best_indices[0]
    return [allocations[best_index], offby[best_index]]

def sort_closestalg_output(closestalg_output,backup):
    # Safely extract the allocation details
    try:
        allocation = closestalg_output[0]  # First element contains totals, allocations, and remaining spaces
        remaining_spaces = allocation[2]   # Remaining spaces in vehicles
        allocations = allocation[1]        # Group allocations (5-person, 6-person)
    except (IndexError, TypeError, ValueError) as e:
        raise ValueError("Invalid closestalg_output structure") from e

    # Calculate vehicle sizes dynamically
    vehicle_sizes = []
    for remaining_space, assignment in zip(remaining_spaces, allocations):
        size = remaining_space + (backup * assignment[0]) + (6 * assignment[1])
        vehicle_sizes.append(size)

    # Combine sizes, allocations, and remaining spaces into a list of tuples
    combined_data = []
    for i in range(len(remaining_spaces)):
        combined_data.append((vehicle_sizes[i], allocations[i], remaining_spaces[i]))

    # Sort the combined data by remaining spaces in descending order
    combined_data.sort(key=lambda x: x[2], reverse=True)

    # Separate the sorted data into three lists
    sorted_sizes = [entry[0] for entry in combined_data]
    sorted_allocations = [entry[1] for entry in combined_data]
    sorted_remaining_spaces = [entry[2] for entry in combined_data]
    number=[]
    for i in range(len(sorted_sizes)):
        number.append(i+1)

    return sorted_allocations, sorted_remaining_spaces, sorted_sizes, number

