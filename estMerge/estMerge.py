from collections import defaultdict
from itertools import chain, combinations


def get_support(item, transaction_list, frequent_set):
    return float(frequent_set[item]) / len(transaction_list)


def join_set(item_set, length):
    return set(
        [i.union(j) for i in item_set for j in item_set if len(i.union(j)) == length]
    )


def return_items_with_min_support(item_set, transaction_list, min_support, freq_set):
    _item_set = set()
    _removed_item_set = set()
    local_set = defaultdict(int)

    for item in item_set:
        for transaction in transaction_list:
            if item.issubset(transaction):
                freq_set[item] += 1
                local_set[item] += 1

    transaction_list_length = len(transaction_list)

    for item, count in local_set.items():
        support = float(count) / transaction_list_length

        if support >= min_support:
            _item_set.add(item)
        else:
            _removed_item_set.add(item)

    return _item_set, _removed_item_set


def prepare_single_set(transaction_list):
    item_set = set()

    for transaction in transaction_list:
        for item in transaction:
            item_set.add(frozenset([int(item)]))

    return item_set


def filter_set_by_set(first_set, second_set):
    _final_set = set()

    for item in first_set:
        if item not in second_set:
            _final_set.add(item)

    return _final_set



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
                    confidence = get_support(item, transaction_list, frequent_set) / get_support(element,
                                                                                                 transaction_list,
                                                                                                 frequent_set)
                    if confidence >= min_conf:
                        to_ret_rules.append(((tuple(element), tuple(remain)), confidence))
    return to_ret_items, to_ret_rules


def print_results(items, rules):
    # for item, support in sorted(items, key=lambda x: x[1]):
    #     print("item: %s , %.3f" % (str(item), support))
    print("\n------------------------ RULES:")
    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))


def run_est_merge(min_support, min_conf, transaction_list, transaction_list_sample):
    l_dict = dict()
    c_dict = dict()
    c_1_dict = dict()
    c_2_dict = dict()

    support_dict = defaultdict(int)
    estimated_support_dict = defaultdict(int)

    k = 2

    print("Processing iteration: 1")
    single_set = prepare_single_set(transaction_list)

    l_dict[1], _ = return_items_with_min_support(single_set, transaction_list, min_support, support_dict)
    c_dict[1] = l_dict[1]
    c_2_dict[1] = set([])

    return_items_with_min_support(single_set, transaction_list_sample, min_support, estimated_support_dict)

    while l_dict[k - 1] != set([]) or c_2_dict[k - 1] != set([]):
        print("Processing iteration: ", k)
        c_dict[k] = join_set(l_dict[k - 1].union(c_2_dict[k - 1]), k)
        c_dict_k_with_min_sup, _ = return_items_with_min_support(c_dict[k], transaction_list_sample,
                                                                 min_support, estimated_support_dict)
        c_dict_k_parents_with_min_sup, _ = return_items_with_min_support(join_set(c_dict[k - 1], k), transaction_list_sample,
                                                                 min_support, estimated_support_dict)

        c_1_dict[k] = c_dict_k_with_min_sup.union(c_dict_k_parents_with_min_sup)
        l_dict[k], removed_set = return_items_with_min_support(c_1_dict[k], transaction_list, min_support,
                                                       support_dict)

        c_dict[k] = filter_set_by_set(c_dict[k], removed_set)
        c_2_dict[k] = filter_set_by_set(c_dict[k], c_1_dict[k])
        set_to_extend_l, _ = return_items_with_min_support(c_2_dict[k - 1], transaction_list, min_support, support_dict)
        l_dict[k - 1] = l_dict[k - 1].union(set_to_extend_l)

        k += 1

    item, rules = mk_rules(l_dict, min_conf, transaction_list, support_dict)

    print_results(item, rules)
    