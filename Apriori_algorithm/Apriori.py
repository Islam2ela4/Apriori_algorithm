from collections import defaultdict
from Apriori_algorithm.cached import *
from itertools import combinations


class Apriori():

    def __init__(self, transaction, minsup, minconf, correct_items=None):

        self.transaction = transaction
        self.transaction_length = len(transaction)
        self.minsup = minsup
        self.minconf = minconf
        self.correct_items = correct_items
        self.frequent_itemset = dict()
        self.frequent_itemset_support = dict()
        self.rule = []

        self.frequent_itemset_ignore = dict()
        self.frequent_itemset_support_ignore = dict()

        self.ignore_rule = []

    @cached_property
    def items(self):
        itemset = set()
        for i in self.transaction:
            for j in i:
                itemset.add(j)
        return itemset



    def itemset_greaterThanOrEqual_minsup(self, itemset):

        count = defaultdict(int)
        for item in itemset:
            for transact in self.transaction:
                if item.issubset(transact):
                    count[item] += 1

        result = set()
        ignore = set()
        for item, count in count.items():
            support = float(count) / self.transaction_length  # count / #of transaction
            if support >= self.minsup:
                result.add(item)
                self.frequent_itemset_support[item] = support
            else:
                ignore.add(item)
                self.frequent_itemset_support_ignore[item] = support

        return result, ignore


    def remove_itemset_lessThan_minsup(self):

        if self.correct_items is None:
            return

        removed_item = []
        for key, val in self.frequent_itemset.items():
            for itemset in val:
                if not self.correct_items.issubset(itemset):
                    removed_item.append((key, itemset))

        for (key, itemset) in removed_item:
            self.frequent_itemset[key].remove(itemset)


    def Concatenation_new_itemset(self, itemset, length):
        new_itemset = set()
        for x in itemset:
            for y in itemset:
                if len(x.union(y)) >= length:
                    new_itemset.add(x.union(y))
        return new_itemset


    def iteration_of_frequent_itemset(self):
        iteration = 1
        current_itemset = []
        for item in self.items:
            current_itemset.append(frozenset([item]))

        self.frequent_itemset[iteration], self.frequent_itemset_ignore[iteration] = self.itemset_greaterThanOrEqual_minsup(current_itemset)

        while True:
            iteration += 1
            current_itemset = self.Concatenation_new_itemset(current_itemset, iteration)
            current_itemset, itemset_ignore = self.itemset_greaterThanOrEqual_minsup(current_itemset)
            if current_itemset != set([]):
                self.frequent_itemset[iteration] = current_itemset
                self.frequent_itemset_ignore[iteration] = itemset_ignore
            else:
                break

        return self.frequent_itemset, self.frequent_itemset_ignore



    def calc_rule(self, itemset, itemset_constant):
        if len(itemset) < 2:
            return

        for element in combinations(list(itemset), 1):
            LHS_X = itemset - set(element)    # set because itemset is object from set
            confidence = self.frequent_itemset_support[itemset_constant] / self.frequent_itemset_support[LHS_X]
            support = self.frequent_itemset_support[itemset_constant]
            if confidence >= self.minconf:
                rule = ((LHS_X, itemset - LHS_X), confidence, support)
                if rule not in self.rule:
                    self.rule.append(rule)
                    self.calc_rule(LHS_X, itemset_constant)
            else:
                ignore_rule = ((LHS_X, itemset - LHS_X), confidence, support)
                self.ignore_rule.append(ignore_rule)
                self.calc_rule(LHS_X, itemset_constant)

