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
