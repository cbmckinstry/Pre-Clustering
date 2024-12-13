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
