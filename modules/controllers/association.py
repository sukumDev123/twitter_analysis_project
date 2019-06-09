def createC1(dataSet):
    print("create c1\n")
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])

    C1.sort()
    return list(map(frozenset, C1))  #use frozen set so we


    #can use it as a key in a dict
def scanD(D, Ck, minSupport):
    print("scanD\n")

    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt: ssCnt[can] = 1
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData


def aprioriGen(Lk, k):  #creates Ck
    print("aprioriGen\n")

    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:  #if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j])  #set union
    return retList


def apriori(dataSet, minSupport=0.5):
    print("apriori\n")

    C1 = (createC1(dataSet))
    D = (list(map(set, dataSet)))
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minSupport)  #scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


def calcConfAndLiff(freqSet, H, supportData, brl, minConf=0.7):
    print("calcConfAndLiff\n")

    prunedH = []  #create new list to return
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet -
                                                  conseq]  #calc confidence
        liff = supportData[freqSet] / (supportData[freqSet - conseq] *
                                       supportData[conseq])

        if conf >= minConf:
            print("ss {} {}".format(freqSet, conseq), freqSet - conseq, '-->',
                  conseq, 'conf:', conf, ' liff: ', liff)
            brl.append((freqSet - conseq, conseq, conf, liff))
            prunedH.append(conseq)
    return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    print('rulesFromConseq\n')
    m = len(H[0])
    if (len(freqSet) > (m + 1)):  #try further merging
        Hmp1 = aprioriGen(H, m + 1)  #create Hm+1 new candidates
        Hmp1 = calcConfAndLiff(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):  #need at least two sets to merge
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


def generateRules(L, supportData,
                  minConf=0.7):  #supportData is a dict coming from scanD
    print('generateRules\n')

    bigRuleList = []
    for i in range(1, len(L)):  #only get the sets with two or more items
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConfAndLiff(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList
