import logging

logging.basicConfig(level=logging.DEBUG)

def validate_inputs(vehicle_capacities, five_person_groups, six_person_groups):
    if not all(isinstance(cap, int) and cap >= 0 for cap in vehicle_capacities):
        raise ValueError("Vehicle capacities must be a list of non-negative integers.")
    if not isinstance(five_person_groups, int) or five_person_groups < 0:
        raise ValueError("Five-person groups must be a non-negative integer.")
    if not isinstance(six_person_groups, int) or six_person_groups < 0:
        raise ValueError("Six-person groups must be a non-negative integer.")

def allocate_groups(vehicle_capacities, five_person_groups, six_person_groups, vers, sort_order="none", fill_before_next=False):
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
    def distribute_groups(group_count, group_size, index_list):
        progress = False
        for i in index_list:
            if group_count > 0 and vehicle_capacities[i] >= group_size:
                vehicle_assignments[i][group_size == 6] += 1
                totals[group_size == 6] += 1
                vehicle_capacities[i] -= group_size
                group_count -= 1
                progress = True
                if fill_before_next:
                    # Break early to focus on one vehicle
                    break
        return group_count, progress

    vehicle_indices = list(range(len(vehicle_capacities)))

    # Distribute primary groups
    while primary_groups > 0:
        primary_groups, progress = distribute_groups(primary_groups, primary_size, vehicle_indices)
        if not progress:
            break

    # Distribute secondary groups
    while secondary_groups > 0:
        secondary_groups, progress = distribute_groups(secondary_groups, secondary_size, vehicle_indices)
        if not progress:
            break

    space_remaining = list(vehicle_capacities)
    restored_order = sorted(zip(original_indices, vehicle_assignments, space_remaining), key=lambda x: x[0])
    vehicle_assignments = [x[1] for x in restored_order]
    space_remaining = [x[2] for x in restored_order]

    return [totals, vehicle_assignments, space_remaining]

def allocate_groups_simultaneous(vehicle_capacities, five_person_groups, six_person_groups, sort_order="none", fill_before_next=False):
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

    vehicle_indices = list(range(len(vehicle_capacities)))

    while five_person_groups > 0 or six_person_groups > 0:
        progress = False

        for i in vehicle_indices:
            if vehicle_capacities[i] < 5:
                continue

            can_place_6 = vehicle_capacities[i] >= 6 and six_person_groups > 0
            can_place_5 = vehicle_capacities[i] >= 5 and five_person_groups > 0

            if can_place_6 and can_place_5:
                if (vehicle_capacities[i] - 6) % 6 <= (vehicle_capacities[i] - 5) % 5:
                    vehicle_assignments[i][1] += 1
                    totals[1] += 1
                    vehicle_capacities[i] -= 6
                    six_person_groups -= 1
                else:
                    vehicle_assignments[i][0] += 1
                    totals[0] += 1
                    vehicle_capacities[i] -= 5
                    five_person_groups -= 1
                progress = True
                if fill_before_next:
                    break
            elif can_place_6:
                vehicle_assignments[i][1] += 1
                totals[1] += 1
                vehicle_capacities[i] -= 6
                six_person_groups -= 1
                progress = True
                if fill_before_next:
                    break
            elif can_place_5:
                vehicle_assignments[i][0] += 1
                totals[0] += 1
                vehicle_capacities[i] -= 5
                five_person_groups -= 1
                progress = True
                if fill_before_next:
                    break

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

    # If there's a tie, choose the allocation with the most 6-person groups
    if len(best_indices) > 1:
        best_indices.sort(key=lambda i: allocations[i][0][1], reverse=True)  # Sort by 6-person groups

    # Return the best allocation
    best_index = best_indices[0]
    return [allocations[best_index], offby[best_index]]
