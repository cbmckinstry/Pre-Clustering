from Combine import *
def threes(shortfall, allocations1, spaces1, backupsize=5, used5=None, boundlst=None):
    if boundlst is None:
        boundlst = [[0,0], [0,0], [0,0]]
    if used5 is None:
        used5=set()
    allocations=[]
    spaces=[]
    upperbound=boundlst[1][1]
    lower=boundlst[1][0]
    for i in range(len(spaces1)):
        if spaces1[i]!=0:
            allocations.append(allocations1[i])
            spaces.append(spaces1[i])

    x=compared_combine(allocations,spaces,shortfall.copy(),backupsize,used5,boundlst)
    if x[1]:
        return x

    six6=shortfall[1]
    backup6=shortfall[0]
    threes6=[]
    used6=used5.copy()
    init=[]
    for m in range(lower,upperbound):
        for i in range(0,len(spaces)-2):
            if six6==0 and backup6==0:
                break
            for j in range(len(spaces)-1,i+1,-1):
                if six6==0 and backup6==0:
                    break
                for k in range(j-1,i,-1):
                    if six6==0 and backup6==0:
                        break
                    if (i not in used6 and j not in used6 and k not in used6) and spaces[i]+spaces[k]+spaces[j]>=(2*max(backupsize,6)) and (six6>0 or backup6>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<=m:
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
                            if six6==0 and backup6==0:
                                return threes6,init
                            trial=compared_combine(allocations,spaces,[backup6,six6],backupsize,used6,[[boundlst[0][0],m+1],[boundlst[0][0],m+1],[boundlst[0][0],m+1],[boundlst[0][0],m+1]])
                            if trial[1]:
                                return trial[0]+threes6,trial[1]+init
    six7=six6
    backup7=backup6
    used7=used6.copy()
    threes7=threes6.copy()
    init1=init.copy()
    for m in range(lower,upperbound):
        for i in range(0,len(spaces)-2):
            if six7==0 and backup7==0:
                break
            for j in range(len(spaces)-1,i+1,-1):
                if six7==0 and backup7==0:
                    break
                for k in range(j-1,i,-1):
                    if six7==0 and backup7==0:
                        break
                    if (i not in used7 and j not in used7 and k not in used7) and spaces[i]+spaces[k]+spaces[j]>=(max(backupsize,6)+min(backupsize,6)) and (six7>0 and backup7>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<=m:
                        if spaces[i]+spaces[k]+spaces[j]>=(max(backupsize,6)+min(backupsize,6)):
                            if backup7>0 and six7>0:
                                backup7-=1
                                six7-=1
                                used7.update([i,j,k])
                                threes7.append([i+1,k+1,j+1])
                                init1.append([1,1])
                            if six7==0 and backup7==0:
                                return threes7,init1
                            trial=compared_combine(allocations,spaces,[backup7,six7],backupsize,used7,[[boundlst[0][0],m+1],[boundlst[0][0],m+1],[boundlst[0][0],m+1],[boundlst[0][0],m+1]])
                            if trial[1]:
                                return trial[0]+threes7,trial[1]+init1
    six8=six7
    backup8=backup7
    used8=used7.copy()
    threes8=threes7.copy()
    init2=init1.copy()
    for m in range(lower,upperbound):
        for i in range(0,len(spaces)-2):
            if six8==0 and backup8==0:
                break
            for j in range(len(spaces)-1,i+1,-1):
                if six8==0 and backup8==0:
                    break
                for k in range(j-1,i,-1):
                    if six8==0 and backup8==0:
                        break
                    if (i not in used8 and j not in used8 and k not in used8) and spaces[i]+spaces[k]+spaces[j]>=(2*min(backupsize,6)) and (six8>0 or backup8>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<=m:
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
                            if six8==0 and backup8==0:
                                return threes8,init2
                            trial=compared_combine(allocations,spaces,[backup8,six8],backupsize,used8,[[boundlst[0][0],m+1],[boundlst[0][0],m+1],[boundlst[0][0],m+1],[boundlst[0][0],m+1]])
                            if trial[1]:
                                return trial[0]+threes8,trial[1]+init2

    if six8==0 and backup8==0:
        return threes8,init2


    shortfall4=[backup8,six8]
    used4=used8.copy()
    triplecombos4=threes8.copy()

    used5=used8.copy()
    shortfall5=shortfall4.copy()
    triplecombos5=threes8.copy()

    init3=init2.copy()
    init4=init2.copy()
    if len(spaces)>=3:
        if backupsize==7:
            for bound5 in range(lower,upperbound):
                if shortfall4[0]==0:
                    break
                for i in range(len(spaces)-2):
                    if shortfall4[0]==0:
                        break
                    for j in range(len(spaces)-1, i+1, -1):
                        if shortfall4[0]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall4[0]==0:
                                break
                            if spaces[i]+spaces[j]+spaces[k]>=7 and (shortfall4[0]>0) and (i not in used4 and j not in used4 and k not in used4) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound5:
                                used4.add(i)
                                used4.add(j)
                                used4.add(k)
                                shortfall4[0]-=1
                                triplecombos4.append([i+1,k+1,j+1])
                                init3.append([1,0])
                                if shortfall4[0]==0 and shortfall4[1]==0:
                                    return triplecombos4,init3
                                trial=compared_combine(allocations,spaces,shortfall4,backupsize,used4,[[boundlst[0][0],bound5+1],[boundlst[0][0],bound5+1],[boundlst[0][0],bound5+1],[boundlst[0][0],bound5+1]])
                                if trial[1]:
                                    return trial[0]+triplecombos4,trial[1]+init3
            shortfall5=shortfall4.copy()
            used5=used4.copy()
            triplecombos5=triplecombos4.copy()
            init4=init3.copy()
            for bound6 in range(lower,upperbound):
                if shortfall5[1]==0:
                    break
                for i in range(len(spaces)-2):
                    if shortfall5[1]==0:
                        break
                    for j in range(len(spaces)-1, i+1, -1):
                        if shortfall5[1]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall5[1]==0:
                                break
                            if spaces[i]+spaces[j]+spaces[k]>=6 and (shortfall5[1]>0) and (i not in used5 and j not in used5 and k not in used5) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound6:
                                used5.add(i)
                                used5.add(j)
                                used5.add(k)
                                shortfall5[1]-=1
                                triplecombos5.append([i+1,k+1,j+1])
                                init4.append([0,1])
                                if shortfall5[0]==0 and shortfall5[1]==0:
                                    return triplecombos5,init4
                                trial=compared_combine(allocations,spaces,shortfall5,backupsize,used5,[[boundlst[0][0],bound6+1],[boundlst[0][0],bound6+1],[boundlst[0][0],bound6+1],[boundlst[0][0],bound6+1]])
                                if trial[1]:
                                    return trial[0]+triplecombos5,trial[1]+init4
        else:
            for bound5 in range(lower,upperbound):
                if shortfall4[1]==0:
                    break
                for i in range(len(spaces)-2):
                    if shortfall4[1]==0:
                        break
                    for j in range(len(spaces)-1, i+1, -1):
                        if shortfall4[1]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall4[1]==0:
                                break
                            if spaces[i]+spaces[j]+spaces[k]>=6 and (shortfall4[1]>0) and (i not in used4 and j not in used4 and k not in used4) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound5:
                                used4.add(i)
                                used4.add(j)
                                used4.add(k)
                                shortfall4[1]-=1
                                triplecombos4.append([i+1,k+1,j+1])
                                init3.append([0,1])
                                if shortfall4[0]==0 and shortfall4[1]==0:
                                    return triplecombos4,init3
                                trial=compared_combine(allocations,spaces,shortfall4,backupsize,used4,[[boundlst[0][0],bound5+1],[boundlst[0][0],bound5+1],[boundlst[0][0],bound5+1],[boundlst[0][0],bound5+1]])
                                if trial[1]:
                                    return trial[0]+triplecombos4,trial[1]+init3
            shortfall5=shortfall4.copy()
            used5=used4.copy()
            triplecombos5=triplecombos4.copy()
            init4=init3.copy()
            for bound6 in range(lower,upperbound):
                if shortfall5[0]==0:
                    break
                for i in range(len(spaces)-2):
                    if shortfall5[0]==0:
                        break
                    for j in range(len(spaces)-1, i+1, -1):
                        if shortfall5[0]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall5[0]==0:
                                break
                            if spaces[i]+spaces[j]+spaces[k]>=5 and (shortfall5[0]>0) and (i not in used5 and j not in used5 and k not in used5) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound6:
                                used5.add(i)
                                used5.add(j)
                                used5.add(k)
                                shortfall5[0]-=1
                                triplecombos5.append([i+1,k+1,j+1])
                                init4.append([1,0])
                                if shortfall5[0]==0 and shortfall5[1]==0:
                                    return triplecombos5,init4
                                trial=compared_combine(allocations,spaces,shortfall5,backupsize,used5,[[boundlst[0][0],bound6+1],[boundlst[0][0],bound6+1],[boundlst[0][0],bound6+1],[boundlst[0][0],bound6+1]])
                                if trial[1]:
                                    return trial[0]+triplecombos5,trial[1]+init4
    if shortfall5[0]==0 and shortfall5[1]==0:
        return triplecombos5,init4

    return [],[]

def threes1(shortfall, allocations1, spaces1, backupsize=5, used5=None, boundlst=None):
    if boundlst is None:
        boundlst = [[0,0], [0,0], [0,0]]
    if used5 is None:
        used5=set()
    allocations=[]
    spaces=[]
    upperbound=boundlst[1][1]
    lower=boundlst[1][0]
    for i in range(len(spaces1)):
        if spaces1[i]!=0:
            allocations.append(allocations1[i])
            spaces.append(spaces1[i])

    x=compared_combine(allocations,spaces,shortfall.copy(),backupsize,used5,boundlst)
    if x[1]:
        return x

    six6=shortfall[1]
    backup6=shortfall[0]
    threes6=[]
    used6=used5.copy()
    init=[]
    for m in range(lower,upperbound):
        six6=shortfall[1]
        backup6=shortfall[0]
        used6=used5.copy()
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
                    if (i not in used6 and j not in used6 and k not in used6) and spaces[i]+spaces[k]+spaces[j]>=(2*max(backupsize,6)) and (six6>0 or backup6>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<=m:
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
                            if six6==0 and backup6==0:
                                return threes6,init
                            trial=compared_combine(allocations,spaces,[backup6,six6],backupsize,used6,[[boundlst[0][0],m+1],[boundlst[0][0],m+1],[boundlst[0][0],m+1],[boundlst[0][0],m+1]])
                            if trial[1]:
                                return trial[0]+threes6,trial[1]+init
    six7=six6
    backup7=backup6
    used7=used6.copy()
    threes7=threes6.copy()
    init1=init.copy()
    for m in range(lower,upperbound):
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
                    if (i not in used7 and j not in used7 and k not in used7) and spaces[i]+spaces[k]+spaces[j]>=(max(backupsize,6)+min(backupsize,6)) and (six7>0 and backup7>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<=m:
                        if spaces[i]+spaces[k]+spaces[j]>=(max(backupsize,6)+min(backupsize,6)):
                            if backup7>0 and six7>0:
                                backup7-=1
                                six7-=1
                                used7.update([i,j,k])
                                threes7.append([i+1,k+1,j+1])
                                init1.append([1,1])
                            if six7==0 and backup7==0:
                                return threes7,init1
                            trial=compared_combine(allocations,spaces,[backup7,six7],backupsize,used7,[[boundlst[0][0],m+1],[boundlst[0][0],m+1],[boundlst[0][0],m+1],[boundlst[0][0],m+1]])
                            if trial[1]:
                                return trial[0]+threes7,trial[1]+init1
    six8=six7
    backup8=backup7
    used8=used7.copy()
    threes8=threes7.copy()
    init2=init1.copy()
    for m in range(lower,upperbound):
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
                    if (i not in used8 and j not in used8 and k not in used8) and spaces[i]+spaces[k]+spaces[j]>=(2*min(backupsize,6)) and (six8>0 or backup8>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<=m:
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
                            if six8==0 and backup8==0:
                                return threes8,init2
                            trial=compared_combine(allocations,spaces,[backup8,six8],backupsize,used8,[[boundlst[0][0],m+1],[boundlst[0][0],m+1],[boundlst[0][0],m+1],[boundlst[0][0],m+1]])
                            if trial[1]:
                                return trial[0]+threes8,trial[1]+init2

    if six8==0 and backup8==0:
        return threes8,init2


    shortfall4=[backup8,six8]
    used4=used8.copy()
    triplecombos4=threes8.copy()

    used5=used8.copy()
    shortfall5=shortfall4.copy()
    triplecombos5=threes8.copy()

    init3=init2.copy()
    init4=init2.copy()
    if len(spaces)>=3:
        if backupsize==7:
            for bound5 in range(lower,upperbound):
                if shortfall4[0]==0:
                    break
                shortfall4=[backup8,six8]
                used4=used8.copy()
                triplecombos4=threes8.copy()
                init3=init2.copy()
                for i in range(len(spaces)-2):
                    if shortfall4[0]==0:
                        break
                    for j in range(len(spaces)-1, i+1, -1):
                        if shortfall4[0]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall4[0]==0:
                                break
                            if spaces[i]+spaces[j]+spaces[k]>=7 and (shortfall4[0]>0) and (i not in used4 and j not in used4 and k not in used4) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound5:
                                used4.add(i)
                                used4.add(j)
                                used4.add(k)
                                shortfall4[0]-=1
                                triplecombos4.append([i+1,k+1,j+1])
                                init3.append([1,0])
                                if shortfall4[0]==0 and shortfall4[1]==0:
                                    return triplecombos4,init3
                                trial=compared_combine(allocations,spaces,shortfall4,backupsize,used4,[[boundlst[0][0],bound5+1],[boundlst[0][0],bound5+1],[boundlst[0][0],bound5+1],[boundlst[0][0],bound5+1]])
                                if trial[1]:
                                    return trial[0]+triplecombos4,trial[1]+init3
            shortfall5=shortfall4.copy()
            used5=used4.copy()
            triplecombos5=triplecombos4.copy()
            init4=init3.copy()
            for bound6 in range(lower,upperbound):
                shortfall5=shortfall4.copy()
                used5=used4.copy()
                triplecombos5=triplecombos4.copy()
                init4=init3.copy()
                if shortfall5[1]==0:
                    break
                for i in range(len(spaces)-2):
                    if shortfall5[1]==0:
                        break
                    for j in range(len(spaces)-1, i+1, -1):
                        if shortfall5[1]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall5[1]==0:
                                break
                            if spaces[i]+spaces[j]+spaces[k]>=6 and (shortfall5[1]>0) and (i not in used5 and j not in used5 and k not in used5) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound6:
                                used5.add(i)
                                used5.add(j)
                                used5.add(k)
                                shortfall5[1]-=1
                                triplecombos5.append([i+1,k+1,j+1])
                                init4.append([0,1])
                                if shortfall5[0]==0 and shortfall5[1]==0:
                                    return triplecombos5,init4
                                trial=compared_combine(allocations,spaces,shortfall5,backupsize,used5,[[boundlst[0][0],bound6+1],[boundlst[0][0],bound6+1],[boundlst[0][0],bound6+1],[boundlst[0][0],bound6+1]])
                                if trial[1]:
                                    return trial[0]+triplecombos5,trial[1]+init4
        else:
            for bound5 in range(lower,upperbound):
                if shortfall4[1]==0:
                    break
                shortfall4=[backup8,six8]
                used4=used8.copy()
                triplecombos4=threes8.copy()
                init3=init2.copy()
                for i in range(len(spaces)-2):
                    if shortfall4[1]==0:
                        break
                    for j in range(len(spaces)-1, i+1, -1):
                        if shortfall4[1]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall4[1]==0:
                                break
                            if spaces[i]+spaces[j]+spaces[k]>=6 and (shortfall4[1]>0) and (i not in used4 and j not in used4 and k not in used4) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound5:
                                used4.add(i)
                                used4.add(j)
                                used4.add(k)
                                shortfall4[1]-=1
                                triplecombos4.append([i+1,k+1,j+1])
                                init3.append([0,1])
                                if shortfall4[0]==0 and shortfall4[1]==0:
                                    return triplecombos4,init3
                                trial=compared_combine(allocations,spaces,shortfall4,backupsize,used4,[[boundlst[0][0],bound5+1],[boundlst[0][0],bound5+1],[boundlst[0][0],bound5+1],[boundlst[0][0],bound5+1]])
                                if trial[1]:
                                    return trial[0]+triplecombos4,trial[1]+init3
            shortfall5=shortfall4.copy()
            used5=used4.copy()
            triplecombos5=triplecombos4.copy()
            init4=init3.copy()
            for bound6 in range(lower,upperbound):
                shortfall5=shortfall4.copy()
                used5=used4.copy()
                triplecombos5=triplecombos4.copy()
                init4=init3.copy()
                if shortfall5[0]==0:
                    break
                for i in range(len(spaces)-2):
                    if shortfall5[0]==0:
                        break
                    for j in range(len(spaces)-1, i+1, -1):
                        if shortfall5[0]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall5[0]==0:
                                break
                            if spaces[i]+spaces[j]+spaces[k]>=5 and (shortfall5[0]>0) and (i not in used5 and j not in used5 and k not in used5) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound6:
                                used5.add(i)
                                used5.add(j)
                                used5.add(k)
                                shortfall5[0]-=1
                                triplecombos5.append([i+1,k+1,j+1])
                                init4.append([1,0])
                                if shortfall5[0]==0 and shortfall5[1]==0:
                                    return triplecombos5,init4
                                trial=compared_combine(allocations,spaces,shortfall5,backupsize,used5,[[boundlst[0][0],bound6+1],[boundlst[0][0],bound6+1],[boundlst[0][0],bound6+1],[boundlst[0][0],bound6+1]])
                                if trial[1]:
                                    return trial[0]+triplecombos5,trial[1]+init4
    if shortfall5[0]==0 and shortfall5[1]==0:
        return triplecombos5,init4

    return [],[]

def compared_threes(shortfall,allocations,spaces,backupsize=5,used=None,boundlst=None):
    results=threes(shortfall,allocations,spaces,backupsize,used,boundlst)
    results1=threes1(shortfall,allocations,spaces,backupsize,used,boundlst)
    maxnow=0
    maxnow1=0
    if results1==([],[]) and results==([],[]):
        return [],[]
    if results1==([],[]):
        return results[0],results[1]
    if results==([],[]):
        return results1[0],results1[1]
    for elem in results[0]:
        runningsum=0
        for item in elem:
            runningsum+=sum(allocations[item-1])
        if runningsum>maxnow:
            maxnow=runningsum
    for elem in results1[0]:
        runningsum1=0
        for item in elem:
            runningsum1+=sum(allocations[item-1])
        if runningsum1>maxnow1:
            maxnow1=runningsum1
    if maxnow1<maxnow:
        return results1[0],results1[1]
    else:
        return results[0],results[1]