from Threes import *
def fours(shortfall,allocations1,spaces1,backupsize=5,used5=None,boundlst=None):
    if used5 is None:
        used5=set()
    if boundlst is None:
        boundlst = [[0,0], [0,0], [0,0],[0,0]]
    allocations=[]
    spaces=[]
    for i in range(len(spaces1)):
        if spaces1[i]!=0:
            allocations.append(allocations1[i])
            spaces.append(spaces1[i])

    a=compared_threes(shortfall.copy(),allocations,spaces,backupsize,used5,boundlst)
    if a[1]:
        return a
    lower=boundlst[2][0]
    upperbound=boundlst[2][1]

    six6=shortfall[1]
    backup6=shortfall[0]
    fours6=[]
    used6=used5.copy()
    init=[]
    for bound in range(lower,upperbound):
        for i in range(0,len(spaces)-3):
            if six6==0 and backup6==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six6==0 and backup6==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six6==0 and backup6==0:
                        break
                    for l in range(k-1,i,-1):
                        if six6==0 and backup6==0:
                            break
                        if (i not in used6 and j not in used6 and k not in used6 and l not in used6) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(3*max(backupsize,6)) and (six6>0 or backup6>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(3*max(backupsize,6)):
                                if backupsize==7 and backup6>=3:
                                    backup6-=3
                                    used6.update([i,j,k,l])
                                    fours6.append([i+1,l+1,k+1,j+1])
                                    init.append([3,0])
                                elif backupsize==5 and six6>=3:
                                    six6-=3
                                    used6.update([i,j,k,l])
                                    fours6.append([i+1,l+1,k+1,j+1])
                                    init.append([0,3])
                                if six6==0 and backup6==0:
                                    return fours6,init
                                trial=compared_threes([backup6,six6],allocations,spaces,backupsize,used6,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours6,trial[1]+init
    six7=six6
    backup7=backup6
    used7=used6.copy()
    fours7=fours6.copy()
    init1=init.copy()
    for bound in range(lower,upperbound):
        for i in range(0,len(spaces)-3):
            if six7==0 and backup7==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six7==0 and backup7==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six7==0 and backup7==0:
                        break
                    for l in range(k-1,i,-1):
                        if six7==0 and backup7==0:
                            break
                        if (i not in used7 and j not in used7 and k not in used7 and l not in used7) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(2*max(backupsize,6)+min(backupsize,6)) and (six7>0 and backup7>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(2*max(backupsize,6)+min(backupsize,6)):
                                if backupsize==7 and backup7>=2 and six7>=1:
                                    backup7-=2
                                    six7-=1
                                    used7.update([i,j,k,l])
                                    fours7.append([i+1,l+1,k+1,j+1])
                                    init1.append([2,1])
                                elif backupsize==5 and six7>=2 and backup7>=1:
                                    six7-=2
                                    backup7-=1
                                    used7.update([i,j,k,l])
                                    fours7.append([i+1,l+1,k+1,j+1])
                                    init1.append([1,2])
                                if six7==0 and backup7==0:
                                    return fours7,init1
                                trial=compared_threes([backup7,six7],allocations,spaces,backupsize,used7,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours7,trial[1]+init1
    six8=six7
    backup8=backup7
    used8=used7.copy()
    fours8=fours7.copy()
    init2=init1.copy()
    for bound in range(lower,upperbound):
        for i in range(0,len(spaces)-3):
            if six8==0 and backup8==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six8==0 and backup8==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six8==0 and backup8==0:
                        break
                    for l in range(k-1,i,-1):
                        if six8==0 and backup8==0:
                            break
                        if (i not in used8 and j not in used8 and k not in used8 and l not in used8) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(max(backupsize,6)+2*min(backupsize,6)) and (six8>0 and backup8>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(max(backupsize,6)+2*min(backupsize,6)):
                                if backupsize==7 and backup8>=1 and six8>=2:
                                    backup8-=1
                                    six8-=2
                                    used8.update([i,j,k,l])
                                    fours8.append([i+1,l+1,k+1,j+1])
                                    init2.append([1,2])
                                elif backupsize==5 and six8>=1 and backup8>=2:
                                    six8-=1
                                    backup8-=2
                                    used8.update([i,j,k,l])
                                    fours8.append([i+1,l+1,k+1,j+1])
                                    init2.append([2,1])
                                if six8==0 and backup8==0:
                                    return fours8,init2
                                trial=compared_threes([backup8,six8],allocations,spaces,backupsize,used8,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours8,trial[1]+init2
    six9=six8
    backup9=backup8
    fours9=fours8.copy()
    used9=used8.copy()
    init3=init2.copy()
    for bound in range(lower,upperbound):
        for i in range(0,len(spaces)-3):
            if six9==0 and backup9==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six9==0 and backup9==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six9==0 and backup9==0:
                        break
                    for l in range(k-1,i,-1):
                        if six9==0 and backup9==0:
                            break
                        if (i not in used9 and j not in used9 and k not in used9 and l not in used9) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(3*min(backupsize,6)) and (six9>0 or backup9>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(3*max(backupsize,6)):
                                if backupsize==7 and six9>=3:
                                    six9-=3
                                    used9.update([i,j,k,l])
                                    fours9.append([i+1,l+1,k+1,j+1])
                                    init3.append([0,3])
                                elif backupsize==5 and backup9>=3:
                                    backup9-=3
                                    used9.update([i,j,k,l])
                                    fours9.append([i+1,l+1,k+1,j+1])
                                    init3.append([3,0])
                                if six9==0 and backup9==0:
                                    return fours9,init3
                                trial=compared_threes([backup9,six9],allocations,spaces,backupsize,used9,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours9,trial[1]+init3

    if six9==0 and backup9==0:
        return fours9,init3


    six10=six9
    backup10=backup9
    fours10=fours9.copy()
    used10=used9.copy()
    init4=init3.copy()
    for bound in range(lower,upperbound):
        for i in range(0,len(spaces)-3):
            if six10==0 and backup10==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six10==0 and backup10==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six10==0 and backup10==0:
                        break
                    for l in range(k-1,i,-1):
                        if six10==0 and backup10==0:
                            break
                        if (i not in used10 and j not in used10 and k not in used10 and l not in used10) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(2*max(backupsize,6)) and (six10>0 or backup10>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(2*max(backupsize,6)):
                                if backupsize==7 and backup10>=2:
                                    backup10-=2
                                    used10.update([i,j,k,l])
                                    fours10.append([i+1,l+1,k+1,j+1])
                                    init4.append([2,0])
                                elif backupsize==5 and six10>=2:
                                    six10-=2
                                    used10.update([i,j,k,l])
                                    fours10.append([i+1,l+1,k+1,j+1])
                                    init4.append([0,2])
                                if six10==0 and backup10==0:
                                    return fours10,init4
                                trial=compared_threes([backup10,six10],allocations,spaces,backupsize,used10,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours10,trial[1]+init4
    six11=six10
    backup11=backup10
    used11=used10.copy()
    fours11=fours10.copy()
    init5=init4.copy()
    for bound in range(lower,upperbound):
        for i in range(0,len(spaces)-3):
            if six11==0 and backup11==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six11==0 and backup11==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six11==0 and backup11==0:
                        break
                    for l in range(k-1,i,-1):
                        if six11==0 and backup11==0:
                            break
                        if (i not in used11 and j not in used11 and k not in used11 and l not in used11) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(max(backupsize,6)+min(backupsize,6)) and (six11>0 and backup11>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(max(backupsize,6)+min(backupsize,6)):
                                if backup11>=1 and six11>=1:
                                    backup11-=1
                                    six11-=1
                                    used11.update([i,j,k,l])
                                    fours11.append([i+1,l+1,k+1,j+1])
                                    init5.append([1,1])
                                if six11==0 and backup11==0:
                                    return fours11,init5
                                trial=compared_threes([backup11,six11],allocations,spaces,backupsize,used11,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours11,trial[1]+init5
    six12=six11
    backup12=backup11
    fours12=fours11.copy()
    used12=used11.copy()
    init6=init5.copy()
    for bound in range(lower,upperbound):
        for i in range(0,len(spaces)-3):
            if six12==0 and backup12==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six12==0 and backup12==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six12==0 and backup12==0:
                        break
                    for l in range(k-1,i,-1):
                        if six12==0 and backup12==0:
                            break
                        if (i not in used12 and j not in used12 and k not in used12 and l not in used12) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(2*min(backupsize,6)) and (six12>0 or backup12>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(2*min(backupsize,6)):
                                if backupsize==7 and six12>=2:
                                    six12-=2
                                    used12.update([i,j,k,l])
                                    fours12.append([i+1,l+1,k+1,j+1])
                                    init6.append([0,2])
                                elif backupsize==5 and backup12>=2:
                                    backup12-=2
                                    used12.update([i,j,k,l])
                                    fours12.append([i+1,l+1,k+1,j+1])
                                    init6.append([2,0])
                                if six12==0 and backup12==0:
                                    return fours12,init6
                                trial=compared_threes([backup12,six12],allocations,spaces,backupsize,used12,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours12,trial[1]+init6

    if backup12==0 and six12==0:
        return fours12,init6

    six13=six12
    backup13=backup12
    fours13=fours12.copy()
    used13=used12.copy()
    init7=init6.copy()
    for bound in range(lower,upperbound):
        for i in range(0,len(spaces)-3):
            if six13==0 and backup13==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six13==0 and backup13==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six13==0 and backup13==0:
                        break
                    for l in range(k-1,i,-1):
                        if six13==0 and backup13==0:
                            break
                        if (i not in used13 and j not in used13 and k not in used13 and l not in used13) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(max(backupsize,6)) and (six13>0 or backup13>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(max(backupsize,6)):
                                if backupsize==7 and backup13>=1:
                                    backup13-=1
                                    used13.update([i,j,k,l])
                                    fours13.append([i+1,l+1,k+1,j+1])
                                    init7.append([1,0])
                                elif backupsize==5 and six13>=1:
                                    six13-=1
                                    used13.update([i,j,k,l])
                                    fours13.append([i+1,l+1,k+1,j+1])
                                    init7.append([0,1])
                                if six13==0 and backup13==0:
                                    return fours13,init7
                                trial=compared_threes([backup13,six13],allocations,spaces,backupsize,used13,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours13,trial[1]+init7
    six14=six13
    backup14=backup13
    fours14=fours13.copy()
    used14=used13.copy()
    init8=init7.copy()
    for bound in range(lower,upperbound):
        for i in range(0,len(spaces)-3):
            if six14==0 and backup14==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six14==0 and backup14==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six14==0 and backup14==0:
                        break
                    for l in range(k-1,i,-1):
                        if six14==0 and backup14==0:
                            break
                        if (i not in used14 and j not in used14 and k not in used14 and l not in used14) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(min(backupsize,6)) and (six14>0 or backup14>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(min(backupsize,6)):
                                if backupsize==7 and six14>=1:
                                    six14-=1
                                    used14.update([i,j,k,l])
                                    fours14.append([i+1,l+1,k+1,j+1])
                                    init8.append([0,1])
                                elif backupsize==5 and backup14>=1:
                                    backup14-=1
                                    used14.update([i,j,k,l])
                                    fours14.append([i+1,l+1,k+1,j+1])
                                    init8.append([1,0])
                                if six14==0 and backup14==0:
                                    return fours14,init8
                                trial=compared_threes([backup14,six14],allocations,spaces,backupsize,used14,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours14,trial[1]+init8

    if six14==0 and backup14==0:
        return fours14,init8

def fours1(shortfall,allocations1,spaces1,backupsize=5,used5=None,boundlst=None):
    if used5 is None:
        used5=set()
    if boundlst is None:
        boundlst = [[0,0], [0,0], [0,0],[0,0]]
    allocations=[]
    spaces=[]
    for i in range(len(spaces1)):
        if spaces1[i]!=0:
            allocations.append(allocations1[i])
            spaces.append(spaces1[i])

    a=compared_threes(shortfall.copy(),allocations,spaces,backupsize,used5,boundlst)
    if a[1]:
        return a
    lower=boundlst[2][0]
    upperbound=boundlst[2][1]

    six6=shortfall[1]
    backup6=shortfall[0]
    fours6=[]
    used6=used5.copy()
    init=[]
    for bound in range(lower,upperbound):
        six6=shortfall[1]
        backup6=shortfall[0]
        fours6=[]
        used6=used5.copy()
        init=[]
        for i in range(0,len(spaces)-3):
            if six6==0 and backup6==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six6==0 and backup6==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six6==0 and backup6==0:
                        break
                    for l in range(k-1,i,-1):
                        if six6==0 and backup6==0:
                            break
                        if (i not in used6 and j not in used6 and k not in used6 and l not in used6) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(3*max(backupsize,6)) and (six6>0 or backup6>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(3*max(backupsize,6)):
                                if backupsize==7 and backup6>=3:
                                    backup6-=3
                                    used6.update([i,j,k,l])
                                    fours6.append([i+1,l+1,k+1,j+1])
                                    init.append([3,0])
                                elif backupsize==5 and six6>=3:
                                    six6-=3
                                    used6.update([i,j,k,l])
                                    fours6.append([i+1,l+1,k+1,j+1])
                                    init.append([0,3])
                                if six6==0 and backup6==0:
                                    return fours6,init
                                trial=compared_threes([backup6,six6],allocations,spaces,backupsize,used6,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours6,trial[1]+init
    six7=six6
    backup7=backup6
    used7=used6.copy()
    fours7=fours6.copy()
    init1=init.copy()
    for bound in range(lower,upperbound):
        six7=six6
        backup7=backup6
        used7=used6.copy()
        fours7=fours6.copy()
        init1=init.copy()
        for i in range(0,len(spaces)-3):
            if six7==0 and backup7==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six7==0 and backup7==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six7==0 and backup7==0:
                        break
                    for l in range(k-1,i,-1):
                        if six7==0 and backup7==0:
                            break
                        if (i not in used7 and j not in used7 and k not in used7 and l not in used7) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(2*max(backupsize,6)+min(backupsize,6)) and (six7>0 and backup7>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(2*max(backupsize,6)+min(backupsize,6)):
                                if backupsize==7 and backup7>=2 and six7>=1:
                                    backup7-=2
                                    six7-=1
                                    used7.update([i,j,k,l])
                                    fours7.append([i+1,l+1,k+1,j+1])
                                    init1.append([2,1])
                                elif backupsize==5 and six7>=2 and backup7>=1:
                                    six7-=2
                                    backup7-=1
                                    used7.update([i,j,k,l])
                                    fours7.append([i+1,l+1,k+1,j+1])
                                    init1.append([1,2])
                                if six7==0 and backup7==0:
                                    return fours7,init1
                                trial=compared_threes([backup7,six7],allocations,spaces,backupsize,used7,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours7,trial[1]+init1
    six8=six7
    backup8=backup7
    used8=used7.copy()
    fours8=fours7.copy()
    init2=init1.copy()
    for bound in range(lower,upperbound):
        six8=six7
        backup8=backup7
        used8=used7.copy()
        fours8=fours7.copy()
        init2=init1.copy()
        for i in range(0,len(spaces)-3):
            if six8==0 and backup8==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six8==0 and backup8==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six8==0 and backup8==0:
                        break
                    for l in range(k-1,i,-1):
                        if six8==0 and backup8==0:
                            break
                        if (i not in used8 and j not in used8 and k not in used8 and l not in used8) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(max(backupsize,6)+2*min(backupsize,6)) and (six8>0 and backup8>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(max(backupsize,6)+2*min(backupsize,6)):
                                if backupsize==7 and backup8>=1 and six8>=2:
                                    backup8-=1
                                    six8-=2
                                    used8.update([i,j,k,l])
                                    fours8.append([i+1,l+1,k+1,j+1])
                                    init2.append([1,2])
                                elif backupsize==5 and six8>=1 and backup8>=2:
                                    six8-=1
                                    backup8-=2
                                    used8.update([i,j,k,l])
                                    fours8.append([i+1,l+1,k+1,j+1])
                                    init2.append([2,1])
                                if six8==0 and backup8==0:
                                    return fours8,init2
                                trial=compared_threes([backup8,six8],allocations,spaces,backupsize,used8,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours8,trial[1]+init2
    six9=six8
    backup9=backup8
    fours9=fours8.copy()
    used9=used8.copy()
    init3=init2.copy()
    for bound in range(lower,upperbound):
        six9=six8
        backup9=backup8
        fours9=fours8.copy()
        used9=used8.copy()
        init3=init2.copy()
        for i in range(0,len(spaces)-3):
            if six9==0 and backup9==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six9==0 and backup9==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six9==0 and backup9==0:
                        break
                    for l in range(k-1,i,-1):
                        if six9==0 and backup9==0:
                            break
                        if (i not in used9 and j not in used9 and k not in used9 and l not in used9) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(3*min(backupsize,6)) and (six9>0 or backup9>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(3*max(backupsize,6)):
                                if backupsize==7 and six9>=3:
                                    six9-=3
                                    used9.update([i,j,k,l])
                                    fours9.append([i+1,l+1,k+1,j+1])
                                    init3.append([0,3])
                                elif backupsize==5 and backup9>=3:
                                    backup9-=3
                                    used9.update([i,j,k,l])
                                    fours9.append([i+1,l+1,k+1,j+1])
                                    init3.append([3,0])
                                if six9==0 and backup9==0:
                                    return fours9,init3
                                trial=compared_threes([backup9,six9],allocations,spaces,backupsize,used9,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours9,trial[1]+init3

    if six9==0 and backup9==0:
        return fours9,init3


    six10=six9
    backup10=backup9
    fours10=fours9.copy()
    used10=used9.copy()
    init4=init3.copy()
    for bound in range(lower,upperbound):
        six10=six9
        backup10=backup9
        fours10=fours9.copy()
        used10=used9.copy()
        init4=init3.copy()
        for i in range(0,len(spaces)-3):
            if six10==0 and backup10==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six10==0 and backup10==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six10==0 and backup10==0:
                        break
                    for l in range(k-1,i,-1):
                        if six10==0 and backup10==0:
                            break
                        if (i not in used10 and j not in used10 and k not in used10 and l not in used10) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(2*max(backupsize,6)) and (six10>0 or backup10>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(2*max(backupsize,6)):
                                if backupsize==7 and backup10>=2:
                                    backup10-=2
                                    used10.update([i,j,k,l])
                                    fours10.append([i+1,l+1,k+1,j+1])
                                    init4.append([2,0])
                                elif backupsize==5 and six10>=2:
                                    six10-=2
                                    used10.update([i,j,k,l])
                                    fours10.append([i+1,l+1,k+1,j+1])
                                    init4.append([0,2])
                                if six10==0 and backup10==0:
                                    return fours10,init4
                                trial=compared_threes([backup10,six10],allocations,spaces,backupsize,used10,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours10,trial[1]+init4
    six11=six10
    backup11=backup10
    used11=used10.copy()
    fours11=fours10.copy()
    init5=init4.copy()
    for bound in range(lower,upperbound):
        six11=six10
        backup11=backup10
        used11=used10.copy()
        fours11=fours10.copy()
        init5=init4.copy()
        for i in range(0,len(spaces)-3):
            if six11==0 and backup11==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six11==0 and backup11==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six11==0 and backup11==0:
                        break
                    for l in range(k-1,i,-1):
                        if six11==0 and backup11==0:
                            break
                        if (i not in used11 and j not in used11 and k not in used11 and l not in used11) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(max(backupsize,6)+min(backupsize,6)) and (six11>0 and backup11>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(max(backupsize,6)+min(backupsize,6)):
                                if backup11>=1 and six11>=1:
                                    backup11-=1
                                    six11-=1
                                    used11.update([i,j,k,l])
                                    fours11.append([i+1,l+1,k+1,j+1])
                                    init5.append([1,1])
                                if six11==0 and backup11==0:
                                    return fours11,init5
                                trial=compared_threes([backup11,six11],allocations,spaces,backupsize,used11,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours11,trial[1]+init5
    six12=six11
    backup12=backup11
    fours12=fours11.copy()
    used12=used11.copy()
    init6=init5.copy()
    for bound in range(lower,upperbound):
        six12=six11
        backup12=backup11
        fours12=fours11.copy()
        used12=used11.copy()
        init6=init5.copy()
        for i in range(0,len(spaces)-3):
            if six12==0 and backup12==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six12==0 and backup12==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six12==0 and backup12==0:
                        break
                    for l in range(k-1,i,-1):
                        if six12==0 and backup12==0:
                            break
                        if (i not in used12 and j not in used12 and k not in used12 and l not in used12) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(2*min(backupsize,6)) and (six12>0 or backup12>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(2*min(backupsize,6)):
                                if backupsize==7 and six12>=2:
                                    six12-=2
                                    used12.update([i,j,k,l])
                                    fours12.append([i+1,l+1,k+1,j+1])
                                    init6.append([0,2])
                                elif backupsize==5 and backup12>=2:
                                    backup12-=2
                                    used12.update([i,j,k,l])
                                    fours12.append([i+1,l+1,k+1,j+1])
                                    init6.append([2,0])
                                if six12==0 and backup12==0:
                                    return fours12,init6
                                trial=compared_threes([backup12,six12],allocations,spaces,backupsize,used12,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours12,trial[1]+init6

    if backup12==0 and six12==0:
        return fours12,init6

    six13=six12
    backup13=backup12
    fours13=fours12.copy()
    used13=used12.copy()
    init7=init6.copy()
    for bound in range(lower,upperbound):
        six13=six12
        backup13=backup12
        fours13=fours12.copy()
        used13=used12.copy()
        init7=init6.copy()
        for i in range(0,len(spaces)-3):
            if six13==0 and backup13==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six13==0 and backup13==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six13==0 and backup13==0:
                        break
                    for l in range(k-1,i,-1):
                        if six13==0 and backup13==0:
                            break
                        if (i not in used13 and j not in used13 and k not in used13 and l not in used13) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(max(backupsize,6)) and (six13>0 or backup13>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(max(backupsize,6)):
                                if backupsize==7 and backup13>=1:
                                    backup13-=1
                                    used13.update([i,j,k,l])
                                    fours13.append([i+1,l+1,k+1,j+1])
                                    init7.append([1,0])
                                elif backupsize==5 and six13>=1:
                                    six13-=1
                                    used13.update([i,j,k,l])
                                    fours13.append([i+1,l+1,k+1,j+1])
                                    init7.append([0,1])
                                if six13==0 and backup13==0:
                                    return fours13,init7
                                trial=compared_threes([backup13,six13],allocations,spaces,backupsize,used13,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours13,trial[1]+init7
    six14=six13
    backup14=backup13
    fours14=fours13.copy()
    used14=used13.copy()
    init8=init7.copy()
    for bound in range(lower,upperbound):
        six14=six13
        backup14=backup13
        fours14=fours13.copy()
        used14=used13.copy()
        init8=init7.copy()
        for i in range(0,len(spaces)-3):
            if six14==0 and backup14==0:
                break
            for j in range(len(spaces)-1,i+2,-1):
                if six14==0 and backup14==0:
                    break
                for k in range(j-1,i+1,-1):
                    if six14==0 and backup14==0:
                        break
                    for l in range(k-1,i,-1):
                        if six14==0 and backup14==0:
                            break
                        if (i not in used14 and j not in used14 and k not in used14 and l not in used14) and spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(min(backupsize,6)) and (six14>0 or backup14>0) and sum(allocations[i])+sum(allocations[j])+sum(allocations[k])+sum(allocations[l])<=bound:
                            if spaces[i]+spaces[k]+spaces[j]+spaces[l]>=(min(backupsize,6)):
                                if backupsize==7 and six14>=1:
                                    six14-=1
                                    used14.update([i,j,k,l])
                                    fours14.append([i+1,l+1,k+1,j+1])
                                    init8.append([0,1])
                                elif backupsize==5 and backup14>=1:
                                    backup14-=1
                                    used14.update([i,j,k,l])
                                    fours14.append([i+1,l+1,k+1,j+1])
                                    init8.append([1,0])
                                if six14==0 and backup14==0:
                                    return fours14,init8
                                trial=compared_threes([backup14,six14],allocations,spaces,backupsize,used14,[[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1],[boundlst[0][0],bound+1]])
                                if trial[1]:
                                    return trial[0]+fours14,trial[1]+init8

    if six14==0 and backup14==0:
        return fours14,init8

    return [],[]

def compared_fours(shortfall,allocations,spaces,backupsize=5,used=None,boundlst=None):
    results=fours(shortfall,allocations,spaces,backupsize,used,boundlst)
    results1=fours1(shortfall,allocations,spaces,backupsize,used,boundlst)
    maxnow=0
    maxnow1=0
    if results1==([],[]) and results==([],[]):
        return [],[]
    if results1==([],[]):
        return results
    if results==([],[]):
        return results1
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
        return results1
    else:
        return results