from Combine import *
from Threes import *
from Twothree import *
from Allocations import *

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

def allalgs(allocations,spaces,shortfall,backupsize):
    round1=combine(allocations,spaces,shortfall,backupsize)
    if round1[1]:
        return round1[0],[],round1[2]
    else:
        round5=place3w2(shortfall.copy(),allocations,spaces,backupsize,1)
        if round5[1]:
            return [],round5[0],round5[3]
        elif round5[2]:
            return round5[0][0],round5[0][1],round5[0][2]
        else:
            short6=round5[0][1]
            used6=round5[0][2]
            round6=placingthrees(short6.copy(),used6.copy(),allocations,spaces,backupsize,1)
            if round6[1]:
                return [],round5[0][0]+round6[0],round5[0][2]+round6[3]
            elif round6[2]:
                return round6[0][0],round6[0][1]+round5[0][0],round6[0][2]+round5[0][3]
    return [],[],[]

def alltogether(pairs,threes,allist):
    al=pairs+threes
    i=zip(al,allist)
    out=[]
    for elem in enumerate(i):
        out.append(elem[1])
    return out

from more_itertools import set_partitions
def partitions(lst,n):
    return list(set_partitions(lst,n))

def sortpartitions(lists):
    # Define the sorting key
    def sort_key(sublist):
        # Length of the largest inner list
        max_inner_length = max(len(inner) for inner in sublist) if sublist else 0
        # Length of the parent sublist
        overall_length = len(sublist)
        return (max_inner_length, -overall_length)

    # Sort the list based on the custom key
    return sorted(lists, key=sort_key)
def assigntogether(pers5,pers6,pers7,vehicles0):
    indeces0=list(range(1,len(vehicles0)+1))
    combined = sorted(zip(vehicles0, indeces0),reverse=True, key=lambda x: x[0])
    vehicles, indeces = zip(*combined)
    vehicles=list(vehicles)
    indeces=list(indeces)

    backup_group = pers7 if pers7 != 0 else pers5
    backupsize = 5 if pers7 == 0 else 7
    primary_group = pers6
    use_backup = pers7 != 0

    allocations1 = []
    for priority in range(2):
        for order in [None, "asc", "desc"]:
            for opt2 in [False, True]:
                for opt1 in [False, True]:
                    allocations1.append(allocate_groups(
                        vehicles.copy(), backup_group, primary_group, priority, order, opt2, opt1, use_backup
                    ))

    for order in [None, "asc", "desc"]:
        for opt2 in [False, True]:
            for opt1 in [False, True]:
                allocations1.append(allocate_groups_simultaneous(
                    vehicles.copy(), backup_group, primary_group, order, opt2, opt1, use_backup
                ))

    results = closestalg([backup_group, pers6], allocations1,backupsize)
    sorted_allocations, sorted_spaces, sorted_sizes, number = sort_closestalg_output(results, backupsize)
    pairs,threes,listing=allalgs(sorted_allocations.copy(),sorted_spaces,results[1].copy(),backupsize)
    if pairs or threes:
        out1=pairs+threes
        out2=[]
        for elem in out1:
            if elem and len(elem)!=1:
                out2.append(elem)
        return out2

    for n in range(len(vehicles)//3,0,-1):
        partition=sortpartitions(partitions(vehicles,n))
        relative=sortpartitions(partitions(indeces,n))

        for elem1 in range(len(partition)):
            newvehicles=[]
            for elem2 in partition[elem1]:
                newvehicles.append(sum(elem2))
            allocations = []
            for priority in range(2):
                for order in [None, "asc", "desc"]:
                    for opt2 in [False, True]:
                        for opt1 in [False, True]:
                            allocations.append(allocate_groups(
                                newvehicles[:].copy(), backup_group, primary_group, priority, order, opt2, opt1, use_backup
                            ))

            for order in [None, "asc", "desc"]:
                for opt2 in [False, True]:
                    for opt1 in [False, True]:
                        allocations.append(allocate_groups_simultaneous(
                            newvehicles[:].copy(), backup_group, primary_group, order, opt2, opt1, use_backup
                        ))

            results = closestalg([backup_group, pers6], allocations,backupsize)
            if results[1][0]==0 and results[1][1]==0:
                for elem in relative[elem1]:
                    elem.sort()
                out=[]
                for item in relative[elem1]:
                    if len(item)!=1:
                        out.append(item)
                return out

    return []

def compute_ranges(people):
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

def compute_matrices(people,crews):
    pers5=-1*people+6*crews
    pers6=people-5*crews
    if pers5>=0 and pers6>=0 and isinstance(pers5,int) and isinstance(pers6,int):
        return pers5,pers6,0
    pers7=people-6*crews
    pers6n=-1*people+7*crews
    if pers7>=0 and pers6n>=0 and isinstance(pers7,int) and isinstance(pers6n,int):
        return 0,pers6n,pers7
    return []