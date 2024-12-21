import logging

logging.basicConfig(level=logging.DEBUG)

def validate_inputs(vehicle_capacities, five_person_groups, six_person_groups):
    if not all(isinstance(cap, int) and cap >= 0 for cap in vehicle_capacities):
        raise ValueError("Vehicle capacities must be a list of non-negative integers.")
    if not isinstance(five_person_groups, int) or five_person_groups < 0:
        raise ValueError("Five-person groups must be a non-negative integer.")
    if not isinstance(six_person_groups, int) or six_person_groups < 0:
        raise ValueError("Six-person groups must be a non-negative integer.")

def allocate_groups(vehicle_capacities, five_person_groups, six_person_groups, vers, sort_order="none", minimize_remainder=False, fill_before_next=False):
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

    # Determine primary and secondary groups based on `vers`
    if vers == 1:
        primary_size, secondary_size = 6, 5
        primary_groups, secondary_groups = six_person_groups, five_person_groups
    else:
        primary_size, secondary_size = 5, 6
        primary_groups, secondary_groups = five_person_groups, six_person_groups

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

    def can_place_any_group():
        """Check if any group can still be placed in any vehicle."""
        for capacity in vehicle_capacities:
            if (primary_groups > 0 and capacity >= primary_size) or (secondary_groups > 0 and capacity >= secondary_size):
                return True
        return False

    current_vehicle = 0

    # Distribute primary and secondary groups
    while primary_groups > 0 or secondary_groups > 0:
        progress_in_iteration = False  # Track progress for the entire iteration

        if minimize_remainder:
            if fill_before_next:
                # Find the best vehicle and fill it
                best_vehicle_primary = find_best_vehicle(primary_size) if primary_groups > 0 else None
                best_vehicle_secondary = find_best_vehicle(secondary_size) if secondary_groups > 0 else None

                if best_vehicle_primary is not None and (best_vehicle_secondary is None or vehicle_capacities[best_vehicle_primary] % primary_size <= vehicle_capacities[best_vehicle_secondary] % secondary_size):
                    best_vehicle = best_vehicle_primary
                    group_size = primary_size
                elif best_vehicle_secondary is not None:
                    best_vehicle = best_vehicle_secondary
                    group_size = secondary_size
                else:
                    break

                # Fill the vehicle completely
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
                # Find the best vehicle and place one group
                best_vehicle_primary = find_best_vehicle(primary_size) if primary_groups > 0 else None
                best_vehicle_secondary = find_best_vehicle(secondary_size) if secondary_groups > 0 else None

                if best_vehicle_primary is not None and (best_vehicle_secondary is None or vehicle_capacities[best_vehicle_primary] % primary_size <= vehicle_capacities[best_vehicle_secondary] % secondary_size):
                    best_vehicle = best_vehicle_primary
                    group_size = primary_size
                elif best_vehicle_secondary is not None:
                    best_vehicle = best_vehicle_secondary
                    group_size = secondary_size
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
                # Sequentially fill each vehicle
                for current_vehicle in range(len(vehicle_capacities)):
                    while vehicle_capacities[current_vehicle] >= primary_size and primary_groups > 0:
                        vehicle_assignments[current_vehicle][primary_size == 6] += 1
                        totals[primary_size == 6] += 1
                        vehicle_capacities[current_vehicle] -= primary_size
                        primary_groups -= 1
                        progress_in_iteration = True

                    while vehicle_capacities[current_vehicle] >= secondary_size and secondary_groups > 0:
                        vehicle_assignments[current_vehicle][secondary_size == 6] += 1
                        totals[secondary_size == 6] += 1
                        vehicle_capacities[current_vehicle] -= secondary_size
                        secondary_groups -= 1
                        progress_in_iteration = True
            else:
                # Sequentially place one group per vehicle
                for current_vehicle in range(len(vehicle_capacities)):
                    if vehicle_capacities[current_vehicle] >= primary_size and primary_groups > 0:
                        group_size = primary_size
                    elif vehicle_capacities[current_vehicle] >= secondary_size and secondary_groups > 0:
                        group_size = secondary_size
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
            # Terminate if no progress is made in a full iteration
            break

    # Restore original order and prepare output
    space_remaining = list(vehicle_capacities)
    restored_order = sorted(zip(original_indices, vehicle_assignments, space_remaining), key=lambda x: x[0])
    vehicle_assignments = [x[1] for x in restored_order]
    space_remaining = [x[2] for x in restored_order]

    return [totals, vehicle_assignments, space_remaining]

