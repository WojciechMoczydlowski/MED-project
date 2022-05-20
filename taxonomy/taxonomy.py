def read_taxonomy_data(file_name):
    taxonomy = dict()

    with open(file_name) as f:
        for line in f:  # read rest of lines
            arr = []

            for x in line.split(","):
                arr.append(int(x))

            taxonomy[arr[0]] = arr[1]

    return taxonomy


def extend_data_with_taxonomy(transaction_list, taxonomy):
    _transaction_list = list()

    for transaction in transaction_list:
        arr = set()

        for item in transaction:
            arr.add(item)
            ancestor = taxonomy.get(item)

            while ancestor is not None:
                arr.add(ancestor)
                ancestor = taxonomy.get(ancestor)

        transaction = frozenset(arr)
        _transaction_list.append(transaction)

    return _transaction_list


