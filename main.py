from efficient_apriori import apriori
from apriori.apriori import run_apriori
from taxonomy.taxonomy import read_taxonomy_data, extend_data_with_taxonomy
from transactions.transactions import read_transaction_data, prepare_transaction_sample

support = 0.4
confidence = 0.3

# test_transaction_data = read_transaction_data("./data/data.txt")
transaction_data = read_transaction_data("./data/data.txt")
taxonomy = read_taxonomy_data("./data/taxonomy.txt")

extended_transaction_data = extend_data_with_taxonomy(transaction_data, taxonomy)

print("------APRIORI------")

run_apriori(support, confidence, extended_transaction_data)

print("\n------EFFICIENT APRIORI------")

_, rules = apriori(extended_transaction_data, min_support=support, min_confidence=confidence)

print(rules)
print("Rules amount: ", len(rules))
