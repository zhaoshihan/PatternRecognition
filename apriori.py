from dataset import getSimpleTestData,getRandomData

def preprocess(data):
    itemsets = []
    for i in range(len(data)):
        itemset = set(data[i])    # remove duplicate elements
        itemsets.append(itemset)
    return itemsets

def getSupport(dataset, itemsets, minSupport):
    support = {}
    for data in dataset:
        for itemset in itemsets:
            listItemset = list(itemset)
            listItemset.sort()
            tupleItemset = tuple(listItemset) 
            if itemset.issubset(data):
                support[tupleItemset] = support.get(tupleItemset,0) + 1
    return {itemset:count for itemset,count in support.items() if count >= minSupport}

def print_rules(rules):
    print('Association Rules:')
    for rule in rules:
        print('%s ==> %s' % (rule[0], rule[1]))

def print_frequent_itemset(result):
    print('Frequent Itemset:')
    for s in result:
        setstr = ''
        for item in s:
            setstr += str(item) + ' '
        print(setstr)

def isJoinable(s1, s2):
    if len(s1) != len(s2):
        return False
    if len(s1) == 0:
        return False
    for i in range(len(s1)-1):
        if s1[i] != s2[i]:
            return False
    if s1[-1] >= s2[-1]:
        return False
    return True

def getAllSubsets(itemset):
    if len(itemset) == 0:
        return []
    result = [[]]
    for item in itemset:
        newSet = [ oldSet + [item] for oldSet in result]
        result.extend(newSet)
    result = result[1:-1] # remove empty subset and itemset itself
    for i in range(len(result)):
        result[i].sort()
    return result
    

def getAssociaionRules(frequent_itemset, support, minConfidenceRatio):
    rules = []
    for itemset in frequent_itemset:
        subsets = getAllSubsets(itemset)
        for subset in subsets:
            confidence = support[tuple(itemset)] / support[tuple(subset)]
            if confidence >= minConfidenceRatio:
                diffset = set(itemset).difference(set(subset))
                print('%s ==> %s' % (tuple(subset), tuple(diffset)))
                rules.append((tuple(subset),tuple(diffset)))
    return rules


def apriori(dataset, minSupportRatio, minConfidenceRatio):
    dataset = preprocess(dataset)
    frequent_itemset = []
    support = {}
    itemsets = set()
    for data in dataset:
        itemsets |= data
    itemsets = [set([itemset,]) for itemset in itemsets]
    minSupport = int(minSupportRatio * len(dataset))
    while True:
        L = getSupport(dataset, itemsets, minSupport)
        # print(L)
        support.update(L)
        # print(support)
        if len(L.items()) == 0: 
            break
        frequent_itemset.extend(L.keys())
        itemsets = []
        for set1 in L.keys():
            for set2 in L.keys():
                if isJoinable(set1, set2):
                    itemsets.append(set(set1) | set(set2))
    
    rules = getAssociaionRules(frequent_itemset, support, minConfidenceRatio)
    return frequent_itemset, rules





if __name__ =='__main__':
    # data = getSimpleTestData()
    data = getRandomData()
    # print(data)
    frequent_itemset, rules = apriori(data,0.7,0.7)
    
    print_frequent_itemset(frequent_itemset)
    # print_rules(rules)
    print(len(frequent_itemset))
    print(len(rules))





