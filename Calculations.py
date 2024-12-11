import logging

logging.basicConfig(level=logging.DEBUG)

def validate_inputs(vehicle_capacities, five_person_groups, six_person_groups):
    if not all(isinstance(cap, int) and cap >= 0 for cap in vehicle_capacities):
        raise ValueError("Vehicle capacities must be a list of non-negative integers.")
    if not isinstance(five_person_groups, int) or five_person_groups < 0:
        raise ValueError("Five-person groups must be a non-negative integer.")
    if not isinstance(six_person_groups, int) or six_person_groups < 0:
        raise ValueError("Six-person groups must be a non-negative integer.")

def allocate_groups(vehicle_capacities, five_person_groups, six_person_groups, vers):
    validate_inputs(vehicle_capacities, five_person_groups, six_person_groups)

    vehicle_assignments = [[0, 0] for _ in vehicle_capacities]
    totals = [0, 0]

    if vers == 1:
        cap1, cap2 = 6, 5
        iter1, iter2 = six_person_groups, five_person_groups
    else:
        cap1, cap2 = 5, 6
        iter1, iter2 = five_person_groups, six_person_groups

    for _ in range(iter1):
        placed = False
        for i, capacity in enumerate(vehicle_capacities):
            if capacity >= cap1 and (capacity % cap1 <= capacity % cap2):
                vehicle_assignments[i][1] += 1
                totals[vers] += 1
                vehicle_capacities[i] -= cap1
                placed = True
                break
        if not placed:
            for i, capacity in enumerate(vehicle_capacities):
                if capacity >= cap1:
                    vehicle_assignments[i][1] += 1
                    totals[vers] += 1
                    vehicle_capacities[i] -= cap1
                    break
    for _ in range(iter2):
        for i, capacity in enumerate(vehicle_capacities):
            if capacity >= cap2:
                vehicle_assignments[i][0] += 1
                totals[vers == 0] += 1
                vehicle_capacities[i] -= cap2
                break

    space_remaining = vehicle_capacities.copy()
    return [totals, vehicle_assignments, space_remaining]

def allocate_groups_simultaneous(vehicle_capacities, five_person_groups, six_person_groups):
    """
    Allocate 5-person and 6-person groups simultaneously to vehicles for balanced allocation.

    Parameters:
    vehicle_capacities (list): List of vehicle capacities.
    five_person_groups (int): Number of 5-person groups to allocate.
    six_person_groups (int): Number of 6-person groups to allocate.

    Returns:
    list: [totals, vehicle_assignments, remaining_spaces]
    """
    vehicle_assignments = [[0, 0] for _ in vehicle_capacities]  # [5-person, 6-person]
    totals = [0, 0]  # Total [5-person groups, 6-person groups] assigned

    while five_person_groups > 0 or six_person_groups > 0:
        progress = False

        for i, capacity in enumerate(vehicle_capacities):
            if capacity < 5:  # Skip vehicles with insufficient capacity
                continue

            # Check whether to place a 6-person group or a 5-person group
            can_place_6 = capacity >= 6 and six_person_groups > 0
            can_place_5 = capacity >= 5 and five_person_groups > 0

            if can_place_6 and can_place_5:
                # Choose the group that minimizes remaining capacity
                if (capacity - 6) % 6 <= (capacity - 5) % 5:
                    # Place a 6-person group
                    vehicle_assignments[i][1] += 1
                    totals[1] += 1
                    vehicle_capacities[i] -= 6
                    six_person_groups -= 1
                else:
                    # Place a 5-person group
                    vehicle_assignments[i][0] += 1
                    totals[0] += 1
                    vehicle_capacities[i] -= 5
                    five_person_groups -= 1
                progress = True
            elif can_place_6:
                # Place a 6-person group if only it can fit
                vehicle_assignments[i][1] += 1
                totals[1] += 1
                vehicle_capacities[i] -= 6
                six_person_groups -= 1
                progress = True
            elif can_place_5:
                # Place a 5-person group if only it can fit
                vehicle_assignments[i][0] += 1
                totals[0] += 1
                vehicle_capacities[i] -= 5
                five_person_groups -= 1
                progress = True

        if not progress:
            # Stop if no groups can be placed
            break

    # Remaining space in each vehicle
    space_remaining = vehicle_capacities[:]

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

    # If there's a tie, choose the allocation with the most 6-person groups
    if len(best_indices) > 1:
        best_indices.sort(key=lambda i: allocations[i][0][1], reverse=True)  # Sort by 6-person groups

    # Return the best allocation
    best_index = best_indices[0]
    return [allocations[best_index], offby[best_index]]
