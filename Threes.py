def placingthrees(shortfall,used,allocations1,space1,backup_size,upperbound=10):
    allgood=True
    triplecombos=[]
    if used is None:
        used=set()
    allocations=[]
    space=[]
    for i in range(len(space1)):
        if space1[i]!=0:
            allocations.append(allocations1[i])
            space.append(space1[i])

    shortfall4=shortfall.copy()
    used4=used.copy()
    triplecombos4=triplecombos.copy()

    used5=used.copy()
    shortfall5=shortfall.copy()
    triplecombos5=triplecombos4.copy()
    if len(space)>=3:
        if backup_size==7:
            for bound5 in range(0,upperbound):
                if shortfall4[0]==0:
                    break
                shortfall4=shortfall.copy()
                used4=used.copy()
                triplecombos4=triplecombos.copy()
                for i in range(len(space)-2):
                    if shortfall4[0]==0:
                        break
                    for j in range(len(space)-1, i+1, -1):
                        if shortfall4[0]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall4[0]==0:
                                break
                            if space[i]+space[j]+space[k]>=7 and (shortfall4[0]>0) and (i not in used4 and j not in used4 and k not in used4) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound5:
                                used4.add(i)
                                used4.add(j)
                                used4.add(k)
                                shortfall4[0]-=1
                                triplecombos4.append([i+1,k+1,j+1])
            shortfall5=shortfall4.copy()
            used5=used4.copy()
            triplecombos5=triplecombos4.copy()
            for bound6 in range(0,upperbound):
                shortfall5=shortfall4.copy()
                used5=used4.copy()
                triplecombos5=triplecombos4.copy()
                if shortfall5[1]==0:
                    break
                for i in range(len(space)-2):
                    if shortfall5[1]==0:
                        break
                    for j in range(len(space)-1, i+1, -1):
                        if shortfall5[1]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall5[1]==0:
                                break
                            if space[i]+space[j]+space[k]>=6 and (shortfall5[1]>0) and (i not in used5 and j not in used5 and k not in used5) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound6:
                                used5.add(i)
                                used5.add(j)
                                used5.add(k)
                                shortfall5[1]-=1
                                triplecombos5.append([i+1,k+1,j+1])
        else:
            for bound5 in range(0,upperbound):
                if shortfall4[1]==0:
                    break
                shortfall4=shortfall.copy()
                used4=used.copy()
                triplecombos4=triplecombos.copy()
                for i in range(len(space)-2):
                    if shortfall4[1]==0:
                        break
                    for j in range(len(space)-1, i+1, -1):
                        if shortfall4[1]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall4[1]==0:
                                break
                            if space[i]+space[j]+space[k]>=6 and (shortfall4[1]>0) and (i not in used4 and j not in used4 and k not in used4) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound5:
                                used4.add(i)
                                used4.add(j)
                                used4.add(k)
                                shortfall4[1]-=1
                                triplecombos4.append([i+1,k+1,j+1])
            shortfall5=shortfall4.copy()
            used5=used4.copy()
            triplecombos5=triplecombos4.copy()
            for bound6 in range(0,upperbound):
                shortfall5=shortfall4.copy()
                used5=used4.copy()
                triplecombos5=triplecombos4.copy()
                if shortfall5[0]==0:
                    break
                for i in range(len(space)-2):
                    if shortfall5[0]==0:
                        break
                    for j in range(len(space)-1, i+1, -1):
                        if shortfall5[0]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall5[0]==0:
                                break
                            if space[i]+space[j]+space[k]>=5 and (shortfall5[0]>0) and (i not in used5 and j not in used5 and k not in used5) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound6:
                                used5.add(i)
                                used5.add(j)
                                used5.add(k)
                                shortfall5[0]-=1
                                triplecombos5.append([i+1,k+1,j+1])
    if shortfall5[0]==0 and shortfall5[1]==0:
       return triplecombos5,allgood
    allgood=False
    return [triplecombos5,used5,shortfall5],allgood