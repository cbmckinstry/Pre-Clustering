import logging

logging.basicConfig(level=logging.DEBUG)

def validate_inputs(vehicle_capacities, five_person_groups, six_person_groups, seven_person_groups):
    if not all(isinstance(cap, int) and cap >= 0 for cap in vehicle_capacities):
        raise ValueError("Vehicle capacities must be a list of non-negative integers.")
    if not isinstance(five_person_groups, int) or five_person_groups < 0:
        raise ValueError("Five-person groups must be a non-negative integer.")
    if not isinstance(six_person_groups, int) or six_person_groups < 0:
        raise ValueError("Six-person groups must be a non-negative integer.")
    if not isinstance(seven_person_groups, int) or seven_person_groups < 0:
        raise ValueError("Seven-person groups must be a non-negative integer.")
    if seven_person_groups!=0 and five_person_groups!=0:
        raise ValueError("There cannot be both 5 and 7 person crews")

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

    # Check if any group can be placed
    def can_place_any_group():
        for capacity in vehicle_capacities:
            if (primary_groups > 0 and capacity >= primary_size) or (secondary_groups > 0 and capacity >= backup_size):
                return True
        return False

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
                    vehicle_assignments[best_vehicle][group_size == primary_size] += 1
                    totals[group_size == primary_size] += 1
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
                    vehicle_assignments[best_vehicle][group_size == primary_size] += 1
                    totals[group_size == primary_size] += 1
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