def allocate_groups_simultaneous(vehicle_capacities, five_person_groups, six_person_groups, sort_order="none", minimize_remainder=False, fill_before_next=False):
    # Validate and sort vehicle capacities based on `sort_order`
    original_indices = list(range(len(vehicle_capacities)))
    if sort_order == "asc":
        sorted_data = sorted(zip(vehicle_capacities, original_indices))
        vehicle_capacities, original_indices = zip(*sorted_data)
    elif sort_order == "desc":
        sorted_data = sorted(zip(vehicle_capacities, original_indices), reverse=True)
        vehicle_capacities, original_indices = zip(*sorted_data)

    vehicle_capacities = list(vehicle_capacities)
    vehicle_assignments = [[0, 0] for _ in vehicle_capacities]  # [5-person, 6-person]
    totals = [0, 0]

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

    def can_place_any_group():
        """Check if any group can still be placed in any vehicle."""
        for capacity in vehicle_capacities:
            if (five_person_groups > 0 and capacity >= 5) or (six_person_groups > 0 and capacity >= 6):
                return True
        return False

    current_vehicle = 0

    # Distribute groups based on minimize_remainder and fill_before_next
    while five_person_groups > 0 or six_person_groups > 0:
        progress_in_iteration = False  # Track progress for the entire iteration

        if minimize_remainder:
            if fill_before_next:
                # Find the best vehicle and fill it
                best_vehicle_6 = find_best_vehicle(6) if six_person_groups > 0 else None
                best_vehicle_5 = find_best_vehicle(5) if five_person_groups > 0 else None

                if best_vehicle_6 is not None and (best_vehicle_5 is None or vehicle_capacities[best_vehicle_6] % 6 < vehicle_capacities[best_vehicle_5] % 5 or (vehicle_capacities[best_vehicle_6] % 6 == vehicle_capacities[best_vehicle_5] % 5)):
                    best_vehicle = best_vehicle_6
                    primary_group_size = 6
                    secondary_group_size = 5
                elif best_vehicle_5 is not None:
                    best_vehicle = best_vehicle_5
                    primary_group_size = 5
                    secondary_group_size = 6
                else:
                    break

                # Fill the vehicle completely
                while vehicle_capacities[best_vehicle] >= primary_group_size and (six_person_groups > 0 if primary_group_size == 6 else five_person_groups > 0):
                    vehicle_assignments[best_vehicle][primary_group_size == 6] += 1
                    totals[primary_group_size == 6] += 1
                    vehicle_capacities[best_vehicle] -= primary_group_size
                    if primary_group_size == 6:
                        six_person_groups -= 1
                    else:
                        five_person_groups -= 1
                    progress_in_iteration = True

                while vehicle_capacities[best_vehicle] >= secondary_group_size and (six_person_groups > 0 if secondary_group_size == 6 else five_person_groups > 0):
                    vehicle_assignments[best_vehicle][secondary_group_size == 6] += 1
                    totals[secondary_group_size == 6] += 1
                    vehicle_capacities[best_vehicle] -= secondary_group_size
                    if secondary_group_size == 6:
                        six_person_groups -= 1
                    else:
                        five_person_groups -= 1
                    progress_in_iteration = True
            else:
                # Find the best vehicle and place one group
                best_vehicle_6 = find_best_vehicle(6) if six_person_groups > 0 else None
                best_vehicle_5 = find_best_vehicle(5) if five_person_groups > 0 else None

                if best_vehicle_6 is not None and (best_vehicle_5 is None or vehicle_capacities[best_vehicle_6] % 6 < vehicle_capacities[best_vehicle_5] % 5 or (vehicle_capacities[best_vehicle_6] % 6 == vehicle_capacities[best_vehicle_5] % 5)):
                    best_vehicle = best_vehicle_6
                    group_size = 6
                elif best_vehicle_5 is not None:
                    best_vehicle = best_vehicle_5
                    group_size = 5
                else:
                    break

                if vehicle_capacities[best_vehicle] >= group_size:
                    vehicle_assignments[best_vehicle][group_size == 6] += 1
                    totals[group_size == 6] += 1
                    vehicle_capacities[best_vehicle] -= group_size
                    if group_size == 6:
                        six_person_groups -= 1
                    else:
                        five_person_groups -= 1
                    progress_in_iteration = True

        else:
            if fill_before_next:
                # Sequentially fill each vehicle
                for current_vehicle in range(len(vehicle_capacities)):
                    while vehicle_capacities[current_vehicle] >= 6 and six_person_groups > 0:
                        vehicle_assignments[current_vehicle][1] += 1
                        totals[1] += 1
                        vehicle_capacities[current_vehicle] -= 6
                        six_person_groups -= 1
                        progress_in_iteration = True

                    while vehicle_capacities[current_vehicle] >= 5 and five_person_groups > 0:
                        vehicle_assignments[current_vehicle][0] += 1
                        totals[0] += 1
                        vehicle_capacities[current_vehicle] -= 5
                        five_person_groups -= 1
                        progress_in_iteration = True
            else:
                # Sequentially place one group per vehicle
                for current_vehicle in range(len(vehicle_capacities)):
                    if vehicle_capacities[current_vehicle] >= 6 and six_person_groups > 0:
                        group_size = 6
                    elif vehicle_capacities[current_vehicle] >= 5 and five_person_groups > 0:
                        group_size = 5
                    else:
                        continue

                    if vehicle_capacities[current_vehicle] >= group_size:
                        vehicle_assignments[current_vehicle][group_size == 6] += 1
                        totals[group_size == 6] += 1
                        vehicle_capacities[current_vehicle] -= group_size
                        if group_size == 6:
                            six_person_groups -= 1
                        else:
                            five_person_groups -= 1
                        progress_in_iteration = True

        if not progress_in_iteration:
            # Terminate if no progress is made in a full iteration
            break

    # Restore original order and prepare output
    space_remaining = list(vehicle_capacities)
    restored_order = sorted(zip(original_indices, vehicle_assignments, space_remaining), key=lambda x: x[0])
    vehicle_assignments = [x[1] for x in restored_order]
    space_remaining = [x[2] for x in restored_order]

    return [totals, vehicle_assignments, space_remaining]



