from Combine import *
def place3w2(shortfall,allocations1,spaces1,backupsize=5,param=0,upperbound=9):
    allocations=[]
    spaces=[]
    for i in range(len(spaces1)):
        if spaces1[i]!=0:
            allocations.append(allocations1[i])
            spaces.append(spaces1[i])

    six6=shortfall[1]
    backup6=shortfall[0]
    used6=set()
    threes6=[]
    init=[]
    init2=[]
    for m in range(upperbound):
        six6=shortfall[1]
        backup6=shortfall[0]
        used6=set()
        threes6=[]
        init=[]
        for i in range(0,len(spaces)-2):
            if six6==0 and backup6==0:
                break
            for j in range(len(spaces)-1,i+1,-1):
                if six6==0 and backup6==0:
                    break
                for k in range(j-1,i,-1):
                    if six6==0 and backup6==0:
                        break
                    if (i not in used6 and j not in used6 and k not in used6) and spaces[i]+spaces[k]+spaces[j]>=(2*max(backupsize,6)) and (six6>0 or backup6>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<m:
                        if spaces[i]+spaces[k]+spaces[j]>=(2*max(backupsize,6)):
                            if backupsize==7 and backup6>=2:
                                backup6-=2
                                used6.update([i,j,k])
                                threes6.append([i+1,k+1,j+1])
                                init.append([2,0])
                            elif backupsize==5 and six6>=2:
                                six6-=2
                                used6.update([i,j,k])
                                threes6.append([i+1,k+1,j+1])
                                init.append([0,2])
                            if param==1:
                                trial=combine(allocations,spaces,[backup6,six6],backupsize,used6)
                                if trial[1]:
                                    return [trial[0],threes6,trial[2]+init],False,True
    six7=six6
    backup7=backup6
    used7=used6.copy()
    threes7=threes6.copy()
    init1=init.copy()
    for m in range(upperbound):
        six7=six6
        backup7=backup6
        used7=used6.copy()
        threes7=threes6.copy()
        init1=init.copy()
        for i in range(0,len(spaces)-2):
            if six7==0 and backup7==0:
                break
            for j in range(len(spaces)-1,i+1,-1):
                if six7==0 and backup7==0:
                    break
                for k in range(j-1,i,-1):
                    if six7==0 and backup7==0:
                        break
                    if (i not in used7 and j not in used7 and k not in used7) and spaces[i]+spaces[k]+spaces[j]>=(max(backupsize,6)+min(backupsize,6)) and (six7>0 and backup7>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<m:
                        if spaces[i]+spaces[k]+spaces[j]>=(max(backupsize,6)+min(backupsize,6)):
                            if backup7>0 and six7>0:
                                backup7-=1
                                six7-=1
                                used7.update([i,j,k])
                                threes7.append([i+1,k+1,j+1])
                                init1.append([1,1])
                            if param==1:
                                trial=combine(allocations,spaces,[backup7,six7],backupsize,used7)
                                if trial[1] and param==1:
                                    return [trial[0],threes7,trial[2]+init1],False,True
    six8=six7
    backup8=backup7
    used8=used7.copy()
    threes8=threes7.copy()
    init2=init1.copy()
    for m in range(upperbound):
        six8=six7
        backup8=backup7
        used8=used7.copy()
        threes8=threes7.copy()
        init2=init1.copy()
        for i in range(0,len(spaces)-2):
            if six8==0 and backup8==0:
                break
            for j in range(len(spaces)-1,i+1,-1):
                if six8==0 and backup8==0:
                    break
                for k in range(j-1,i,-1):
                    if six8==0 and backup8==0:
                        break
                    if (i not in used8 and j not in used8 and k not in used8) and spaces[i]+spaces[k]+spaces[j]>=(2*min(backupsize,6)) and (six8>0 or backup8>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<m:
                        if spaces[i]+spaces[k]+spaces[j]>=(2*min(backupsize,6)):
                            if backupsize==7 and six8>=2:
                                six8-=2
                                used8.update([i,j,k])
                                threes8.append([i+1,k+1,j+1])
                                init2.append([0,2])
                            elif backupsize==5 and backup8>=2:
                                backup8-=2
                                used8.update([i,j,k])
                                threes8.append([i+1,k+1,j+1])
                                init2.append([2,0])
                            if param==1:
                                trial=combine(allocations,spaces,[backup8,six8],backupsize,used8)
                                if trial[1] and param==1:
                                    return [trial[0],threes8,trial[2]+init2],False,True

    if six8==0 and backup8==0:
        return threes8,True,False,init2

    return [threes8,[backup8,six8],used8,init2],False,False
