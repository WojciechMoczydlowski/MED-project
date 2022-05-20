from collections import defaultdict
from itertools import chain, combinations

# from apriori.taxonomy import read_taxonomy_data
from transactions.transactions import read_transaction_data


def get_support(item, transaction_list, frequent_set):
    return float(frequent_set[item]) / len(transaction_list)


def join_set(item_set, length):
    return set(
        [i.union(j) for i in item_set for j in item_set if len(i.union(j)) == length]
    )


def return_items_with_min_support(item_set, transaction_list, min_support, freq_set):
    _item_set = set()
    local_set = defaultdict(int)

    for item in item_set:
        for transaction in transaction_list:
            a = item.issubset(transaction)
            if item.issubset(transaction):
                freq_set[item] += 1
                local_set[item] += 1

    transaction_list_length = len(transaction_list)

    for item, count in local_set.items():
        support = float(count) / transaction_list_length

        if support >= min_support:
            _item_set.add(item)

    return _item_set


def prepare_single_set(transaction_list):
    item_set = set()

    for transaction in transaction_list:
        for item in transaction:
            item_set.add(frozenset([int(item)]))

    return item_set


def mk_subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def mk_rules(large_set, min_conf, transaction_list, frequent_set):
    to_ret_items = []

    for key, value in large_set.items():
        to_ret_items.extend([(tuple(item), get_support(item, transaction_list, frequent_set)) for item in value])

    to_ret_rules = []

    for key, value in list(large_set.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in mk_subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = get_support(item, transaction_list, frequent_set) / get_support(element, transaction_list, frequent_set)
                    if confidence >= min_conf:
                        to_ret_rules.append(((tuple(element), tuple(remain)), confidence))
    return to_ret_items, to_ret_rules


def print_results(items, rules):
    for item, support in sorted(items, key=lambda x: x[1]):
        print("item: %s , %.3f" % (str(item), support))
    print("\n------------------------ RULES:")
    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))


def run_apriori(min_support, min_conf, transaction_list):

    item_set = prepare_single_set(transaction_list)

    frequent_set = defaultdict(int)
    large_set = dict()

    print("Processing iteration: 1")
    one_c_set = return_items_with_min_support(item_set, transaction_list, min_support, frequent_set)

    current_l_set = one_c_set
    k = 2

    while current_l_set != set([]):
        print("Processing iteration:", k)
        large_set[k - 1] = current_l_set
        current_c_set = join_set(current_l_set, k)
        current_l_set = return_items_with_min_support(current_c_set, transaction_list, min_support, frequent_set)
        k += 1

    item, rules = mk_rules(large_set, min_conf, transaction_list, frequent_set)

    print_results(item, rules)


# run_apriori(0.01, 0.01)


# tax = read_taxonomy_data()

print("Tax")