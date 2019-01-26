import pandas as pd
from Apriori_algorithm.Apriori import *


dataset = pd.read_csv('Data2.csv')


m = []
transactions_ = []
for i in range(0, len(dataset)):
    for j in range(0, 4):
        if str(dataset.values[i, j]) != 'nan':
            m.append(str(dataset.values[i, j]))

        transactions_.append(m)
    m = []
print(dataset)
print('\nTransactions : \n')
print(transactions_)
minsup = 0.2
minconf = 0.8

apriori = Apriori(transactions_, minsup, minconf)
apriori.iteration_of_frequent_itemset()
apriori.remove_itemset_lessThan_minsup()

for key, val in apriori.frequent_itemset.items():
    for itemset in val:
        apriori.calc_rule(itemset, itemset)

print('---------------------------------------------------------------------------------')

print('\nFrequent itemset : \n')
for key, val in apriori.frequent_itemset.items():
    for itemset in val:
        print('iteration : ' + str(key) + '    (' + ', '.join(itemset) + ')' + '   frequancy = ' + str((apriori.frequent_itemset_support[itemset])*len(dataset)) + '  support = ' + str(round(apriori.frequent_itemset_support[itemset], 3)) + '\n')

print('---------------------------------------------------------------------------------')

print('\nIgnore frequent itemset : \n')
for key, val in apriori.frequent_itemset_ignore.items():
    for itemset in val:
        print('iteration : ' + str(key) + '     (' + ', '.join(itemset) + ')' + '   frequancy = ' + str((apriori.frequent_itemset_support_ignore[itemset])*len(dataset)) + '  support = ' + str(round(apriori.frequent_itemset_support_ignore[itemset], 3)) + '\n')

print('---------------------------------------------------------------------------------')

print('\nRules : \n')
for rule in apriori.rule:
    LHS = rule[0][0]
    RHS = rule[0][1]
    confidence = rule[1]
    support = rule[2]
    print('(' + ', '.join(LHS) + ') => (' + '(' + ', '.join(RHS) + ')' + '  confidence = ' + str(round(confidence, 3)) + '    support = ' + str(round(support, 3)) + '\n')

print('---------------------------------------------------------------------------------')

print('\nIgnore rules : \n')
for rule in apriori.ignore_rule:
    LHS = rule[0][0]
    RHS = rule[0][1]
    confidence = rule[1]
    support = rule[2]
    print('(' + ', '.join(LHS) + ') => (' + '(' + ', '.join(RHS) + ')' + '  confidence = ' + str(round(confidence, 3)) + '    support = ' + str(round(support, 3)) + '\n')