def closestalg(required_groups, allocations):
    offby = []
    total_shortfalls = []

    for allocation in allocations:
        shortfall = [
            max(0, required_groups[0] - allocation[0][0]),  # Shortfall of 5-person groups
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
            -allocations[i][0][1]  # Number of 6-person groups
        ))

    # Return the best allocation
    best_index = best_indices[0]
    return [allocations[best_index], offby[best_index]]

def sort_closestalg_output(closestalg_output):
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
        size = remaining_space + (5 * assignment[0]) + (6 * assignment[1])
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

def combine(sorted_output,shortfall):
    allocations=sorted_output[0]
    space=sorted_output[1]
    five=shortfall[0]
    six=shortfall[1]

    allocations0=[]
    space0=[]
    for i in range(len(space)):
        if space[i]!=0:
            allocations0.append(allocations[i])
            space0.append(space[i])
    used1=set()
    five1=five
    six1=six
    combos1=[]
    for bound in range(0,5):
        if five1==0 and six1==0:
            break
        for m in range(len(space0)):
            if five1==0 and six1==0:
                break
            for n in range(len(space0)-1,m,-1):
                if five1==0 and six1==0:
                    break
                if (space0[m]+space0[n]>=5) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (five1 or six1)>0 and (m not in used1) and (n not in used1):
                    if space0[m]+space0[n]>=6:
                        used1.add(m)
                        used1.add(n)
                        combos1.append([m+1,n+1])
                        six1-=1
                    elif space0[m]+space0[n]==5:
                        used1.add(m)
                        used1.add(n)
                        combos1.append([m+1,n+1])
                        five1-=1
    if five1==0 and six1==0:
        return combos1
    used2=set()
    five2=five
    six2=six
    combos2=[]
    for bound in range(0,5):
        if six2==0:
            break
        for m in range(len(space0)):
            if six2==0:
                break
            for n in range(len(space0)-1,m,-1):
                if six2==0:
                    break
                if (space0[m]+space0[n]>=6) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used2) and (n not in used2):
                    used2.add(m)
                    used2.add(n)
                    combos2.append([m+1,n+1])
                    six2-=1
    for bound in range(0,5):
        if five2==0:
            break
        for m in range(len(space0)):
            if five2==0:
                break
            for n in range(len(space0)-1,m,-1):
                if five2==0:
                    break
                if (space0[m]+space0[n]>=5) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used2) and (n not in used2):
                    used2.add(m)
                    used2.add(n)
                    combos2.append([m+1,n+1])
                    five2-=1
    if five2==0 and six2==0:
        return combos2
    for bound in range(0,5):
        used3=set()
        five3=five
        six3=six
        combos3=[]
        if five3==0 and six3==0:
            break
        for m in range(len(space0)):
            if five3==0 and six3==0:
                break
            for n in range(len(space0)-1,m,-1):
                if five3==0 and six3==0:
                    break
                if (space0[m]+space0[n]>=5) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (five3 or six3)>0 and (m not in used3) and (n not in used3):
                    if space0[m]+space0[n]>=6:
                        used3.add(m)
                        used3.add(n)
                        combos3.append([m+1,n+1])
                        six3-=1
                    elif space0[m]+space0[n]==5:
                        used3.add(m)
                        used3.add(n)
                        combos3.append([m+1,n+1])
                        five3-=1
    if five3==0 and six3==0:
        return combos3
    six4=six
    used4=set()
    combos4=[]
    five4=five
    for bound in range(0,5):
        if six4==0:
            break
        used4=set()
        six4=six
        combos4=[]
        for m in range(len(space0)):
            if six4==0:
                break
            for n in range(len(space0)-1,m,-1):
                if six4==0:
                    break
                if (space0[m]+space0[n]>=6) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used4) and (n not in used4):
                    used4.add(m)
                    used4.add(n)
                    combos4.append([m+1,n+1])
                    six4-=1
    for bound in range(0,5):
        if five4==0:
            break
        used5=used4
        five4=five
        combos5=combos4
        for m in range(len(space0)):
            if five4==0:
                break
            for n in range(len(space0)-1,m,-1):
                if five4==0:
                    break
                if (space0[m]+space0[n]>=5) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used5) and (n not in used5):
                    used5.add(m)
                    used5.add(n)
                    combos5.append([m+1,n+1])
                    five4-=1
    if five4==0 and six4==0:
        return combos5
    return []
out=[[[0,1],[1,1],[1,0],[0,0]],[4,3,3,1]]
short=[1,1]
print(combine(out,short))