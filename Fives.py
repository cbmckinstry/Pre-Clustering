from Fours import *
def fives(shortfall, allocations1, spaces1, backupsize=5, used5=None):
    if used5 is None:
        used5 = set()
    allocations = []
    spaces = []
    for i in range(len(spaces1)):
        if spaces1[i] != 0:
            allocations.append(allocations1[i])
            spaces.append(spaces1[i])

    a = fours(shortfall, allocations, spaces, backupsize, used5)
    if a[1]:
        return a

    backup, six = shortfall[0], shortfall[1]
    used = used5.copy()
    fives_alloc = []
    init = []
    for m in range(1):
        backup, six = shortfall[0], shortfall[1]
        used = used5.copy()
        fives_alloc = []
        init = []
        for i in range(0, len(spaces) - 4):
            if backup == 0 and six == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup == 0 and six == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup == 0 and six == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup == 0 and six == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used and j not in used and k not in used and l not in used and n not in used and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= 4 * max(backupsize, 6))):
                                if backupsize == 7 and backup >= 4:
                                    backup -= 4
                                    used.update([i, j, k, l, n])
                                    fives_alloc.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init.append([4, 0])
                                elif backupsize == 5 and six >= 4:
                                    six -= 4
                                    used.update([i, j, k, l, n])
                                    fives_alloc.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init.append([0, 4])

                                if six==0 and backup==0:
                                    return fives_alloc,init

                                trial = fours([backup, six], allocations, spaces, backupsize, used)
                                if trial[1]:
                                    return trial[0] + fives_alloc, trial[1] + init

    backup1, six1 = backup, six
    used1 = used.copy()
    fives1 = fives_alloc.copy()
    init1 = init.copy()

    for m in range(1):
        backup1, six1 = backup, six
        used1 = used.copy()
        fives1 = fives_alloc.copy()
        init1 = init.copy()

        for i in range(0, len(spaces) - 4):
            if backup1 == 0 and six1 == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup1 == 0 and six1 == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup1 == 0 and six1 == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup1 == 0 and six1 == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used1 and j not in used1 and k not in used1 and l not in used1 and n not in used1 and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= 3 * max(backupsize, 6) + min(backupsize, 6))):
                                if backupsize == 7 and backup1 >= 3 and six1 >= 1:
                                    backup1 -= 3
                                    six1 -= 1
                                    used1.update([i, j, k, l, n])
                                    fives1.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init1.append([3, 1])
                                elif backupsize == 5 and six1 >= 3 and backup1 >= 1:
                                    six1 -= 3
                                    backup1 -= 1
                                    used1.update([i, j, k, l, n])
                                    fives1.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init1.append([1, 3])
                                if six1==0 and backup1==0:
                                    return fives1,init1
                                trial = fours([backup1, six1], allocations, spaces, backupsize,used1)
                                if trial[1]:
                                    return trial[0] + fives1, trial[1] + init1
    backup2, six2 = backup1, six1
    used2 = used1.copy()
    fives2 = fives1.copy()
    init2 = init1.copy()

    for m in range(1):
        backup2, six2 = backup1, six1
        used2 = used1.copy()
        fives2 = fives1.copy()
        init2 = init1.copy()

        for i in range(0, len(spaces) - 4):
            if backup2 == 0 and six2 == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup2 == 0 and six2 == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup2 == 0 and six2 == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup2 == 0 and six2 == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used2 and j not in used2 and k not in used2 and l not in used2 and n not in used2 and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= 2 * max(backupsize, 6) + 2 * min(backupsize, 6))):
                                if backupsize == 7 and backup2 >= 2 and six2 >= 2:
                                    backup2 -= 2
                                    six2 -= 2
                                    used2.update([i, j, k, l, n])
                                    fives2.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init2.append([2, 2])
                                elif backupsize == 5 and six2 >= 2 and backup2 >= 2:
                                    six2 -= 2
                                    backup2 -= 2
                                    used2.update([i, j, k, l, n])
                                    fives2.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init2.append([2, 2])
                                if six2==0 and backup2==0:
                                    return fives2,init2
                                trial = fours([backup2, six2], allocations, spaces, backupsize,used2)
                                if trial[1]:
                                    return trial[0] + fives2, trial[1] + init2

    backup3, six3 = backup2, six2
    used3 = used2.copy()
    fives3 = fives2.copy()
    init3 = init2.copy()

    for m in range(1):
        backup3, six3 = backup2, six2
        used3 = used2.copy()
        fives3 = fives2.copy()
        init3 = init2.copy()

        for i in range(0, len(spaces) - 4):
            if backup3 == 0 and six3 == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup3 == 0 and six3 == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup3 == 0 and six3 == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup3 == 0 and six3 == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used3 and j not in used3 and k not in used3 and l not in used3 and n not in used3 and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= max(backupsize, 6) + 3 * min(backupsize, 6))):
                                if backupsize == 7 and backup3 >= 1 and six3 >= 3:
                                    backup3 -= 1
                                    six3 -= 3
                                    used3.update([i, j, k, l, n])
                                    fives3.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init3.append([1, 3])
                                elif backupsize == 5 and six3 >= 3 and backup3 >= 1:
                                    six3 -= 3
                                    backup3 -= 1
                                    used3.update([i, j, k, l, n])
                                    fives3.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init3.append([1, 3])
                                if six3==0 and backup3==0:
                                    return fives3,init3
                                trial = fours([backup3, six3], allocations, spaces, backupsize,used3)
                                if trial[1]:
                                    return trial[0] + fives3, trial[1] + init3

    backup4, six4 = backup3, six3
    used4 = used3.copy()
    fives4 = fives3.copy()
    init4 = init3.copy()

    for m in range(1):
        backup4, six4 = backup3, six3
        used4 = used3.copy()
        fives4 = fives3.copy()
        init4 = init3.copy()

        for i in range(0, len(spaces) - 4):
            if backup4 == 0 and six4 == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup4 == 0 and six4 == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup4 == 0 and six4 == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup4 == 0 and six4 == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used4 and j not in used4 and k not in used4 and l not in used4 and n not in used4 and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= 4 * min(backupsize, 6))):
                                if backupsize==7 and six4 >= 4:
                                    six4 -= 4
                                    used4.update([i, j, k, l, n])
                                    fives4.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init4.append([0, 4])
                                elif backupsize==5 and backup4>=4:
                                    backup4-=4
                                    used4.update([i, j, k, l, n])
                                    fives4.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init4.append([4, 0])
                                if six4==0 and backup4==0:
                                    return fives4,init4
                                trial = fours([backup4, six4], allocations, spaces, backupsize, used4)
                                if trial[1]:
                                    return trial[0] + fives4, trial[1] + init4

    if backup4==0 and six4==0:
        return fives4,init4

    backup5, six5 = backup4, six4
    used5 = used4.copy()
    fives5 = fives4.copy()
    init5 = init4.copy()

    for m in range(1):
        backup5, six5 = backup4, six4
        used5 = used4.copy()
        fives5 = fives4.copy()
        init5 = init4.copy()

        for i in range(0, len(spaces) - 4):
            if backup5 == 0 and six5 == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup5 == 0 and six5 == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup5 == 0 and six5 == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup5 == 0 and six5 == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used5 and j not in used5 and k not in used5 and l not in used5 and n not in used5 and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= 3 * max(backupsize, 6))):
                                if backupsize == 7 and backup5 >= 3:
                                    backup5 -= 3
                                    used5.update([i, j, k, l, n])
                                    fives5.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init5.append([3, 0])
                                elif backupsize == 5 and six5 >= 3:
                                    six5 -= 3
                                    used5.update([i, j, k, l, n])
                                    fives5.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init5.append([0, 3])
                                if six5==0 and backup5==0:
                                    return fives5,init5
                                trial = fours([backup5, six5], allocations, spaces, backupsize, used5)
                                if trial[1]:
                                    return trial[0] + fives5, trial[1] + init5
    backup6, six6 = backup5, six5
    used6 = used5.copy()
    fives6 = fives5.copy()
    init6 = init5.copy()

    for m in range(1):
        backup6, six6 = backup5, six5
        used6 = used5.copy()
        fives6 = fives5.copy()
        init6 = init5.copy()

        for i in range(0, len(spaces) - 4):
            if backup6 == 0 and six6 == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup6 == 0 and six6 == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup6 == 0 and six6 == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup6 == 0 and six6 == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used6 and j not in used6 and k not in used6 and l not in used6 and n not in used6 and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= 2 * max(backupsize, 6) + 1 * min(backupsize, 6))):
                                if backupsize == 7 and backup6 >= 2 and six6 >= 1:
                                    backup6 -= 2
                                    six6 -= 1
                                    used6.update([i, j, k, l, n])
                                    fives6.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init6.append([2, 1])
                                elif backupsize == 5 and six6 >= 2 and backup6 >= 1:
                                    six6 -= 2
                                    backup6 -= 1
                                    used6.update([i, j, k, l, n])
                                    fives6.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init6.append([1, 2])
                                if six6==0 and backup6==0:
                                    return fives6,init6
                                trial = fours([backup6, six6], allocations, spaces, backupsize, used6)
                                if trial[1]:
                                    return trial[0] + fives6, trial[1] + init6

    backup7, six7 = backup6, six6
    used7 = used6.copy()
    fives7 = fives6.copy()
    init7 = init6.copy()

    for m in range(1):
        backup7, six7 = backup6, six6
        used7 = used6.copy()
        fives7 = fives6.copy()
        init7 = init6.copy()

        for i in range(0, len(spaces) - 4):
            if backup7 == 0 and six7 == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup7 == 0 and six7 == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup7 == 0 and six7 == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup7 == 0 and six7 == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used7 and j not in used7 and k not in used7 and l not in used7 and n not in used7 and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= 1 * max(backupsize, 6) + 2 * min(backupsize, 6))):
                                if backupsize == 7 and backup7 >= 1 and six7 >= 2:
                                    backup7 -= 1
                                    six7 -= 2
                                    used7.update([i, j, k, l, n])
                                    fives7.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init7.append([1, 2])
                                elif backupsize == 5 and six7 >= 1 and backup7 >= 2:
                                    six7 -= 1
                                    backup7 -= 2
                                    used7.update([i, j, k, l, n])
                                    fives7.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init7.append([2, 1])
                                if six7==0 and backup7==0:
                                    return fives7,init7
                                trial = fours([backup7, six7], allocations, spaces, backupsize, used7)
                                if trial[1]:
                                     return trial[0] + fives7, trial[1] + init7

    backup8, six8 = backup7, six7
    used8 = used7.copy()
    fives8 = fives7.copy()
    init8 = init7.copy()

    for m in range(1):
        backup8, six8 = backup7, six7
        used8 = used7.copy()
        fives8 = fives7.copy()
        init8 = init7.copy()

        for i in range(0, len(spaces) - 4):
            if backup8 == 0 and six8 == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup8 == 0 and six8 == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup8 == 0 and six8 == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup8 == 0 and six8 == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used8 and j not in used8 and k not in used8 and l not in used8 and n not in used8 and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= 0 * max(backupsize, 6) + 3 * min(backupsize, 6))):
                                if backupsize == 7 and six8 >= 3:
                                    six8 -= 3
                                    used8.update([i, j, k, l, n])
                                    fives8.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init8.append([0, 3])
                                elif backupsize == 5 and backup8 >= 3:
                                    backup8 -= 3
                                    used8.update([i, j, k, l, n])
                                    fives8.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init8.append([3, 0])
                                if six8==0 and backup8==0:
                                    return fives8,init8
                                trial = fours([backup8, six8], allocations, spaces, backupsize, used8)
                                if trial[1]:
                                    return trial[0] + fives8, trial[1] + init8

    if backup8 == 0 and six8 == 0:
        return fives8, init8


    backup9, six9 = backup8, six8
    used9 = used8.copy()
    fives9 = fives8.copy()
    init9 = init8.copy()

    for m in range(1):
        backup9, six9 = backup8, six8
        used9 = used8.copy()
        fives9 = fives8.copy()
        init9 = init8.copy()

        for i in range(0, len(spaces) - 4):
            if backup9 == 0 and six9 == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup9 == 0 and six9 == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup9 == 0 and six9 == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup9 == 0 and six9 == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used9 and j not in used9 and k not in used9 and l not in used9 and n not in used9 and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= 2 * max(backupsize, 6))):
                                if backupsize == 7 and backup9 >= 2:
                                    backup9 -= 2
                                    used9.update([i, j, k, l, n])
                                    fives9.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init9.append([2, 0])
                                elif backupsize == 5 and six9 >= 2:
                                    six9 -= 2
                                    used9.update([i, j, k, l, n])
                                    fives9.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init9.append([0, 2])
                                if six9==0 and backup9==0:
                                    return fives9,init9
                                trial = fours([backup9, six9], allocations, spaces, backupsize, used9)
                                if trial[1]:
                                    return trial[0] + fives9, trial[1] + init9

    backup10, six10 = backup9, six9
    used10 = used9.copy()
    fives10 = fives9.copy()
    init10 = init9.copy()

    for m in range(1):
        backup10, six10 = backup9, six9
        used10 = used9.copy()
        fives10 = fives9.copy()
        init10 = init9.copy()

        for i in range(0, len(spaces) - 4):
            if backup10 == 0 and six10 == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup10 == 0 and six10 == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup10 == 0 and six10 == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup10 == 0 and six10 == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used10 and j not in used10 and k not in used10 and l not in used10 and n not in used10 and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= 1 * max(backupsize, 6) + 1 * min(backupsize, 6))):
                                if backupsize == 7 and backup10 >= 1 and six10 >= 1:
                                    backup10 -= 1
                                    six10 -= 1
                                    used10.update([i, j, k, l, n])
                                    fives10.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init10.append([1, 1])
                                elif backupsize == 5 and six10 >= 1 and backup10 >= 1:
                                    six10 -= 1
                                    backup10 -= 1
                                    used10.update([i, j, k, l, n])
                                    fives10.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init10.append([1, 1])
                                if six10==0 and backup10==0:
                                    return fives10,init10
                                trial = fours([backup10, six10], allocations, spaces, backupsize,used10)
                                if trial[1]:
                                    return trial[0] + fives10, trial[1] + init10

    backup11, six11 = backup10, six10
    used11 = used10.copy()
    fives11 = fives10.copy()
    init11 = init10.copy()

    for m in range(1):
        backup11, six11 = backup10, six10
        used11 = used10.copy()
        fives11 = fives10.copy()
        init11 = init10.copy()

        for i in range(0, len(spaces) - 4):
            if backup11 == 0 and six11 == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup11 == 0 and six11 == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup11 == 0 and six11 == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup11 == 0 and six11 == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used11 and j not in used11 and k not in used11 and l not in used11 and n not in used11 and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= 2 * min(backupsize, 6))):
                                if backupsize == 7 and six11 >= 2:
                                    six11 -= 2
                                    used11.update([i, j, k, l, n])
                                    fives11.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init11.append([0, 2])
                                elif backupsize == 5 and backup11 >= 2:
                                    backup11 -= 2
                                    used11.update([i, j, k, l, n])
                                    fives11.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init11.append([2, 0])
                                if six11==0 and backup11==0:
                                    return fives11,init11
                                trial = fours([backup11, six11], allocations, spaces, backupsize, used11)
                                if trial[1]:
                                     return trial[0] + fives11, trial[1] + init11
    if backup11 == 0 and six11 == 0:
        return fives11, init11

    backup12, six12 = backup11, six11
    used12 = used11.copy()
    fives12 = fives11.copy()
    init12 = init11.copy()

    for m in range(1):
        backup12, six12 = backup11, six11
        used12 = used11.copy()
        fives12 = fives11.copy()
        init12 = init11.copy()

        for i in range(0, len(spaces) - 4):
            if backup12 == 0 and six12 == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup12 == 0 and six12 == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup12 == 0 and six12 == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup12 == 0 and six12 == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used12 and j not in used12 and k not in used12 and l not in used12 and n not in used12 and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= 1 * max(backupsize, 6))):
                                if backupsize == 7 and backup12 >= 1:
                                    backup12 -= 1
                                    used12.update([i, j, k, l, n])
                                    fives12.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init12.append([1, 0])
                                elif backupsize == 5 and six12 >= 1:
                                    six12 -= 1
                                    used12.update([i, j, k, l, n])
                                    fives12.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init12.append([0, 1])
                                if six12==0 and backup12==0:
                                    return fives12,init12
                                trial = fours([backup12, six12], allocations, spaces, backupsize, used12)
                                if trial[1]:
                                    return trial[0] + fives12, trial[1] + init12

    backup13, six13 = backup12, six12
    used13 = used12.copy()
    fives13 = fives12.copy()
    init13 = init12.copy()

    for m in range(1):
        backup13, six13 = backup12, six12
        used13 = used12.copy()
        fives13 = fives12.copy()
        init13 = init12.copy()

        for i in range(0, len(spaces) - 4):
            if backup13 == 0 and six13 == 0:
                break
            for j in range(len(spaces) - 1, i + 3, -1):
                if backup13 == 0 and six13 == 0:
                    break
                for k in range(j - 1, i + 2, -1):
                    if backup13 == 0 and six13 == 0:
                        break
                    for l in range(k - 1, i + 1, -1):
                        if backup13 == 0 and six13 == 0:
                            break
                        for n in range(l - 1, i, -1):
                            if (i not in used13 and j not in used13 and k not in used13 and l not in used13 and n not in used13 and (spaces[i] + spaces[j] + spaces[k] + spaces[l] + spaces[n] >= 1 * min(backupsize, 6))):
                                if backupsize == 7 and six13 >= 1:
                                    six13 -= 1
                                    used13.update([i, j, k, l, n])
                                    fives13.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init13.append([0, 1])
                                elif backupsize == 5 and backup13 >= 1:
                                    backup13 -= 1
                                    used13.update([i, j, k, l, n])
                                    fives13.append([i + 1, n + 1, l + 1, k + 1, j + 1])
                                    init13.append([1, 0])
                                if six13==0 and backup13==0:
                                    return fives13,init13
                                trial = fours([backup13, six13], allocations, spaces, backupsize,used13)
                                if trial[1]:
                                    return trial[0] + fives13, trial[1] + init13
    if backup13 == 0 and six13 == 0:
        return fives13, init13

    return [],[]
