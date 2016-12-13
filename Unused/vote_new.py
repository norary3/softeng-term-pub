import logging
import time
import bdb_config
from cryptoconditions import crypto
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.exceptions import NotFoundError
from bigchaindb_driver.exceptions import TransportError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

bdb = BigchainDB(bdb_config.host)
delay = 1.0


# Actual Voting function with duplicate checker implemented
# Input: (str)Current voter ID/(str)current voter private key
#       /(str)candidate public key/(list)List of past verified transfer ID list
# Output: (str)Validated block id or (None)None
def transfer_ballot(voter_private_key, candidate_public_key, verified_transfer_ids, candidate_dict, voter_ids):
    # find corresponding public_key by its private_key
    voter_public_key = crypto.Ed25519SigningKey(voter_private_key).get_verifying_key().encode().decode()
    for voter_id in voter_ids:
        retrieve_block = bdb.transactions.retrieve(voter_id)  # call by txid    
        if retrieve_block['transaction']['fulfillments'][0]['owners_before'][0] == voter_public_key:
            logging.info("Voter (" + retrieve_block['transaction']['fulfillments'][0]['owners_before'][0] + ")"
                         + " is trying to transfer ballot to Candidate (" + str(candidate_public_key) + ")")

            if not poll_id_check(retrieve_block, candidate_public_key, candidate_dict):
                # voter is trying to vote to a candidate in different poll OR
                # Candidate is not in the list of candidates of the poll.
                return None

            cid = 0
            condition = retrieve_block['transaction']['conditions'][cid]
            transfer_input = {'fulfillment': condition['condition']['details'],
                              'input': {'cid': cid,
                                        'txid': retrieve_block['id'],
                                        },
                              'owners_before': condition['owners_after'],
                              }

            prepared_transfer_tx = bdb.transactions.prepare(
                operation='TRANSFER',
                asset=retrieve_block['transaction']['asset'],
                inputs=transfer_input,
                owners_after=candidate_public_key,  # asset endpoint
            )

            fulfilled_transfer_tx = bdb.transactions.fulfill(prepared_transfer_tx,
                                                             private_keys=voter_private_key, )
            try:
                sent_transfer_tx = bdb.transactions.send(fulfilled_transfer_tx)
            except TransportError as Error:
                logging.warning(
                    'Already voted to another candidate Or It is an invalid transaction')  # Duplicate vote error logging
                return None

            try:
                time.sleep(delay)
                status = bdb.transactions.status(sent_transfer_tx['id'])
                if status['status'] == 'valid':  # When the transaction is already sent and valid.
                    logging.warning('Already voted to same candidate')  # log vote success
                    return None
                elif status['status'] == 'backlog':  # When the transaction is sent and waiting to be valid.
                    logging.info("Transaction ID : " + sent_transfer_tx['id'] + " Voter (" +
                                 retrieve_block['transaction']['fulfillments'][0]['owners_before'][0] + ")"
                                 + " tied to transfer ballot to Candidate (" + str(candidate_public_key) + ")")
                    return sent_transfer_tx['id']  # return only the sent_transfer_tx's id
            except NotFoundError as e:
                logger.info('Transaction "%s" was not found.', txid)
                return None
    return None


# Poll Id checker
# Input: (Block)Current voter_block/(str)Current candidate_public_key/(dictionary) dictionary of candidates in that poll
# Output: (boolean)TRUE: Voter is trying to vote to a candidate in sound poll.
#                  False: Voter is trying to vote to a candidate in different poll.
#                  False: Candidate is NOT in the list of candidates of the poll.
def poll_id_check(voter_block, candidate_public_key, candidate_dict):
    for i in range(len(candidate_dict['verifying_keys'].values())):
        if list(candidate_dict['verifying_keys'].values())[i] == candidate_public_key:
            candidate_create_block = bdb.transactions.retrieve(
                list(candidate_dict['candidate_ids'].values())[i])  # call by id
            if voter_block['transaction']['asset']['data']['vote']['poll_id'] == \
                    candidate_create_block['transaction']['metadata']['data']['poll_id']:
                return True
            else:
                logging.warning('Vote to different Poll Committed')
                return False
        else:
            continue
    logging.warning('Candidate is not in the poll')
    return False


# Duplicate checker
# Input: (Block)Current voter_block/(list)Verified Transfer ID List
# Output: (boolean)TRUE:No Duplicate
#                  False:Duplicate found in Verified ID List
def duplicate_check(voter_block, verified_transfer_ids):
    if len(verified_transfer_ids) == 0:
        return True
    for i in range(0, len(verified_transfer_ids)):
        transfer_block = bdb.transactions.retrieve(verified_transfer_ids[i])
        if (transfer_block['transaction']['fulfillments'][0]['owners_before'][0]
                == voter_block['transaction']['fulfillments'][0]['owners_before'][0]):
            return False
        else:
            continue
    return True

# Exception Handling Not Implemented
# def transfer_ballot(voter_id, voter_private_key, candidate_public_key):
#     try:
#         retrieve_block = bdb.transactions.retrieve(voter_id)
#         transfer_block = bdb.transactions.transfer(
#             retrieve_block,
#             candidate_public_key,
#             retrieve_block['transaction']['asset'],
#             voter_private_key
#         )
#     except BigchaindbException as e:
#         print(e)
#         return None
#
#     return transfer_block['id']

##################################################################
# Version 0.1 Created by 박종훈

# import sys
# import time
# import logging
# from bigchaindb_driver import BigchainDB
# from bigchaindb.common.exceptions import KeypairMismatchException
#
# bdb = BigchainDB('http://localhost:9984/api/v1')
# logging.basicConfig(level=logging.DEBUG)
# vote = {
#     'data': {
#         'vote': {
#             'poll_id': 'abcd1234',
#         },
#     },
# }
#
# sign_key = sys.argv[1]  # 'm9DJRc7PF5aJ62fuN7kdqrD34P42cLRbDfjqB5z7cYH'
# vote_to = sys.argv[2]  # '2H33a8XNH7VXMwVNbqCWsM9dfAPrGkcNQGNvTHrA8K1p'
#
# verifying_keys = ['AMrzzErJCTEGkWuGgDGLyMdLypLJ2cdS6rK1wGUg4EfS', 'Hzsdai8iBSzWVFSpFwLGuiFapfHvtVvVENsvnKu44qpm']
#
# logging.info('Testing verifying key')
# for verifying_key in verifying_keys:
#     try:
#         creation_tx = bdb.transactions.create(verifying_key=verifying_key,
#                                               signing_key=sign_key,
#                                               asset=vote)
#         logging.info('correct verifying key')
#         time.sleep(2)
#         transfer_tx = bdb.transactions.transfer(
#             creation_tx,
#             vote_to,
#             asset=creation_tx['transaction']['asset'],
#             signing_key=sign_key,
#         )
#         logging.info('Voting complete')
#         break
#     except KeypairMismatchException as e:
#         continue
