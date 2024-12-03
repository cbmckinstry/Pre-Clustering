import itertools

def findrange(vehlist):
    final=[]
    for item in vehlist:
        redo=[]
        for x in range(item//5+1):
            redo.append([x,(item-(5*x))//6])
        final.append(redo)
    return final

def find_all_combinations(ent):
    return list(itertools.product(*ent))

def valid(vehlist,required):
    poss=find_all_combinations(findrange(vehlist))
    for item in poss:
        sum1=0
        sum2=0
        for spec in item:
            sum1+=spec[0]
            sum2+=spec[1]
        if sum1>=required[0] and sum2>=required[1]:
            return True
    return False
def validlist(vehlist,required):
    poss=find_all_combinations(findrange(vehlist))
    finposs=[]
    possout=[]
    for item in poss:
        sum1=0
        sum2=0
        for spec in item:
            sum1+=spec[0]
            sum2+=spec[1]
            if sum1>=required[0] and sum2>=required[1]:
                if [sum1,sum2] not in finposs:
                    finposs.append([sum1,sum2])
                    possout.append(item)
    return [finposs,possout]

def needed(vehlist,pers5,pers6):
    largelist=validlist(vehlist,[0,0])[0]
    largelist1=[]
    other=[]
    examples=validlist(vehlist,[0,0])[1]
    for elem in range(len(largelist)):
        largelist1.append([pers5-largelist[elem][0],pers6-largelist[elem][1]])
    for newelem in range(len(largelist)):
        if largelist1[newelem][0]<0:
            largelist1[newelem][0]=0
        if largelist1[newelem][1]<0:
            largelist1[newelem][1]=0
    singlelarge=[]
    for newer in range(len(largelist1)):
        singlelarge.append(largelist1[newer][0]+largelist1[newer][1])
    final=[]
    currentmin=min(singlelarge)
    for diff in range(len(singlelarge)):
        if singlelarge[diff]==currentmin and largelist1[diff] not in final:
            final.append(largelist1[diff])
            other.append(examples[diff])
    return [final,other]

def spaces(examplelist,vehlist):
    final=[]
    for item in range(len(examplelist)):
        final.append(vehlist[item]-(5*examplelist[item][0]+6*examplelist[item][1]))
    return final