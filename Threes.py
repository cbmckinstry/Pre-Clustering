def placingthrees(shortfall,used,allocations,space,backup_size,upperbound=10):
    allgood=True
    triplecombos=[]
    if used is None:
        used=set()
    shortfall1=shortfall.copy()
    used1=used.copy()
    triplecombos1=triplecombos.copy()
    if len(space)>=3:
        for bound1 in range(0,upperbound):
            if shortfall1[0]==0 and shortfall1[1]==0:
                break
            for i in range(len(space)-2):
                if shortfall1[0]==0 and shortfall1[1]==0:
                    break
                for j in range(len(space)-1, i+1, -1):
                    if shortfall1[0]==0 and shortfall1[1]==0:
                        break
                    for k in range(j-1, i, -1):
                        if shortfall1[0]==0 and shortfall1[1]==0:
                            break
                        if space[i]+space[j]+space[k]>=min(backup_size,6) and (shortfall1[0]>0 or shortfall1[1]>0) and (i not in used1) and (j not in used1) and (k not in used1) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound1:
                            if shortfall1[0]>0 and space[i]+space[j]+space[k]>=7 and backup_size==7:
                                used1.add(i)
                                used1.add(j)
                                used1.add(k)
                                shortfall1[0]-=1
                                triplecombos1.append([i+1,k+1,j+1])
                            elif shortfall1[1]>0 and space[i]+space[j]+space[k]>=6:
                                used1.add(i)
                                used1.add(j)
                                used1.add(k)
                                shortfall1[1]-=1
                                triplecombos1.append([i+1,k+1,j+1])
                            elif shortfall1[0]>0 and space[i]+space[j]+space[k]>=5 and backup_size==5:
                                used1.add(i)
                                used1.add(j)
                                used1.add(k)
                                shortfall1[0]-=1
                                triplecombos1.append([i+1,k+1,j+1])

    if shortfall1[0]==0 and shortfall1[1]==0:
       return triplecombos1,allgood

    shortfall2=shortfall.copy()
    used2=used.copy()
    triplecombos2=triplecombos.copy()
    if len(space)>=3:
        if backup_size==7:
            for bound3 in range(0,upperbound):
                if shortfall2[0]==0:
                    break
                for i in range(len(space)-2):
                    if shortfall2[0]==0:
                        break
                    for j in range(len(space)-1, i+1, -1):
                        if shortfall2[0]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall2[0]==0:
                                break
                            if space[i]+space[j]+space[k]>=7 and (shortfall2[0]>0) and (i not in used2 and j not in used2 and k not in used2) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound3:
                                used2.add(i)
                                used2.add(j)
                                used2.add(k)
                                shortfall2[0]-=1
                                triplecombos2.append([i+1,k+1,j+1])
        for bound2 in range(0,upperbound):
            if shortfall2[1]==0:
                break
            for i in range(len(space)-2):
                if shortfall2[1]==0:
                    break
                for j in range(len(space)-1, i+1, -1):
                    if shortfall2[1]==0:
                        break
                    for k in range(j-1, i, -1):
                        if shortfall2[1]==0:
                            break
                        if space[i]+space[j]+space[k]>=6 and (shortfall2[1]>0) and (i not in used2 and j not in used2 and k not in used2) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound2:
                            used2.add(i)
                            used2.add(j)
                            used2.add(k)
                            shortfall2[1]-=1
                            triplecombos2.append([i+1,k+1,j+1])
        if backup_size==5:
            for bound3 in range(0,upperbound):
                if shortfall2[0]==0:
                    break
                for i in range(len(space)-2):
                    if shortfall2[0]==0:
                        break
                    for j in range(len(space)-1, i+1, -1):
                        if shortfall2[0]==0:
                            break
                        for k in range(j-1, i, -1):
                            if shortfall2[0]==0:
                                break
                            if space[i]+space[j]+space[k]>=5 and (shortfall2[0]>0) and (i not in used2 and j not in used2 and k not in used2) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound3:
                                used2.add(i)
                                used2.add(j)
                                used2.add(k)
                                shortfall2[0]-=1
                                triplecombos2.append([i+1,k+1,j+1])
    if shortfall2[0]==0 and shortfall2[1]==0:
        return triplecombos2,allgood

    shortfall3=shortfall.copy()
    used3=used.copy()
    triplecombos3=triplecombos.copy()
    if len(space)>=3:
        for bound4 in range(0,upperbound):
            if shortfall3[0]==0 and shortfall3[1]==0:
                break
            shortfall3=shortfall.copy()
            used3=used.copy()
            triplecombos3=triplecombos.copy()
            for i in range(len(space)-2):
                if shortfall3[0]==0 and shortfall3[1]==0:
                    break
                for j in range(len(space)-1, i+1, -1):
                    if shortfall3[0]==0 and shortfall3[1]==0:
                        break
                    for k in range(j-1, i, -1):
                        if shortfall3[0]==0 and shortfall3[1]==0:
                            break
                        if space[i]+space[j]+space[k]>=min(backup_size,6) and (shortfall3[0]>0 or shortfall3[1]>0) and (i not in used3 and j not in used3 and k not in used3) and sum(allocations[i])+sum(allocations[k])+sum(allocations[j])<=bound4:
                            if shortfall3[0]>0 and space[i]+space[j]+space[k]>=7 and backup_size==7:
                                used3.add(i)
                                used3.add(j)
                                used3.add(k)
                                shortfall3[0]-=1
                                triplecombos3.append([i+1,k+1,j+1])
                            elif shortfall3[1]>0 and space[i]+space[j]+space[k]>=6:
                                used3.add(i)
                                used3.add(j)
                                used3.add(k)
                                shortfall3[1]-=1
                                triplecombos3.append([i+1,k+1,j+1])
                            elif shortfall3[0]>0 and space[i]+space[j]+space[k]>=5 and backup_size==5:
                                used3.add(i)
                                used3.add(j)
                                used3.add(k)
                                shortfall3[0]-=1
                                triplecombos3.append([i+1,k+1,j+1])
    if shortfall3[0]==0 and shortfall3[1]==0:
        return triplecombos3,allgood

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

def best3(shortfall,used,allocations,space,backup_size):
    for upper in range(9,10):
        out=placingthrees(shortfall,used,allocations,space,backup_size,upper)
        if out[1]:
            return out
    return out
