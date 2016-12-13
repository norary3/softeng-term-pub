import time
import datetime
import bdb_config
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

bdb = BigchainDB(bdb_config.host)
delay = 1  # Artificial Delay Constant


# signing_key = private
# verifying_key = public

# Create Voter Assets with Ballot asset implemented
# Input: (int)number of voters to make / (str) corresponding poll's id
# Output: (dict){ [(str)'voter_ids'][(int)index]: Created Asset IDs
#                 [(str)'signing_keys'][(int)index]: Voter private keys
def make_voter(voter_num, poll_id):
    voter_dict = {'voter_ids': {}, 'signing_keys': {}}  # id:private
    for i in range(0, voter_num):
        ballot = {'data': {'vote': {'poll_id': poll_id,
                                    'serial': i,
                                    'time_stamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, }, }
        metadata = {'poll_id': poll_id}
        temp = generate_keypair()
        prepared_creation_tx = bdb.transactions.prepare(operation='CREATE',
                                                        owners_before=temp.verifying_key,
                                                        asset=ballot,
                                                        metadata=metadata, )
        fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx,
                                                         private_keys=temp.signing_key)
        sent_creation_tx = bdb.transactions.send(fulfilled_creation_tx)

        voter_dict['voter_ids'][i] = sent_creation_tx['id']  # Voter asset creation id
        voter_dict['signing_keys'][i] = temp.signing_key  # private key for login
        del temp, prepared_creation_tx, fulfilled_creation_tx, sent_creation_tx  # Delete temp variable for security reasons
        time.sleep(delay)  # Cannot handle multiple votes in same timestamp
    return voter_dict


# Create Candidate Assets with no asset implemented
# Input: (int)number of candidate to make / (str) corresponding poll's id
# Output: (dict){ [(str)'candidate_ids'][(int)index]: Created Asset IDs
#                 [(str)'verifying_keys'][(int)index]: Candidate public keys
def make_candidate(candidate_num, poll_id):
    candidate_dict = {'candidate_ids': {}, 'verifying_keys': {}}  # id:public
    for i in range(0, candidate_num):
        temp = generate_keypair()
        metadata = {'poll_id': poll_id}
        prepared_creation_tx = bdb.transactions.prepare(operation='CREATE',  # Ballot Endpoint Asset Creation
                                                        owners_before=temp.verifying_key,
                                                        asset=None,  # Candidate Does Not Hold Ballot Asset
                                                        metadata=metadata, )
        fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx,
                                                         private_keys=temp.signing_key)
        sent_creation_tx = bdb.transactions.send(fulfilled_creation_tx)

        candidate_dict['candidate_ids'][i] = sent_creation_tx['id']  # Candidate asset creation ID
        candidate_dict['verifying_keys'][i] = temp.verifying_key  # Private key is not needed for transaction
        del temp, prepared_creation_tx, fulfilled_creation_tx, sent_creation_tx  # Delete temp variable for security reasons
        time.sleep(delay)
    return candidate_dict


# Dict -> List formatter functions
# Input: (dict)
# Output: (list)
def list_voter_ids(voter):
    return list(voter['voter_ids'].values())


def list_voter_private_keys(voter):
    return list(voter['signing_keys'].values())


def list_candidate_public_keys(candidate):
    return list(candidate['verifying_keys'].values())


def list_candidate_ids(candidate):
    return list(candidate['candidate_ids'].values())

##################################################################
# Version 0.1 Created by 김재훈

# from bigchaindb_driver import BigchainDB
# from bigchaindb_driver.crypto import generate_keypair
# import sys
#
# voter_key_set = {'voter_key_set': {}}
# candidate_key_set = {'candidate_key_set': {}}
#
#
# def make_keys_for_voters(voter_num):
#     for i in range(0, voter_num):
#         temp = generate_keypair()
#         voter_key_set['voter_key_set'][str(temp.verifying_key)] = str(temp.signing_key)
#
#     return voter_key_set
#
#
# def make_keys_for_candidate(candidate_num):
#     for i in range(0, candidate_num):
#         temp = generate_keypair()
#         candidate_key_set['candidate_key_set'][str(temp.verifying_key)] = str(temp.signing_key)
#     return candidate_key_set
#
#
# voter = make_keys_for_voters(int(sys.argv[1]))
# print(voter)
# candidate = make_keys_for_candidate(int(sys.argv[2]))
