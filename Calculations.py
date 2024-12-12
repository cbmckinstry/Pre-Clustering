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
    validate_inputs(vehicle_capacities, five_person_groups, six_person_groups)

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

    if vers == 1:
        primary_size, secondary_size = 6, 5
        primary_groups, secondary_groups = six_person_groups, five_person_groups
    else:
        primary_size, secondary_size = 5, 6
        primary_groups, secondary_groups = five_person_groups, six_person_groups

    # Function to distribute groups
    def distribute_groups_sequential(group_count, group_size, group_type, current_vehicle):
        progress = False
        best_choice = None

        for i in range(len(vehicle_capacities)):
            idx = (current_vehicle + i) % len(vehicle_capacities)
            if vehicle_capacities[idx] >= group_size:
                if minimize_remainder:
                    remainder = vehicle_capacities[idx] % group_size
                    if best_choice is None or remainder < best_choice[2]:
                        best_choice = (idx, group_size, remainder)
                else:
                    best_choice = (idx, group_size, 0)
                    if fill_before_next:
                        break

        if best_choice:
            vehicle_idx, group_size, _ = best_choice
            vehicle_assignments[vehicle_idx][group_type] += 1
            totals[group_type] += 1
            vehicle_capacities[vehicle_idx] -= group_size
            group_count -= 1
            progress = True
            if fill_before_next:
                current_vehicle = vehicle_idx
            else:
                current_vehicle = (vehicle_idx + 1) % len(vehicle_capacities)

        return group_count, progress, current_vehicle

    current_vehicle = 0

    # Distribute primary groups first
    while primary_groups > 0:
        primary_groups, progress, current_vehicle = distribute_groups_sequential(primary_groups, primary_size, primary_size == 6, current_vehicle)
        if not progress:
            break

    # Distribute secondary groups
    while secondary_groups > 0:
        secondary_groups, progress, current_vehicle = distribute_groups_sequential(secondary_groups, secondary_size, secondary_size == 6, current_vehicle)
        if not progress:
            break

    space_remaining = list(vehicle_capacities)
    restored_order = sorted(zip(original_indices, vehicle_assignments, space_remaining), key=lambda x: x[0])
    vehicle_assignments = [x[1] for x in restored_order]
    space_remaining = [x[2] for x in restored_order]

    return [totals, vehicle_assignments, space_remaining]

def allocate_groups_simultaneous(vehicle_capacities, five_person_groups, six_person_groups, sort_order="none", minimize_remainder=False, fill_before_next=False):
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

    current_vehicle = 0  # Start with the first vehicle

    while five_person_groups > 0 or six_person_groups > 0:
        progress = False

        if fill_before_next:
            # Start with the vehicle with the smallest remainder if minimize_remainder is True
            if minimize_remainder:
                current_vehicle = None
                smallest_remainder = float('inf')
                for i, capacity in enumerate(vehicle_capacities):
                    if capacity >= 5:
                        remainder_5 = capacity % 5 if five_person_groups > 0 else float('inf')
                        remainder_6 = capacity % 6 if six_person_groups > 0 else float('inf')
                        remainder = min(remainder_5, remainder_6)
                        if remainder < smallest_remainder:
                            smallest_remainder = remainder
                            current_vehicle = i
                if current_vehicle is None:
                    break

            # Fill the selected vehicle completely
            while vehicle_capacities[current_vehicle] >= 5 and (five_person_groups > 0 or six_person_groups > 0):
                remainder_5 = vehicle_capacities[current_vehicle] % 5 if five_person_groups > 0 else float('inf')
                remainder_6 = vehicle_capacities[current_vehicle] % 6 if six_person_groups > 0 else float('inf')

                if remainder_6 <= remainder_5 and six_person_groups > 0 and vehicle_capacities[current_vehicle] >= 6:
                    vehicle_assignments[current_vehicle][1] += 1
                    totals[1] += 1
                    vehicle_capacities[current_vehicle] -= 6
                    six_person_groups -= 1
                elif five_person_groups > 0 and vehicle_capacities[current_vehicle] >= 5:
                    vehicle_assignments[current_vehicle][0] += 1
                    totals[0] += 1
                    vehicle_capacities[current_vehicle] -= 5
                    five_person_groups -= 1
                else:
                    break

            current_vehicle = (current_vehicle + 1) % len(vehicle_capacities)  # Move to the next vehicle
        else:
            # Evaluate all vehicles for best choice
            best_choice = None
            for i, capacity in enumerate(vehicle_capacities):
                if capacity < 5:
                    continue

                if minimize_remainder:
                    # Check remainder for placing a 6-person group
                    if capacity >= 6 and six_person_groups > 0:
                        remainder_6 = capacity % 6
                        if best_choice is None or remainder_6 < best_choice[2]:
                            best_choice = (i, 6, remainder_6)

                    # Check remainder for placing a 5-person group
                    if capacity >= 5 and five_person_groups > 0:
                        remainder_5 = capacity % 5
                        if best_choice is None or remainder_5 < best_choice[2]:
                            best_choice = (i, 5, remainder_5)
                else:
                    can_place_6 = capacity >= 6 and six_person_groups > 0
                    can_place_5 = capacity >= 5 and five_person_groups > 0

                    if can_place_6 and can_place_5:
                        if (capacity - 6) % 6 <= (capacity - 5) % 5:
                            best_choice = (i, 6, (capacity - 6) % 6)
                        else:
                            best_choice = (i, 5, (capacity - 5) % 5)
                    elif can_place_6:
                        best_choice = (i, 6, (capacity - 6) % 6)
                    elif can_place_5:
                        best_choice = (i, 5, (capacity - 5) % 5)

            if best_choice:
                vehicle_idx, group_size, _ = best_choice
                if group_size == 6:
                    vehicle_assignments[vehicle_idx][1] += 1
                    totals[1] += 1
                    vehicle_capacities[vehicle_idx] -= 6
                    six_person_groups -= 1
                else:
                    vehicle_assignments[vehicle_idx][0] += 1
                    totals[0] += 1
                    vehicle_capacities[vehicle_idx] -= 5
                    five_person_groups -= 1

                progress = True

            if not progress:
                break

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
