from apriori.apriori import run_apriori
from taxonomy.taxonomy import read_taxonomy_data, extend_data_with_taxonomy
from transactions.transactions import read_transaction_data

transaction_data = read_transaction_data("./data/test.txt")
taxonomy = read_taxonomy_data("./data/taxonomy.txt")
extended_transaction_data = extend_data_with_taxonomy(transaction_data, taxonomy)

run_apriori(0.2, 0.3, extended_transaction_data)

print("First commit")
