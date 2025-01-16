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
        return round1[0],[]
    else:
        round5=place3w2(shortfall.copy(),allocations,spaces,backupsize,1)
        if round5[1]:
            return [],round5[0]
        elif round5[2]:
            return round5[0][0],round5[0][1]
        else:
            short6=round5[0][1]
            used6=round5[0][2]
            round6=combine(allocations,spaces,short6.copy(),backupsize,used6.copy())
            if round6[1]:
                return round6[0],round5[0][0]
            else:
                short7=round6[0][1]
                used7=round6[0][2]
                round7=placingthrees(short7.copy(),used7.copy(),allocations,spaces,backupsize)
                if round7:
                    return round6[0][0],round7+round5[0][0]
    return [],[]
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
