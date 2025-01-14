def combine(allocations, space, shortfall, upperbound, backup_size=5, used=None):
    if used is None:
        used = set()
    allgood=True
    backup=shortfall[0]
    six=shortfall[1]

    allocations0=[]
    space0=[]
    for i in range(len(space)):
        if space[i]!=0:
            allocations0.append(allocations[i])
            space0.append(space[i])
    used1=used.copy()
    backup1=backup
    six1=six
    combos1=[]
    for bound in range(0,upperbound):
        if backup1==0 and six1==0:
            break
        for m in range(len(space0)):
            if backup1==0 and six1==0:
                break
            for n in range(len(space0)-1,m,-1):
                if backup1==0 and six1==0:
                    break
                if (space0[m]+space0[n]>=min(backup_size,6)) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (backup1 or six1)>0 and (m not in used1) and (n not in used1):
                    if space0[m]+space0[n]>=7 and backup1>0 and backup_size==7:
                        used1.add(m)
                        used1.add(n)
                        combos1.append([m+1,n+1])
                        backup1-=1
                    elif space0[m]+space0[n]>=6 and six1>0:
                        used1.add(m)
                        used1.add(n)
                        combos1.append([m+1,n+1])
                        six1-=1
                    elif space0[m]+space0[n]>=5 and backup1>0 and backup_size==5:
                        used1.add(m)
                        used1.add(n)
                        combos1.append([m+1,n+1])
                        backup1-=1
    if backup1==0 and six1==0:
        return combos1,allgood

    used2=used.copy()
    backup2=backup
    six2=six
    combos2=[]
    if backup_size==7:
        for bound in range(0,upperbound):
            if backup2==0:
                break
            for m in range(len(space0)):
                if backup2==0:
                    break
                for n in range(len(space0)-1,m,-1):
                    if backup2==0:
                        break
                    if (space0[m]+space0[n]>=7) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used2) and (n not in used2):
                        used2.add(m)
                        used2.add(n)
                        combos2.append([m+1,n+1])
                        backup2-=1
    for bound in range(0,upperbound):
        if six2==0:
            break
        for m in range(len(space0)):
            if six2==0:
                break
            for n in range(len(space0)-1,m,-1):
                if six2==0:
                    break
                if (space0[m]+space0[n]>=6) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used2) and (n not in used2):
                    used2.add(m)
                    used2.add(n)
                    combos2.append([m+1,n+1])
                    six2-=1
    if backup_size==5:
        for bound in range(0,upperbound):
            if backup2==0:
                break
            for m in range(len(space0)):
                if backup2==0:
                    break
                for n in range(len(space0)-1,m,-1):
                    if backup2==0:
                        break
                    if (space0[m]+space0[n]>=5) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used2) and (n not in used2):
                        used2.add(m)
                        used2.add(n)
                        combos2.append([m+1,n+1])
                        backup2-=1
    if backup2==0 and six2==0:
        return combos2,allgood
    used3=used.copy()
    backup3=backup
    six3=six
    combos3=[]
    for bound in range(0,upperbound):
        used3=used.copy()
        backup3=backup
        six3=six
        combos3=[]
        if backup3==0 and six3==0:
            break
        for m in range(len(space0)):
            if backup3==0 and six3==0:
                break
            for n in range(len(space0)-1,m,-1):
                if backup3==0 and six3==0:
                    break
                if (space0[m]+space0[n]>=min(backup_size,6)) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (backup3 or six3)>0 and (m not in used3) and (n not in used3):
                    if space0[m]+space0[n]>=7 and backup3>0 and backup_size==7:
                        used3.add(m)
                        used3.add(n)
                        combos3.append([m+1,n+1])
                        backup3-=1
                    elif space0[m]+space0[n]>=6 and six3>0:
                        used3.add(m)
                        used3.add(n)
                        combos3.append([m+1,n+1])
                        six3-=1
                    elif space0[m]+space0[n]>=5 and backup3>0 and backup_size==5:
                        used3.add(m)
                        used3.add(n)
                        combos3.append([m+1,n+1])
                        backup3-=1
    if backup3==0 and six3==0:
        return combos3,allgood

    six4=six
    used4=used.copy()
    combos4=[]
    backup4=backup
    if backup_size==7:
        for bound in range(0,upperbound):
            if backup4==0:
                break
            used4=used.copy()
            backup4=backup
            combos4=[]
            for m in range(len(space0)):
                if backup4==0:
                    break
                for n in range(len(space0)-1,m,-1):
                    if backup4==0:
                        break
                    if (space0[m]+space0[n]>=7) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used4) and (n not in used4):
                        used4.add(m)
                        used4.add(n)
                        combos4.append([m+1,n+1])
                        backup4-=1
        combos5=combos4.copy()
        used5=used4.copy()
        for bound in range(0,upperbound):
            if six4==0:
                break
            used5=used4.copy()
            six4=six
            combos5=combos4.copy()
            for m in range(len(space0)):
                if six4==0:
                    break
                for n in range(len(space0)-1,m,-1):
                    if six4==0:
                        break
                    if (space0[m]+space0[n]>=6) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used5) and (n not in used5):
                        used5.add(m)
                        used5.add(n)
                        combos5.append([m+1,n+1])
                        six4-=1
    else:
        for bound in range(0,upperbound):
            if six4==0:
                break
            used4=used.copy()
            six4=six
            combos4=[]
            for m in range(len(space0)):
                if six4==0:
                    break
                for n in range(len(space0)-1,m,-1):
                    if six4==0:
                        break
                    if (space0[m]+space0[n]>=6) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used4) and (n not in used4):
                        used4.add(m)
                        used4.add(n)
                        combos4.append([m+1,n+1])
                        six4-=1
        combos5=combos4.copy()
        used5=used4.copy()
        for bound in range(0,upperbound):
            if backup4==0:
                break
            used5=used4.copy()
            backup4=backup
            combos5=combos4.copy()
            for m in range(len(space0)):
                if backup4==0:
                    break
                for n in range(len(space0)-1,m,-1):
                    if backup4==0:
                        break
                    if (space0[m]+space0[n]>=5) and ((sum(allocations0[m])+sum(allocations0[n]))<=bound) and (m not in used5) and (n not in used5):
                        used5.add(m)
                        used5.add(n)
                        combos5.append([m+1,n+1])
                        backup4-=1
    if backup4==0 and six4==0:
       return combos5,allgood
    allgood=False
    return [combos5,[backup4,six4],used5],allgood

def bestone(allocations,space,shortfall,backup_size,used=None):
    for x in range(10,11):
        y=combine(allocations,space,shortfall,x,backup_size,used)
        if y[1]:
            return y
    return y
