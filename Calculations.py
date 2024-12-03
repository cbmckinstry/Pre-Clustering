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


def spaces(examplelist, vehlist):
    """
    Calculate the remaining space in each vehicle after assigning groups.
    """
    return [
        capacity - (5 * config[0] + 6 * config[1])
        for capacity, config in zip(vehlist, examplelist)
    ]