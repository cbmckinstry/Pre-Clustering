def place3w2(shortfall,allocations,spaces,backupsize=5,upperbound=10):
    allgood=True

    six1=shortfall[1]
    backup1=shortfall[0]
    used1=set()
    threes1=[]
    for m in range(upperbound):
        for i in range(0,len(spaces)-2):
            if six1==0 and backup1==0:
                break
            for j in range(len(spaces)-1,i+1,-1):
                if six1==0 and backup1==0:
                    break
                for k in range(j-1,i,-1):
                    if six1==0 and backup1==0:
                        break
                    if (i not in used1 and j not in used1 and k not in used1) and spaces[i]+spaces[k]+spaces[j]>=(2*min(backupsize,6)) and (six1>0 or backup1>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<m:
                        if spaces[i]+spaces[k]+spaces[j]>=(2*max(backupsize,6)):
                            if backupsize==7:
                                if backup1>1:
                                    backup1-=2
                                    used1.update([i,j,k])
                                    threes1.append([i+1,k+1,j+1])
                                elif six1>1:
                                    six1-=2
                                    used1.update([i,j,k])
                                    threes1.append([i+1,k+1,j+1])
                            elif backupsize==5 and six1>=2:
                                six1-=2
                                used1.update([i,j,k])
                                threes1.append([i+1,k+1,j+1])
                        elif spaces[i]+spaces[k]+spaces[j]>=(max(backupsize,6)+min(backupsize,6)):
                            if backup1>0 and six1>0:
                                backup1-=1
                                six1-=1
                                used1.update([i,j,k])
                                threes1.append([i+1,k+1,j+1])
                        elif spaces[i]+spaces[k]+spaces[j]>=(2*min(backupsize,6)):
                            if backupsize==7 and six1>=2:
                                six1-=2
                                used1.update([i,j,k])
                                threes1.append([i+1,k+1,j+1])
                            elif backupsize==5 and backup1>=2:
                                backup1-=2
                                used1.update([i,j,k])
                                threes1.append([i+1,k+1,j+1])
    if six1==0 and backup1==0:
        return threes1,allgood

    six2=shortfall[1]
    backup2=shortfall[0]
    used2=set()
    threes2=[]
    for m in range(upperbound):
        for i in range(0,len(spaces)-2):
            if six2==0 and backup2==0:
                break
            for j in range(len(spaces)-1,i+1,-1):
                if six2==0 and backup2==0:
                    break
                for k in range(j-1,i,-1):
                    if six2==0 and backup2==0:
                        break
                    if (i not in used2 and j not in used2 and k not in used2) and spaces[i]+spaces[k]+spaces[j]>=(2*max(backupsize,6)) and (six2>0 or backup2>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<m:
                        if spaces[i]+spaces[k]+spaces[j]>=(2*max(backupsize,6)):
                            if backupsize==7:
                                if backup2>1:
                                    backup2-=2
                                    used2.update([i,j,k])
                                    threes2.append([i+1,k+1,j+1])
                                elif six1>1:
                                    six2-=2
                                    used2.update([i,j,k])
                                    threes2.append([i+1,k+1,j+1])
                            elif backupsize==5 and six1>=2:
                                six1-=2
                                used1.update([i,j,k])
                                threes1.append([i+1,k+1,j+1])
    six3=six2
    backup3=backup2
    used3=used2.copy()
    threes3=threes2.copy()
    for m in range(upperbound):
        for i in range(0,len(spaces)-2):
            if six3==0 and backup3==0:
                break
            for j in range(len(spaces)-1,i+1,-1):
                if six3==0 and backup3==0:
                    break
                for k in range(j-1,i,-1):
                    if six3==0 and backup3==0:
                        break
                    if (i not in used3 and j not in used3 and k not in used3) and spaces[i]+spaces[k]+spaces[j]>=(max(backupsize,6)+min(backupsize,6)) and (six3>0 and backup3>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<m:
                        if spaces[i]+spaces[k]+spaces[j]>=(max(backupsize,6)+min(backupsize,6)):
                            if backup3>0 and six3>0:
                                backup3-=1
                                six3-=1
                                used3.update([i,j,k])
                                threes3.append([i+1,k+1,j+1])
    six4=six3
    backup4=backup3
    used4=used3.copy()
    threes4=threes3.copy()
    for m in range(upperbound):
        for i in range(0,len(spaces)-2):
            if six4==0 and backup4==0:
                break
            for j in range(len(spaces)-1,i+1,-1):
                if six4==0 and backup4==0:
                    break
                for k in range(j-1,i,-1):
                    if six4==0 and backup4==0:
                        break
                    if (i not in used4 and j not in used4 and k not in used4) and spaces[i]+spaces[k]+spaces[j]>=(2*min(backupsize,6)) and (six4>0 or backup4>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<m:
                        if spaces[i]+spaces[k]+spaces[j]>=(2*min(backupsize,6)):
                            if backupsize==7 and six4>=2:
                                six4-=2
                                used4.update([i,j,k])
                                threes4.append([i+1,k+1,j+1])
                            elif backupsize==5 and backup4>=2:
                                backup4-=2
                                used4.update([i,j,k])
                                threes4.append([i+1,k+1,j+1])

    if six4==0 and backup4==0:
        return threes4,allgood

    six5=shortfall[1]
    backup5=shortfall[0]
    used5=set()
    threes5=[]
    for m in range(upperbound):
        six5=shortfall[1]
        backup5=shortfall[0]
        used5=set()
        threes5=[]
        for i in range(0,len(spaces)-2):
            if six5==0 and backup5==0:
                break
            for j in range(len(spaces)-1,i+1,-1):
                if six5==0 and backup5==0:
                    break
                for k in range(j-1,i,-1):
                    if six5==0 and backup5==0:
                        break
                    if (i not in used5 and j not in used5 and k not in used5) and spaces[i]+spaces[k]+spaces[j]>=(2*min(backupsize,6)) and (six5>0 or backup5>0) and (sum(allocations[i])+sum(allocations[j])+sum(allocations[k]))<m:
                        if spaces[i]+spaces[k]+spaces[j]>=(2*max(backupsize,6)):
                            if backupsize==7:
                                if backup5>1:
                                    backup5-=2
                                    used5.update([i,j,k])
                                    threes5.append([i+1,k+1,j+1])
                                elif six5>1:
                                    six5-=2
                                    used5.update([i,j,k])
                                    threes5.append([i+1,k+1,j+1])
                            elif backupsize==5 and six5>=2:
                                six5-=2
                                used5.update([i,j,k])
                                threes5.append([i+1,k+1,j+1])
                        elif spaces[i]+spaces[k]+spaces[j]>=(max(backupsize,6)+min(backupsize,6)):
                            if backup5>0 and six5>0:
                                backup5-=1
                                six5-=1
                                used5.update([i,j,k])
                                threes5.append([i+1,k+1,j+1])
                        elif spaces[i]+spaces[k]+spaces[j]>=(2*min(backupsize,6)):
                            if backupsize==7 and six5>=2:
                                six5-=2
                                used5.update([i,j,k])
                                threes5.append([i+1,k+1,j+1])
                            elif backupsize==5 and backup5>=2:
                                backup5-=2
                                used5.update([i,j,k])
                                threes5.append([i+1,k+1,j+1])
    if six5==0 and backup5==0:
        return threes5,allgood
    six6=shortfall[1]
    backup6=shortfall[0]
    used6=set()
    threes6=[]
    for m in range(upperbound):
        six6=shortfall[1]
        backup6=shortfall[0]
        used6=set()
        threes6=[]
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
                            if backupsize==7:
                                if backup6>1:
                                    backup6-=2
                                    used6.update([i,j,k])
                                    threes6.append([i+1,k+1,j+1])
                                elif six6>1:
                                    six6-=2
                                    used6.update([i,j,k])
                                    threes6.append([i+1,k+1,j+1])
                            elif backupsize==5 and six6>=2:
                                six6-=2
                                used6.update([i,j,k])
                                threes6.append([i+1,k+1,j+1])
    six7=six6
    backup7=backup6
    used7=used6.copy()
    threes7=threes6.copy()
    for m in range(upperbound):
        six7=six6
        backup7=backup6
        used7=used6.copy()
        threes7=threes6.copy()
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
    six8=six7
    backup8=backup7
    used8=used7.copy()
    threes8=threes7.copy()
    for m in range(upperbound):
        six8=six7
        backup8=backup7
        used8=used7.copy()
        threes8=threes7.copy()
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
                            elif backupsize==5 and backup8>=2:
                                backup8-=2
                                used8.update([i,j,k])
                                threes8.append([i+1,k+1,j+1])

    if six8==0 and backup8==0:
        return threes8,allgood

    allgood=False
    return [threes8,[backup8,six8],used8],allgood

def place3w2looped(shortfall,allocations,spaces,backupsize):
    for x in range(9,10):
        y=place3w2(shortfall.copy(),allocations,spaces,backupsize,x)
        if y[1]:
            return y
    return y
