import itertools


def read_transaction_data(file_name):
    transaction_list = list()

    with open(file_name) as f:
        for line in f:  # read rest of lines
            arr = []

            for x in line.split():
                arr.append(int(x))

            transaction = frozenset(arr)
            transaction_list.append(transaction)

    return transaction_list


def prepare_transaction_sample(transaction_list, sample_value):
    sample_transaction_list_amount = round(sample_value * len(transaction_list))

    return set(itertools.islice(transaction_list, sample_transaction_list_amount))




