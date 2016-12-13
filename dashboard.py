from bigchaindb_driver import BigchainDB
from collections import Counter
import bdb_config

bdb = BigchainDB(bdb_config.host)


# Counter handles only positive numbers so results are always +1 to origin
# Input: (list)Verified transfer ID list/(list)list of candidate public keys
# Output: (Counter) stat['candidate_public_key'] : count of ballots
def make_statistics(validated_transfers, candidate_public_keys):
    stat = Counter(candidate_public_keys)
    for i in range(0, len(validated_transfers)):
        temp = bdb.transactions.retrieve(validated_transfers[i][0])
        stat[temp['transaction']['conditions'][0]['owners_after'][0]] += 1
    return stat


# -1 to Counter values for print
# Input : (Counter)
# Output: void
def print_statistics(stat):
    print("Ballot Count")
    temp = list(stat.keys())
    for i in range(0, len(temp)):
        print(temp[i] + " : " + str(stat[temp[i]] - 1))
