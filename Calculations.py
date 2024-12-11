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

    vehicle_assignments = [[0, 0] for _ in vehicle_capacities]  # [5-person, 6-person]
    totals = [0, 0]  # Total [5-person, 6-person] groups assigned

    # Set primary and secondary group sizes based on `vers`
    if vers == 1:
        primary_size, secondary_size = 6, 5
        primary_groups, secondary_groups = six_person_groups, five_person_groups
    else:
        primary_size, secondary_size = 5, 6
        primary_groups, secondary_groups = five_person_groups, six_person_groups

    # Distribute primary groups evenly across vehicles
    while primary_groups > 0:
        progress = False
        for i, capacity in enumerate(vehicle_capacities):
            if primary_groups > 0 and capacity >= primary_size:
                vehicle_assignments[i][primary_size == 6] += 1
                totals[primary_size == 6] += 1
                vehicle_capacities[i] -= primary_size
                primary_groups -= 1
                progress = True

        if not progress:
            # Break if no more groups can be placed
            break

    # Distribute secondary groups evenly across vehicles
    while secondary_groups > 0:
        progress = False
        for i, capacity in enumerate(vehicle_capacities):
            if secondary_groups > 0 and capacity >= secondary_size:
                vehicle_assignments[i][secondary_size == 6] += 1
                totals[secondary_size == 6] += 1
                vehicle_capacities[i] -= secondary_size
                secondary_groups -= 1
                progress = True

        if not progress:
            # Break if no more groups can be placed
            break

    # Remaining space in each vehicle
    space_remaining = vehicle_capacities[:]

    return [totals, vehicle_assignments, space_remaining]

def allocate_groups_simultaneous(vehicle_capacities, five_person_groups, six_person_groups):
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
capacity=[23, 12, 14, 15, 11, 7, 7, 8, 5, 5]
cap1=capacity.copy()
cap2=capacity.copy()
cap3=capacity.copy()
cap4=capacity.copy()
cap5=capacity.copy()
cap6=capacity.copy()
five=5
six=13
print(allocate_groups(cap1,five,six,0))
print(allocate_groups(cap2,five,six,1))
print(allocate_groups_simultaneous(cap5,five,six))