def combine(sorted_output,shortfall,upperbound,backup_size=5):
    allocations=sorted_output[0]
    space=sorted_output[1]
    backup=shortfall[0]
    six=shortfall[1]

    allocations0=[]
    space0=[]
    for i in range(len(space)):
        if space[i]!=0:
            allocations0.append(allocations[i])
            space0.append(space[i])
    used1=set()
    backup1=backup
    six1=six
    combos1=[]
    for bound in range(0,upperbound):
        if backup1==0 and six1==0:
            break
        for m in range(len(space0)):
            if backup1==0 and six1==0:
                break
            for n in range(len(space0)-1,m,-1):
                if backup1==0 and six1==0:
                    break
                if (space0[m]+space0[n]>=min(backup_size,6)) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (backup1 or six1)>0 and (m not in used1) and (n not in used1):
                    if space0[m]+space0[n]>=7 and backup1>0 and backup_size==7:
                        used1.add(m)
                        used1.add(n)
                        combos1.append([m+1,n+1])
                        backup1-=1
                    elif space0[m]+space0[n]>=6 and six1>0:
                        used1.add(m)
                        used1.add(n)
                        combos1.append([m+1,n+1])
                        six1-=1
                    elif space0[m]+space0[n]>=5 and backup1>0 and backup_size==5:
                        used1.add(m)
                        used1.add(n)
                        combos1.append([m+1,n+1])
                        backup1-=1
    if backup1==0 and six1==0:
        return combos1
    used2=set()
    backup2=backup
    six2=six
    combos2=[]
    if backup_size==7:
        for bound in range(0,upperbound):
            if backup2==0:
                break
            for m in range(len(space0)):
                if backup2==0:
                    break
                for n in range(len(space0)-1,m,-1):
                    if backup2==0:
                        break
                    if (space0[m]+space0[n]>=7) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used2) and (n not in used2):
                        used2.add(m)
                        used2.add(n)
                        combos2.append([m+1,n+1])
                        backup2-=1
    for bound in range(0,upperbound):
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
    if backup_size==5:
        for bound in range(0,upperbound):
            if backup2==0:
                break
            for m in range(len(space0)):
                if backup2==0:
                    break
                for n in range(len(space0)-1,m,-1):
                    if backup2==0:
                        break
                    if (space0[m]+space0[n]>=5) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used2) and (n not in used2):
                        used2.add(m)
                        used2.add(n)
                        combos2.append([m+1,n+1])
                        backup2-=1
    if backup2==0 and six2==0:
        return combos2
    used3=set()
    backup3=backup
    six3=six
    combos3=[]
    for bound in range(0,upperbound):
        used3=set()
        backup3=backup
        six3=six
        combos3=[]
        if backup3==0 and six3==0:
            break
        for m in range(len(space0)):
            if backup3==0 and six3==0:
                break
            for n in range(len(space0)-1,m,-1):
                if backup3==0 and six3==0:
                    break
                if (space0[m]+space0[n]>=min(backup_size,6)) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (backup3 or six3)>0 and (m not in used3) and (n not in used3):
                    if space0[m]+space0[n]>=7 and backup3>0 and backup_size==7:
                        used3.add(m)
                        used3.add(n)
                        combos3.append([m+1,n+1])
                        backup3-=1
                    elif space0[m]+space0[n]>=6 and six3>0:
                        used3.add(m)
                        used3.add(n)
                        combos3.append([m+1,n+1])
                        six3-=1
                    elif space0[m]+space0[n]>=5 and backup3>0 and backup_size==5:
                        used3.add(m)
                        used3.add(n)
                        combos3.append([m+1,n+1])
                        backup3-=1
    if backup3==0 and six3==0:
        return combos3

    six4=six
    used4=set()
    combos4=[]
    backup4=backup
    if backup_size==7:
        for bound in range(0,upperbound):
            if backup4==0:
                break
            used4=set()
            backup4=backup
            combos4=[]
            for m in range(len(space0)):
                if backup4==0:
                    break
                for n in range(len(space0)-1,m,-1):
                    if backup4==0:
                        break
                    if (space0[m]+space0[n]>=7) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used4) and (n not in used4):
                        used4.add(m)
                        used4.add(n)
                        combos4.append([m+1,n+1])
                        backup4-=1
        combos5=combos4
        used5=used4
        for bound in range(0,upperbound):
            if six4==0:
                break
            used5=used4
            six4=six
            combos5=combos4
            for m in range(len(space0)):
                if six4==0:
                    break
                for n in range(len(space0)-1,m,-1):
                    if six4==0:
                        break
                    if (space0[m]+space0[n]>=6) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used5) and (n not in used5):
                        used5.add(m)
                        used5.add(n)
                        combos5.append([m+1,n+1])
                        six4-=1
    else:
        for bound in range(0,upperbound):
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
        combos5=combos4
        used5=used4
        for bound in range(0,upperbound):
            if backup4==0:
                break
            used5=used4
            backup4=backup
            combos5=combos4
            for m in range(len(space0)):
                if backup4==0:
                    break
                for n in range(len(space0)-1,m,-1):
                    if backup4==0:
                        break
                    if (space0[m]+space0[n]>=5) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used5) and (n not in used5):
                        used5.add(m)
                        used5.add(n)
                        combos5.append([m+1,n+1])
                        backup4-=1
    if backup4==0 and six4==0:
        return combos5
    return []

def bestone(sorted_output,shortfall,upper,backup_size=5):
    for x in range(1,upper):
        y=combine(sorted_output,shortfall,x,backup_size)
        if y:
            return y

def ranges(people):
    final=[]
    counter1=0
    people1=people
    final1=[]
    while people1>=0:
        if people1%6==0:
            final1.append(counter1+(people1//6))
        counter1+=1
        people1-=5
    counter2=0
    people2=people
    final2=[]
    while people2>=0:
        if people2%6==0:
            final2.append(counter2+(people2//6))
        counter2+=1
        people2-=7
    if final1:
        final.append([min(final1),max(final1)])
    else:
        final.append([])
    if final2:
        final.append([min(final2),max(final2)])
    else:
        final.append([])
    return final

def matrices(people,crews):
    pers5=-1*people+6*crews
    pers6=people-5*crews
    if pers5>=0 and pers6>=0 and isinstance(pers5,int) and isinstance(pers6,int):
        return pers5,pers6,0
    pers7=people-6*crews
    pers6n=-1*people+7*crews
    if pers7>=0 and pers6n>=0 and isinstance(pers7,int) and isinstance(pers6n,int):
        return 0,pers6n,pers7
    return []