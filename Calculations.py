import itertools
def findrange(vehlist):
    """
    Generate possible configurations for each vehicle in vehlist.
    Each configuration contains how many 5-person and 6-person groups fit in a vehicle.
    """
    return [
        [[x, (capacity - 5 * x) // 6] for x in range(capacity // 5 + 1) if (capacity - 5 * x) >= 0]
        for capacity in vehlist
    ]


def validlist(vehlist, required):
    """
    Find all valid combinations of groups (5-person and 6-person) that can fit in the vehicles.
    """
    ranges = findrange(vehlist)
    valid_combinations = []
    example_configs = []

    for combination in itertools.product(*ranges):
        sum_5 = sum(c[0] for c in combination)
        sum_6 = sum(c[1] for c in combination)

        if sum_5 >= required[0] and sum_6 >= required[1]:
            if [sum_5, sum_6] not in valid_combinations:
                valid_combinations.append([sum_5, sum_6])
                example_configs.append(combination)

    return [valid_combinations, example_configs]


def needed(vehlist, pers5, pers6):
    """
    Determine how many more 5-person and 6-person groups are required to meet the given need.
    """
    valid_data = validlist(vehlist, [0, 0])
    valid_combinations = valid_data[0]
    example_configs = valid_data[1]

    # Calculate shortfalls for each valid combination
    shortfalls = [
        [
            max(0, pers5 - valid_comb[0]),  # Shortfall of 5-person groups
            max(0, pers6 - valid_comb[1])  # Shortfall of 6-person groups
        ]
        for valid_comb in valid_combinations
    ]

    # Find the minimum shortfall
    min_shortfall = min(sum(shortfall) for shortfall in shortfalls)
    final_combinations = [
        (shortfall, example_configs[i])
        for i, shortfall in enumerate(shortfalls)
        if sum(shortfall) == min_shortfall
    ]

    # Extract results
    results = [comb[0] for comb in final_combinations]
    examples = [comb[1] for comb in final_combinations]

    return [results, examples]

def allocate_groups(vehicle_capacities, five_person_groups, six_person_groups, vers):
    vehicle_assignments=[]
    for i in range(len(vehicle_capacities)):
        vehicle_assignments.append([0,0])
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

    return [totals, vehicle_assignments,space_remaining]

def allocate_groups_simultaneous(vehicle_capacities, five_person_groups, six_person_groups):
    vehicle_assignments=[]
    for i in range(len(vehicle_capacities)):
        vehicle_assignments.append([0,0])
    totals = [0, 0]

    while five_person_groups > 0 or six_person_groups > 0:
        progress = False  # Track if any group was placed in this iteration

        for i, capacity in enumerate(vehicle_capacities):
            if capacity < 5:  # Skip if the vehicle has less than 5 capacity
                continue

            # Determine which group to place based on the smaller remainder
            remainder_6 = capacity % 6
            remainder_5 = capacity % 5

            if six_person_groups > 0 and (remainder_6 < remainder_5 or five_person_groups == 0):
                if capacity >= 6:
                    vehicle_assignments[i][1] += 1  # Place a 6-person group
                    totals[1] += 1
                    vehicle_capacities[i] -= 6
                    six_person_groups -= 1
                    progress = True
                    continue  # Move to the next vehicle after placing
            if five_person_groups > 0 and capacity >= 5:
                vehicle_assignments[i][0] += 1  # Place a 5-person group
                totals[0] += 1
                vehicle_capacities[i] -= 5
                five_person_groups -= 1
                progress = True
                continue  # Move to the next vehicle after placing

        if not progress:
            break
    space_remaining = vehicle_capacities.copy()

    return [totals, vehicle_assignments,space_remaining]
def closestalg(inlist,outlist):
    outcomp=[]
    final=[]
    offby=[]
    for output in outlist:
        outcomp.append(output[0])
    for elem in range(len(outcomp)):
        calc=[max(inlist[0]-outcomp[elem][0],0),max(inlist[1]-outcomp[elem][1],0)]
        offby.append(calc)
        final.append(sum(calc))
    outind=final.index(min(final))
    needed=offby[outind]
    best=outlist[outind]
    return [best,needed]


def spaces(examplelist, vehlist):
    """
    Calculate the remaining space in each vehicle after assigning groups.
    """
    return [
        capacity - (5 * config[0] + 6 * config[1])
        for capacity, config in zip(vehlist, examplelist)
    ]
